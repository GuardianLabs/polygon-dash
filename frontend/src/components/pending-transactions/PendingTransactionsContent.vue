<script setup>
import { store } from '@/store'

</script>

<template>
  <section class="pending_txs-content">
    <div class="pending_txs-content__text">
      <h2>
        Pending transactions in {{ store.activeBlockchain }}
      </h2>
      <p>
        Let's say something
      </p>
    </div>
  </section>
</template>

<style lang="scss">
@import "@/assets/breakpoints.scss";

.pending_txs-content {
  padding: 4rem 0;
  word-break: break-all;
}

@media (min-width: $breakpoint-tablet) {
  .pending_txs-content {
    padding: 3rem 0;
  }
}

@media (min-width: $breakpoint-desktop) {
  .pending_txs-content {
    padding: 7.5rem 0;
    word-break: break-all;
  }
}
</style>
