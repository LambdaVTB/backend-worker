import neo4j

from worker.configs.get_settings import get_neo4j_settings

class Graph:
    driver: neo4j.AsyncNeo4jDriver

    @classmethod
    async def connect_db(cls):
        cls.driver = neo4j.AsyncGraphDatabase.driver(
            get_neo4j_settings().NEO4J_URL, auth=(
                get_neo4j_settings().NEO4J_USERNAME, get_neo4j_settings().NEO4J_PASSWORD
            )
        )
        await cls.driver.verify_connectivity()

    @classmethod
    async def write(cls, query, **kwargs):
        async def write_transaction(tx):
            await tx.run(query, **kwargs)

        async with cls.driver.session() as session:
            await session.write_transaction(write_transaction)

    @classmethod
    async def read(cls, query, **kwargs):
        async def read_transaction(tx):
            result = await tx.run(query, **kwargs)
            values = await result.data()
            return values

        async with cls.driver.session() as session:
            values = await session.read_transaction(read_transaction)
        return values

    @classmethod
    async def disconnect_db(cls):
        await cls.driver.close()
