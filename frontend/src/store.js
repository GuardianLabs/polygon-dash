import { reactive } from 'vue'
import { appConfig } from '@/utils/config';

export const store = reactive({
  activeBlockchain: window.localStorage.getItem('activeBlockchain') || appConfig.supportedBlockchains.POLYGON,
  changeActiveBlockchain(blockchain) {
    this.activeBlockchain = blockchain
    window.localStorage.setItem('activeBlockchain', blockchain)
  }
})
