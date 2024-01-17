<script setup>
defineProps({
  pendingTransactions: {
    type: Array,
    default: [],
  },
  rowType: {
    type: String,
    default: '',
  },
});

const POLYGON_SCAN_URL = 'https://polygonscan.com/tx/';

</script>

<template>
  <div class="pending-transactions-column">
    <h2>{{ rowType }}</h2>
    <ul  class="pending-transactions-column_list">
        <li v-for="transaction in pendingTransactions" :key="transaction.hash">
          <a :href="POLYGON_SCAN_URL+transaction.hash" target="_blank">
            <span>{{ transaction.hash }}</span>
          </a>
        </li>
    </ul>
  </div>
</template>

<style lang="scss">
@import "@/assets/colors.scss";
.pending-transactions-column {
  flex: 1;
  overflow: auto;
  padding-bottom: 2rem;
  h2 {
    text-align: center;
    margin-bottom: 0.5rem;
  }
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
      li {
      padding: 0.5rem;
      border: 1px solid $gray-500;
      word-break: break-all;
      background-color: $gray-100;
      border-radius: 0.5rem;
      margin-bottom: 0.25rem;
      box-shadow: 0 0 0.3rem $gray-300;
      a {
        color: $gray-900;
        text-decoration: none;
        &:hover {
          color: $gray-900;
          text-decoration: underline;
        }
      }
    }
  }
 
  .pending-transactions-column_list {
    // max-width: 100%;
    text-overflow: hidden;
  }
}
</style>
