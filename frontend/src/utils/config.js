export const appConfig = {
  API_BASE_URL_POLYGON: import.meta.env.VITE_APP_API_BASE_URL_POLYGON || 'http://localhost:5050',
  API_BASE_URL_CARDANO: import.meta.env.VITE_APP_API_BASE_URL_CARDANO || 'http://localhost:5050',
  supportedBlockchains: {
    POLYGON: 'polygon',
    CARDANO: 'cardano',
  }
}
