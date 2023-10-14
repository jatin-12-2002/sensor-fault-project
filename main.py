from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import sys, os
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object

from fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running")
        train_pipeline.run_pipeline()
        return Response("Training pipeline Successfully")
    
    except Exception as e:
        raise Exception(f"Error occured!! {e}")
    
@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None

        #train df
        #upload df
        #Calculate datadrift then trigger a email to data scientist team that data drift is detected
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        # we decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)
    
    
if __name__=='__main__':
    app_run(app, host=APP_HOST, port=APP_PORT)
    
    
    
    





    
    
    
    
    
    
    
# def test_exception():
#     try:
#         logging.info("We are dividing 1 by zero")
#         x=1/0
#     except Exception as e:
#         raise SensorException(e,sys)
    
    # training_pipeline_config = TrainingPipelineConfig()
    # data_ingestion_Config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    # print(data_ingestion_Config.__dict__)
    # mongodb_client = MongoDBClient()
    # print("collection name:",mongodb_client.database.list_collection_names())
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)