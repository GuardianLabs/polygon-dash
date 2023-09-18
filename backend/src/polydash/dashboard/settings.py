from pydantic import BaseSettings

from polydash.common.settings import PostgresSettings
from polydash.common.settings import BlockRetrieverSettings


class DashboardSettings(BaseSettings):
    postgres_connection: PostgresSettings = PostgresSettings()
    block_retriever: BlockRetrieverSettings = BlockRetrieverSettings()
    port: int = 5500
    host: str = "0.0.0.0"
    log_level: str = "ERROR"
