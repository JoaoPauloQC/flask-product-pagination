import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
CLOUD_NAME = 'dkhbqhukd'
CO_API_KEY = "197532342159747"
CO_API_SECRET = "46pmQS9UlHDtXdHfrs3CkeyLMg4"

load_dotenv()

DATABASE_URL = "sqlite:///meubanco.db"
print(DATABASE_URL)

# Cria engine e testa conexão
try:
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Conexão MySQL bem-sucedida!')
except Exception as e:
    print('❌ Erro ao conectar ao MySQL:', e)


SECRET_KEY = 'your-secret-key'
