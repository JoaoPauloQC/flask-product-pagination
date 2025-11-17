# create_db.py
from config import engine
from models.model import Base


def criar_banco():
    """Cria todas as tabelas no banco de dados MySQL."""
    print("🚀 Criando tabelas no banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Banco e tabelas criadas com sucesso!")
    except Exception as e:
        print("❌ Erro ao criar o banco de dados:", e)


if __name__ == "__main__":
    criar_banco()
