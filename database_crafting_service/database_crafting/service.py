from pymongo import MongoClient
from database_crafting.mongo_database_crafting import MongoDatabaseCraftingPipeline

from database_crafting.timeout.timeout_in_seconds_processor import (
    TimeoutInSecondProcessorFactory,
)
from database_crafting.monitoring.default_logger import DefaultLogger

DefaultLogger().info("Start crafting database")

db_client: MongoClient = MongoClient("localhost", port=27017)
db = db_client.ColorNoKami
timeout_factory = TimeoutInSecondProcessorFactory(1)
pipeline = MongoDatabaseCraftingPipeline(db, timeout_factory)
pipeline.execute()

DefaultLogger().info("End of crafting")
