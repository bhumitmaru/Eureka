import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'eureka-local-development')
    DATABASE = str(ROOT / os.getenv('DATABASE_PATH', 'data/eureka.db'))
    DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL_SECONDS', '300'))
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY_SECONDS', '0.25'))
    CROSSREF_EMAIL = os.getenv('CROSSREF_EMAIL', '')
    SEMANTIC_SCHOLAR_API_KEY = os.getenv('SEMANTIC_SCHOLAR_API_KEY', '')
