import axios from 'axios'
import { appConfig } from '@/utils/config'
import { store } from '@/store'

const { API_BASE_URL_POLYGON, API_BASE_URL_CARDANO, supportedBlockchains } = appConfig

const apiClientPolygon = axios.create({
  baseURL: API_BASE_URL_POLYGON,
})

const apiClientCardano = axios.create({
  baseURL: API_BASE_URL_CARDANO,
})

const apiClients = {
  [supportedBlockchains.POLYGON]: apiClientPolygon,
  [supportedBlockchains.CARDANO]: apiClientCardano,
}

const ENDPOINTS = {
  FETCH_TABLE: `/dash/miners`,
  FETCH_MINER: (address) => `/dash/miners/${address}`,
  FETCH_MINER_DISTRIBUTION: `/dash/trust-distribution`,
  FETCH_PENDING_TRANSACTIONS: `/dash/pending-txs`,
}

export const fetchTable = (args) => apiClients[store.activeBlockchain]
  .get(ENDPOINTS.FETCH_TABLE, { params: args })
export const fetchMiner = ({ address, params }) => apiClients[store.activeBlockchain]
  .get(ENDPOINTS.FETCH_MINER(address), { params })
export const fetchMinerDistribution = () => apiClients[store.activeBlockchain]
  .get(ENDPOINTS.FETCH_MINER_DISTRIBUTION)
export const fetchPendingTransactions = () => apiClients[store.activeBlockchain]
  .get(ENDPOINTS.FETCH_PENDING_TRANSACTIONS)
