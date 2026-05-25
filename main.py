from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import IntegrityError
import datetime

load_dotenv()

db_host = os.getenv("DB_HOST", "127.0.0.1")
db_name = os.getenv("DB_NAME", "sistema_de_controle_de_habitos")
db_user = os.getenv("DB_USER", "postgres")
db_pass = os.getenv("DB_PASS", "1234")
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Habito(Base):
    __tablename__ = "habitos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True)

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    habito_name = Column(String(100), ForeignKey("habitos.name", ondelete="CASCADE"))
    frequencia = Column(Integer, default=0)
    hora = Column(Date, default=datetime.date.today)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HabitoCreate(BaseModel):
    name: str

@app.post("/criar_tabelas")
def criar_tabelas():
    try:
        Base.metadata.create_all(bind=engine)
        return {"status": "success", "message": "Tabelas criadas com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/criar_habito")
def criar_habito(habito: HabitoCreate):
    db: Session = SessionLocal()
    try:
        novo_habito = Habito(name=habito.name)
        db.add(novo_habito)
        novo_record = Record(habito_name=habito.name, frequencia=0)
        db.add(novo_record)
        db.commit()
        return {"status": "success", "message": f"Hábito '{habito.name}' criado"}
    except IntegrityError:
        db.rollback()
        return {"status": "error", "message": "Erro, o nome deve ser único ou inválido"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.get("/informacoes_habitos")
def informacoes_habitos():
    db: Session = SessionLocal()
    try:
        habitos = db.query(Habito).all()
        return {"status": "success", "data": [{"id": h.id, "name": h.name} for h in habitos]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.post("/marcar_frequencia/{habito_id}")
def marcar_frequencia(habito_id: int):
    db: Session = SessionLocal()
    try:
        habito = db.query(Habito).filter(Habito.id == habito_id).first()
        if not habito:
            return {"status": "error", "message": "Hábito não existe"}
        
        novo_record = Record(habito_name=habito.name, frequencia=1)
        db.add(novo_record)
        db.commit()
        return {"status": "success", "message": f"Frequência marcada para '{habito.name}'"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.delete("/deletar_habito/{habito_id}")
def deletar_habito(habito_id: int):
    db: Session = SessionLocal()
    try:
        habito = db.query(Habito).filter(Habito.id == habito_id).first()
        if habito:
            db.delete(habito)
            db.commit()
        return {"status": "success", "message": "Hábito deletado com sucesso"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.get("/ver_historico")
def ver_historico():
    db: Session = SessionLocal()
    try:
        records = db.query(Record.habito_name, func.sum(Record.frequencia).label("total")).group_by(Record.habito_name).all()
        return {"status": "success", "data": [{"name": r.habito_name, "frequencia": r.total or 0} for r in records]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.delete("/apagar_dados")
def apagar_dados():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"status": "success", "message": "Dados resetados"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
