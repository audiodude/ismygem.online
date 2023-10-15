import os
from dotenv import load_dotenv

if os.environ.get('GEM_ENV') != 'production':
  load_dotenv()
