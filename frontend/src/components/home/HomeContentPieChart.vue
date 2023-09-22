<script setup>
import { onMounted, ref, shallowRef, watch } from 'vue';
import Chart from 'chart.js/auto';

import { fetchMinerDistribution } from '@/api/api-client';
import { useRequest } from '@/use/useRequest';
import { store } from '@/store';

const chart = ref(null);
const chartData = ref(null);
const { sendRequest: getMinerDistribution, isLoading, data, error } = useRequest(fetchMinerDistribution);


const pieChart = shallowRef(null)
const fetchChartData = async () => {
  await getMinerDistribution();
  if (error.value) {
    return;
  }
  if (data.value) {
    chartData.value = data.value;
  }
};

onMounted(async () => {
  await fetchChartData();
  pieChart.value = new Chart(chart.value, {
    type: 'pie',
    data: {
      datasets: [chartData.value.pie_chart],
    },
    options: {
      responsive: true,
    }
  });
});

watch(() => store.activeBlockchain, async () => {
  await fetchChartData();
  pieChart.value.data.datasets = [chartData.value.pie_chart];
  pieChart.value.update();
});
</script>

<template>
  <div class="home-content-pie-chart" v-loading="isLoading">
    <canvas v-if="chartData" ref="chart" />
  </div>
</template>

<style lang="scss">
.home-content-pie-chart {
  position: relative;
}
</style>
