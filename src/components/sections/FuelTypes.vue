<template>
  <section id="fueltypes" class="page-section">
    <div class="chart-header">
      <h2>Energy as a Resource: Understanding the Sources</h2>
    </div>
    <ItemsSlider title="Types of Fuel">
      <div v-for="(item, index) in fuelTypes" :key="index">
        <Card :title="item.title" :content="item.content" :imgSrc="item.imgSrc" />
      </div>
    </ItemsSlider>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import ItemsSlider from '../ItemsSlider.vue';
import Card from '../Card.vue';

const store = useEnergyDataStore()

const fuelTypes = [
  { title: 'Electricity', imgSrc: `fuel-electricity.jpg`, content: "A comon miss conception is to think of energy as just electricity. While it is the most versatile energy carrier for lighting, appliances, industry, and increasingly transport it's just a part of what is consumed at scale and often product from other fossil sources." },
  { title: 'Oil & Petroleum', imgSrc: `fuel-gas.jpg`, content: "The world’s largest primary energy source, essential for transport and petrochemicals. Thanks to its high energy density (~45 MJ/kg), it remains the backbone of global mobility and industrial feedstocks." },
  { title: 'Oil & Petroleum - Crude Oil', imgSrc: `fuel-crude-oil.webp`, content: "Crude oil is sent to refineries where it’s separated into gasoline, diesel, jet fuel, and other products. Its properties vary widely, classified by sulfur content (sweet vs. sour) and density (light vs. heavy), which determine how easily it can be processed." },
  { title: 'Oil & Petroleum - NGL', imgSrc: `fuel-ngl.webp`, content: "Propane, butane, and ethane are natural gas liquids that are separated during natural gas processing before the gas is sent to pipelines. They serve as fuels, petrochemical feedstocks, and heating sources." },
  { title: 'Natural Gas', imgSrc: `fuel-gas.jpg`, content: "Primarily methane (CH₄), it burns about 50% cleaner than coal, making it a lower‑carbon fossil fuel option. It’s essential for heating, electricity generation, and fertilizer production, and is transported long‑distance through pipelines or as liquefied natural gas (LNG) via tankers." },
  { title: 'Coal', imgSrc: `fuel-coal.jpg`, content: 'The most carbon‑intensive fossil fuel, ranked by geological maturity from lignite → sub‑bituminous → bituminous → anthracite. Despite declining use, it still plays a key role in power generation and steelmaking, but is being phased out across much of Europe under climate commitments.' },
  { title: 'Coal - Anthracite', imgSrc: `fuel-anthracite.jpg`, content: 'The highest‑grade coal, about 86–97% carbon with an energy content of 30–35 MJ/kg. It burns hot, clean, and smokeless, but is geologically rare compared to other coal types.' },
  { title: 'Coal - Coking Coal', imgSrc: `fuel-coking-coal.jpg`, content: 'A specialized grade of coal essential for blast‑furnace steel production, where it is converted into metallurgical coke (the high‑carbon, high‑strength fuel needed to melt iron ore and support the furnace structure).' },
  { title: 'Coal - Other Bituminous', imgSrc: `fuel-bituminous.jpg`, content: 'A mid‑grade coal used mainly in power generation, typically containing 45–86% carbon with an energy content of 24–35 MJ/kg.' },
  { title: 'Coal - Sub-bituminous', imgSrc: `fuel-sub-bituminous.jpg`, content: 'A mid‑rank coal between lignite and bituminous, typically containing 35–45% carbon and delivering 17–23 MJ/kg. It is used mainly for power generation due to its moderate energy content and wide availability.' },
  { title: 'Coal - Lignite', imgSrc: `fuel-lignite.jpg`, content: "Also known as brown coal, it contains 25–35% carbon and can hold up to ~75% moisture, giving it very low energy density. Because it tends to crumble when dried and is hard to transport efficiently, lignite is rarely traded internationally and is mostly used near the mine mouth for power generation." },
  { title: 'Peat', imgSrc: `fuel-peat.jpg`, content: 'Partially decomposed plant matter from bogs; a pre‑coal fuel with very low energy density (8–12 MJ/kg). Historically used for heating in northern Europe, but almost always sourced locally due to poor transportability.' },
]
</script>

<style scoped>
.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: var(--text-color-gray);
}

.error {
  color: var(--text-color-red);
}
</style>
