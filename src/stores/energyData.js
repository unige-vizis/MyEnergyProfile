import { defineStore } from "pinia";
import { ref, computed, nextTick } from "vue";

export const useEnergyDataStore = defineStore("energyData", () => {
  const rawData = ref(null);
  const consumptionsData = ref(null);
  const pricesData = ref(null);
  const ecoData = ref(null);
  const selectedCountryCode = ref("IT");
  const selectedYear = ref(2023);
  const isLoading = ref(false);
  const isYearChanging = ref(false);
  const error = ref(null);
  const pricesLoaded = computed(() => Boolean(pricesData.value));
  const ecoLoaded = computed(() => Boolean(ecoData.value));

  const countries = computed(() => {
    if (!rawData.value?.countries) return [];
    return Object.entries(rawData.value.countries)
      .map(([code, data]) => ({
        code,
        name: data.name,
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
  });

  const selectedCountry = computed(() => {
    if (!rawData.value?.countries || !selectedCountryCode.value) return null;
    const countryData = rawData.value.countries[selectedCountryCode.value];
    if (!countryData) return null;
    return {
      code: selectedCountryCode.value,
      name: countryData.name,
      years: countryData.years,
    };
  });

  const metadata = computed(() => rawData.value?.metadata || null);

  // Available years for the selected country (newest first)
  const availableYears = computed(() => {
    if (!selectedCountry.value?.years) return [];
    return Object.keys(selectedCountry.value.years)
      .map(Number)
      .sort((a, b) => b - a);
  });

  // Dependency data for the selected country and year
  const dependencyData = computed(() => {
    if (!selectedCountry.value?.years || !selectedYear.value) return null;
    const yearData = selectedCountry.value.years[selectedYear.value];
    return yearData?.dependency || null;
  });

  // Trade data (imports/exports with partners) for the selected country and year
  const tradeData = computed(() => {
    if (!selectedCountry.value?.years || !selectedYear.value) return null;
    const yearData = selectedCountry.value.years[selectedYear.value];
    if (!yearData) return null;
    return {
      imports: yearData.imports || null,
      exports: yearData.exports || null,
    };
  });

  // Production/consumption data for the selected country and year
  const productionConsumptionData = computed(() => {
    if (!selectedCountry.value?.years || !selectedYear.value) return null;
    const yearData = selectedCountry.value.years[selectedYear.value];
    if (!yearData) return null;
    return {
      production: yearData.production || null,
      consumption: yearData.consumption || null,
    };
  });

  const pieChartData = computed(() => {
    if (!consumptionsData.value || !selectedCountry.value?.name || !selectedYear.value) return [];

    const countryData = consumptionsData.value.countries[selectedCountry.value.name];
    if (!countryData) return [];

    const sectors = ["Industry", "Residential", "Transport", "Service"];

    return sectors.map((sector) => {
      const sectorData = countryData[sector];
      if (!sectorData) return null;

      const yearData = sectorData[selectedYear.value];
      if (!yearData) return null;

      const products = {};

      Object.entries(yearData).forEach(([endUseName, endUseData]) => {
        if (
          endUseName.includes("Manufacturing") ||
          endUseName.includes("Total residential") ||
          endUseName.includes("Total passenger and freight transport") ||
          endUseName.includes("Total services")
        ) {
          Object.entries(endUseData.products).forEach(([productName, productValue]) => {
            if (!productName.includes("Total")) {
              products[productName.replace("(PJ)", "").trim()] = productValue || 0;
            }
          });
        }
      });

      return {
        name: sector,
        energyType: Object.entries(products).map(([name, value]) => ({
          name,
          value,
        })),
      };
    });
  });

  const sunburstData = computed(() => {
    if (!consumptionsData.value || !selectedCountry.value?.name || !selectedYear.value) return [];

    const countryData = consumptionsData.value.countries[selectedCountry.value.name];
    if (!countryData) return [];

    const sectors = ["Industry", "Residential", "Transport", "Service"];
    const children = sectors
      .map((sector) => {
        const sectorData = countryData[sector];
        if (!sectorData) return null;

        const yearData = sectorData[selectedYear.value];
        if (!yearData) return null;

        // Collect children AND calculate total
        const sectorChildren = [];
        let total = 0;

        switch (sector) {
          case "Industry":
            Object.entries(yearData).forEach(([endUseName, endUseData]) => {
              const products = endUseData.products || {};
              const endUseTotal = products["Total final use (PJ)"] || 0;
              sectorChildren.push({ name: endUseName, value: endUseTotal });
              total += endUseTotal;
            });
            break;
          case "Transport":
            Object.entries(yearData).forEach(([endUseName, endUseData]) => {
              if (
                !endUseName.includes("Total") ||
                ["Total trains", "Total airplanes", "Total ships"].includes(endUseName)
              ) {
                const products = endUseData.products || {};
                const endUseTotal = products["Total final use (PJ)"] || 0;
                sectorChildren.push({ name: endUseName, value: endUseTotal });
                total += endUseTotal;
              }
              if (total === 0) {
                const totalTransport = yearData["Total passenger and freight transport"];
                if (totalTransport) {
                  total = totalTransport.products?.["Total final use (PJ)"] || 0;
                }
              }
            });
            break;
          default: // Residential, Service
            Object.entries(yearData).forEach(([endUseName, endUseData]) => {
              if (!endUseName.includes("Total residential") && !endUseName.includes("Total services")) {
                const products = endUseData.products || {};
                const endUseTotal = products["Total final use (PJ)"] || 0;
                sectorChildren.push({ name: endUseName, value: endUseTotal });
                total += endUseTotal;
              }
            });
            if (total == 0) {
              Object.entries(yearData).forEach(([endUseName, endUseData]) => {
                if ((endUseName = "Total residential" || endUseName == "Total services")) {
                  const products = endUseData.products || {};
                  const endUseTotal = products["Total final use (PJ)"] || 0;
                  total += endUseTotal;
                }
              });
            }
            break;
        }
        return {
          name: sector,
          value: total,
          children: sectorChildren,
        };
      })
      .filter((sector) => sector && sector.children.length > 0);

    return {
      name: selectedCountry.value.name + " " + selectedYear.value,
      children: children,
    };
  });

  // Carbon intensity for selected country
  const carbonIntensity = computed(() => {
    if (!ecoData.value?.countries || !selectedCountryCode.value) return null;
    const country = ecoData.value.countries[selectedCountryCode.value];
    return country?.carbon_intensity || null;
  });

  // Carbon intensity ranking (all countries sorted ascending)
  const carbonIntensityRanking = computed(() => {
    if (!ecoData.value?.carbon_intensity_ranking) return [];
    return ecoData.value.carbon_intensity_ranking;
  });

  // Per-capita emissions by sector for selected country
  const emissionsPerCapita = computed(() => {
    if (!ecoData.value?.countries || !selectedCountryCode.value) return null;
    const country = ecoData.value.countries[selectedCountryCode.value];
    return country?.emissions_per_capita || null;
  });

  // Total emissions (kt CO2) by sector for selected country
  const emissionsTotal = computed(() => {
    if (!ecoData.value?.countries || !selectedCountryCode.value) return null;
    const country = ecoData.value.countries[selectedCountryCode.value];
    return country?.emissions_total_kt || null;
  });

  // Emissions per capita ranking (all countries, sum of sectors, sorted ascending)
  const emissionsPerCapitaRanking = computed(() => {
    if (!ecoData.value?.countries) return [];

    const ranking = [];
    for (const [code, country] of Object.entries(ecoData.value.countries)) {
      const epc = country.emissions_per_capita;
      if (!epc) continue;

      const total = (epc.residential || 0) + (epc.services || 0) + (epc.transport || 0) + (epc.industry || 0);

      if (total > 0) {
        ranking.push({
          code,
          name: country.name,
          value: Math.round(total * 100) / 100,
          year: epc.year,
        });
      }
    }

    ranking.sort((a, b) => a.value - b.value);
    return ranking;
  });

  const electricitySeries = computed(() => {
    if (!pricesData.value || !selectedCountryCode.value) return [];

    const country_data = pricesData.value.countries[selectedCountryCode.value];
    if (!country_data) return [];

    const ELECTRICITY_KEY = "Price of electricity (US cents per kWh)";
    const QUARTERS = ["1", "2", "3", "4"];

    const years = Object.keys(country_data)
      .filter((k) => /^\d{4}$/.test(k)) // Only keys that are 4-digit years
      .map(Number) // Convert to numbers
      .sort((a, b) => a - b); // Sort ascending

    return years.map((year) => {
      const yearData = country_data[year];
      const cpi0450 = QUARTERS.map((q) => (yearData?.[q]?.CPI0450 != null ? Number(yearData[q].CPI0450) : null));
      return {
        year,
        electricity: yearData?.[ELECTRICITY_KEY] != null ? Number(yearData[ELECTRICITY_KEY]) : null,
        CPI0450: cpi0450,
      };
    });
  });

  async function loadData() {
    if (rawData.value && consumptionsData.value && pricesData.value) return;

    isLoading.value = true;
    error.value = null;

    try {
      const dependencyJSON = await fetch(`${import.meta.env.BASE_URL}data/energy_mix.json`);
      const dependencyText = await dependencyJSON.text();
      // Handle NaN values in JSON (convert to null)
      const dependencyCleanedText = dependencyText.replace(/:\s*NaN/g, ": null");
      rawData.value = JSON.parse(dependencyCleanedText);

      const consumptionJSON = await fetch(`${import.meta.env.BASE_URL}data/energy_consumptions_by_sector.json`);
      const consumptionText = await consumptionJSON.text();
      const consumptionCleanedText = consumptionText.replace(/:\s*NaN/g, ": null");
      consumptionsData.value = JSON.parse(consumptionCleanedText);

      // Load prepared energy prices (quarterly CPI + annual electricity prices)
      try {
        const pricesJSON = await fetch(`${import.meta.env.BASE_URL}data/energy_prices.json`);
        const pricesText = await pricesJSON.text();
        const pricesCleaned = pricesText.replace(/:\s*NaN/g, ": null");
        pricesData.value = JSON.parse(pricesCleaned);
      } catch (err) {
        // Non-fatal: leave pricesData null and surface later
        console.warn("Failed to load energy_prices.json", err);
        pricesData.value = null;
      }

      // Load eco data (carbon intensity + emissions per capita)
      try {
        const ecoJSON = await fetch(`${import.meta.env.BASE_URL}data/eco_data.json`);
        const ecoText = await ecoJSON.text();
        ecoData.value = JSON.parse(ecoText.replace(/:\s*NaN/g, ": null"));
      } catch (err) {
        console.warn("eco_data.json not loaded", err);
        ecoData.value = null;
      }
    } catch (e) {
      error.value = e.message;
      console.error("Failed to load energy data:", e);
    } finally {
      isLoading.value = false;
    }
  }

  function setSelectedCountry(code) {
    selectedCountryCode.value = code;
  }

  function setSelectedYear(year) {
    if (year === selectedYear.value) return;
    isYearChanging.value = true;
    // Defer the actual data change so the spinner renders first
    requestAnimationFrame(() => {
      selectedYear.value = year;
      nextTick(() => {
        isYearChanging.value = false;
      });
    });
  }

  return {
    rawData,
    selectedCountryCode,
    selectedYear,
    isLoading,
    isYearChanging,
    error,
    countries,
    selectedCountry,
    metadata,
    availableYears,
    dependencyData,
    tradeData,
    productionConsumptionData,
    pieChartData,
    sunburstData,
    loadData,
    setSelectedCountry,
    setSelectedYear,
    pricesData,
    pricesLoaded,
    electricitySeries,
    ecoData,
    ecoLoaded,
    carbonIntensity,
    carbonIntensityRanking,
    emissionsPerCapita,
    emissionsPerCapitaRanking,
    emissionsTotal,
  };
});
