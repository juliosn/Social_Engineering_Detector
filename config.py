import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
DATA_ASSET_ID = os.getenv("DATA_ASSET_ID")

DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

RESULT_PATH = os.getenv("RESULT_PATH")
MODEL_LOCATION = os.getenv("MODEL_LOCATION")
TRAINING_STATUS = os.getenv("TRAINING_STATUS")

required_vars = {
    "API_KEY": API_KEY,
    "PROJECT_ID": PROJECT_ID,
    "DATA_ASSET_ID": DATA_ASSET_ID,
    "DEPLOYMENT_URL": DEPLOYMENT_URL
}
missing = [k for k, v in required_vars.items() if v is None]
if missing:
    raise EnvironmentError(f"Variáveis faltando no .env: {', '.join(missing)}")
