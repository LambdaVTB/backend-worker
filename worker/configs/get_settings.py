from worker.configs.postgresql import PostgresSettings
from worker.configs.neo4j import Neo4jSettings

def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()

def get_neo4j_settings() -> Neo4jSettings:
    return Neo4jSettings()
