export const appConfig = {
  API_BASE_URL_POLYGON: import.meta.env.VITE_APP_API_BASE_URL_POLYGON || 'http://localhost:1234',
  API_BASE_URL_CARDANO: import.meta.env.VITE_APP_API_BASE_URL_CARDANO || 'http://localhost:1235',
  supportedBlockchains: {
    POLYGON: 'polygon',
    CARDANO: 'cardano',
  }
}
