import { createRouter, createWebHistory } from 'vue-router'
import { store } from '@/store';
import { appConfig } from '@/utils/config';

import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: () => {
        return { name: 'home', params: { blockchain: store.activeBlockchain } }
      }
    },
    {
      path: '/:blockchain/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/:blockchain/miner/:address',
      name: 'miner',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/MinerView.vue')
    },
    {
      path: '/:blockchain/pending-transactions/',
      name: 'pending-transactions',
      component: () => import('../views/PendingTransactionsView.vue')
    }
  ],
  scrollBehavior (to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
  },
})

router.beforeEach((to, from, next) => {
  const blockchain = to?.params?.blockchain ?? null
  const isBlockchainSupported = Object.values(appConfig.supportedBlockchains).includes(blockchain)
  const isNotActiveBlockchain = blockchain !== store.activeBlockchain

  if (!isBlockchainSupported) {
    next({ name: 'home', params: { blockchain: store.activeBlockchain } })
    return
  }

  if (isNotActiveBlockchain) {
    store.changeActiveBlockchain(blockchain)
  }
  next()
})

export default router
