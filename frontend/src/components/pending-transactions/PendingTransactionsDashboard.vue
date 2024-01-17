<script setup>
import { onMounted, ref, shallowRef, onUnmounted } from 'vue';
import { useRequest } from '@/use/useRequest';
import { fetchPendingTransactions } from '@/api/api-client';
import PendingTransactionsBody from '@/components/pending-transactions/PendingTransactionsBody.vue';
const { sendRequest: getPendingTransactions, isLoading, data, error } = useRequest(fetchPendingTransactions);
const ROW_TYPE = {
  PENDING: 'Pending',
  IN_BLOCK: 'In Block',
  TO_DELETE: 'Pending to delete',
};
const pendingTransactions = ref({ pending: [], in_block: [], to_delete: []});
let timeoutId = null;

const fetchPendingTransactionsData = async () => {
  if (isLoading.value) {
    return;
  }
  clearTimeout(timeoutId);
  await getPendingTransactions();
  if (error.value) {
    return;
  }
  if (data.value) {
    console.log(data.value)
    pendingTransactions.value = data.value;
  }
  setTimeoutForPendingTransactionsData();
};

const setTimeoutForPendingTransactionsData = () => {
  timeoutId = setTimeout(async () => {
    await fetchPendingTransactionsData();
  }, 10 * 1000);
};

onMounted(async () => {
  await fetchPendingTransactionsData();
});
onUnmounted(() => {
  clearTimeout(timeoutId);
});
</script>

<template>
  <div v-loading="isLoading" class="pending-transactions-dashboard">
    <PendingTransactionsBody :pendingTransactions="pendingTransactions.pending" :rowType="ROW_TYPE.PENDING" />
    <PendingTransactionsBody :pendingTransactions="pendingTransactions.in_block" :rowType="ROW_TYPE.IN_BLOCK" />
    <PendingTransactionsBody :pendingTransactions="pendingTransactions.to_delete" :rowType="ROW_TYPE.TO_DELETE" />
  </div>
</template>

<style lang="scss">
@import "@/assets/colors.scss";

.pending-transactions-dashboard {
  display: flex;
  padding-bottom: 2rem;
  gap: 2rem;
  justify-content: center;
  :first-child ul li:nth-child(-n+25) {
    background-color: #e7e88c;
}
}
</style>
