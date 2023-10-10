import sys
from typing import Optional

import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException

class SensorData:
    """
    This class help to export entire mongo db record as pandas daataframe
    """

    def __init__(self):
        """

        """
        try:
            self.mongodb_client = MongoDBClient(database_name = DATABASE_NAME)
        except Exception as e:
            raise SensorException(e,sys)

    def export_collection_as_dataframe(
            self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        This method help to export entire mongo db collection record as pandas dataframe:
        return pd.DataFrame of collection record
        """
        try:
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client[collection_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.tolist():
                df = df.drop(columns=["_id"], axis=1)
            
            df.replace({"na":np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise SensorException(e,sys)