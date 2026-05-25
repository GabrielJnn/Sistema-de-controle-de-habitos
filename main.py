from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect("host=127.0.0.1 dbname=sistema_de_controle_de_habitos user=postgres password=1234")

@app.post("/criar_tabelas")
def criar_tabelas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS habitos (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE)")
        cur.execute("CREATE TABLE IF NOT EXISTS records (id SERIAL PRIMARY KEY, habito_name VARCHAR(100), frequencia INT DEFAULT 0, hora DATE DEFAULT CURRENT_DATE, FOREIGN KEY (habito_name) REFERENCES habitos(name) ON DELETE CASCADE)")
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Tabelas criadas com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/criar_habito")
def criar_habito(nameHabit: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor() 
        cur.execute("INSERT INTO habitos (name) VALUES (%s)", (nameHabit,))
        cur.execute("INSERT INTO records (habito_name) VALUES (%s)", (nameHabit,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": f"Hábito '{nameHabit}' criado"}
    except Exception as e:
        return {"status": "error", "message": "Erro, o nome deve ser único ou inválido"}

@app.get("/informacoes_habitos")
def informacoes_habitos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM habitos")
        habitos = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return {"status": "success", "data": habitos}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/marcar_frequencia/{habito_id}")
def marcar_frequencia(habito_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM habitos WHERE id = %s", (habito_id,))
        resultado = cur.fetchone()
        if not resultado:
            return {"status": "error", "message": "Hábito não existe"}
        nome = resultado[0]
        cur.execute("INSERT INTO records (frequencia, habito_name) VALUES (1, %s)", (nome,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": f"Frequência marcada para '{nome}'"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/deletar_habito/{habito_id}")
def deletar_habito(habito_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM habitos WHERE id = %s", (habito_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Hábito deletado com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ver_historico")
def ver_historico():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT habito_name, SUM(frequencia) FROM records GROUP BY habito_name")
        historico = [{"name": row[0], "frequencia": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return {"status": "success", "data": historico}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/apagar_dados")
def apagar_dados():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS records")
        cur.execute("DROP TABLE IF EXISTS habitos")
        cur.execute("CREATE TABLE IF NOT EXISTS habitos (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE)")
        cur.execute("CREATE TABLE IF NOT EXISTS records (id SERIAL PRIMARY KEY, habito_name VARCHAR(100), frequencia INT DEFAULT 0, hora DATE DEFAULT CURRENT_DATE, FOREIGN KEY (habito_name) REFERENCES habitos(name) ON DELETE CASCADE)")
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Dados resetados"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
