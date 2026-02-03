import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useEnergyDataStore = defineStore("energyData", () => {
  const rawData = ref(null);
  const consumptionsData = ref(null);
  const selectedCountryCode = ref("IT");
  const selectedYear = ref(2023);
  const isLoading = ref(false);
  const error = ref(null);

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
              if (!endUseName.includes("Manufacturing")) {
                const products = endUseData.products || {};
                const endUseTotal = products["Total final use (PJ)"] || 0;
                sectorChildren.push({ name: endUseName, value: endUseTotal });
                total += endUseTotal;
              }
            });
            break;
          case "Transport":
            Object.entries(yearData).forEach(([endUseName, endUseData]) => {
              if (
                !endUseName.includes("Total") ||
                endUseName === "Total trains" ||
                endUseName === "Total airplanes" ||
                endUseName === "Total ships"
              ) {
                const products = endUseData.products || {};
                const endUseTotal = products["Total final use (PJ)"] || 0;
                sectorChildren.push({ name: endUseName, value: endUseTotal });
                total += endUseTotal;
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

  async function loadData() {
    if (rawData.value && consumptionsData.value) return;

    isLoading.value = true;
    error.value = null;

    try {
      const dependencyJSON = await fetch(`${import.meta.env.BASE_URL}data/energy_imports_exports_dependency.json`);
      const dependencyText = await dependencyJSON.text();
      // Handle NaN values in JSON (convert to null)
      const dependencyCleanedText = dependencyText.replace(/:\s*NaN/g, ": null");
      rawData.value = JSON.parse(dependencyCleanedText);

      const consumptionJSON = await fetch(`${import.meta.env.BASE_URL}data/energy_consumptions_by_sector.json`);
      const consumptionText = await consumptionJSON.text();
      const consumptionCleanedText = consumptionText.replace(/:\s*NaN/g, ": null");
      consumptionsData.value = JSON.parse(consumptionCleanedText);
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
    selectedYear.value = year;
  }

  return {
    rawData,
    selectedCountryCode,
    selectedYear,
    isLoading,
    error,
    countries,
    selectedCountry,
    metadata,
    availableYears,
    dependencyData,
    tradeData,
    pieChartData,
    sunburstData,
    loadData,
    setSelectedCountry,
    setSelectedYear,
  };
});
