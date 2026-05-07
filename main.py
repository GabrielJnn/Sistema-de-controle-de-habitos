from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    "host=127.0.0.1 dbname=sistema_de_controle_de_habitos user=postgres password=1234")

@app.get("/")
def criar_tabelas():

    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS habitos (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE)")
        conn.commit()
        cur.execute(
        "CREATE TABLE IF NOT EXISTS records (id SERIAL PRIMARY KEY, habito_name VARCHAR(100), frequencia INT DEFAULT 0, hora DATE DEFAULT CURRENT_DATE, FOREIGN KEY (habito_name) REFERENCES habitos(name) ON DELETE CASCADE)")
        conn.commit()
        return(True)
    except:
        conn.rollback()
        return(False)
@app.get("/criar_habito")
def criar_habito(nameHabit: str):
    try:
        cur = conn.cursor() 
        cur.execute("INSERT INTO habitos (name) VALUES (%s)",
                (nameHabit,))
        cur.execute(
        "INSERT INTO records (habito_name) VALUES (%s)", (nameHabit,))
    except:
        print("Erro o nome deve ser único")
        conn.rollback()
        conn.commit()
@app.get("/informacoes_habitos")
def informacoes_habitos():
           
            @app.get("/marcar_frequencia")
            def marcar_frequencia():
                try:
                    cur.execute("SELECT name FROM habitos")
                    x = cur.fetchall()
                    cur.execute("SELECT id FROM habitos")
                    id = cur.fetchall()
                    for counter in x:
                        for change in counter:
                            print(
                                f"habito {id[x.index(counter)][0]} >> {change}")
                    i2 = int(
                        input("Digite o numero do Hábito que vai ser marcado >> "))
                    cur.execute(
                        "SELECT name FROM habitos WHERE id = %s", (i2,))
                    i2 = cur.fetchall()
                    cur.execute(
                        "INSERT INTO records (frequencia, habito_name) VALUES (1, %s)", (i2))
                    conn.commit()
                except:
                    print("não existe nenhum hábito")
# tirar update e transformar em insert into
            @app.get("/deletar_habito")
            def deletar_habito(): 
                try:
                    cur.execute("SELECT name FROM habitos")
                    x = cur.fetchall()
                    cur.execute("SELECT id FROM habitos")
                    id = cur.fetchall()
                    for counter in x:
                        for change in counter:
                            print(
                                f"habito {id[x.index(counter)][0]} >> {change}")
                    i2 = int(
                        input("Digite o numero do Hábito que vai ser deletado >> "))
                    cur.execute(
                        "DELETE FROM habitos W2HERE id = %s", (i2,))
                    conn.commit()
                except:
                    print("não existe habitos")
            @app.get("/ver_historico")
            def ver_historico():
                cur.execute(
                    "SELECT habito_name, frequencia, hora FROM records WHERE frequencia > 0")
                x = cur.fetchall()
                newStr = ""
                for a in x:
                    newStr += "\n"
                    for b in a:
                        if a.index(b) == 0:
                            newStr += (f"Habito {b}")
                        elif a.index(b) == 1:
                            newStr += (f" frequência {b}")
                        elif a.index(b) == 2:
                            newStr += (
                                f" Seu registro foi em {str(b).replace("datetime.date", "")}")
                print(newStr)
                (cur.execute(
                    "SELECT habito_name, COUNT(frequencia) FROM records GROUP BY habito_name"))
                newStr = ""
                for a in cur.fetchall():
                    for b in a:
                        if a.index(b) == 0:
                            newStr = f"hábito: {b}"
                        if a.index(b) == 1:
                            newStr += f" frequência total: {b-1}"
                    print(newStr)
@app.get("/apagar_dados")
def apagar_dados():
    try:

        cur.execute("DROP TABLE IF EXISTS records")
        cur.execute("DROP TABLE IF EXISTS habitos")
        conn.commit()
        print("DELETANDO")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS habitos (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE)")
        conn.commit()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS records (id SERIAL PRIMARY KEY, habito_name VARCHAR(100), frequencia INT DEFAULT 0, hora DATE DEFAULT CURRENT_DATE, FOREIGN KEY (habito_name) REFERENCES habitos(name) ON DELETE CASCADE)")
        print("CRIANDO...\n RESETADO")
        conn.commit()
    except:
        print("ruim ERRORR")
