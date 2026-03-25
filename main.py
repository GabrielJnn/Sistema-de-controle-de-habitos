import psycopg2


conn = psycopg2.connect(
    "dbname=sistema_de_controle_de_habitos user=postgres password=jose369875")

try:
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS habitos (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE)")
    conn.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS records (id SERIAL PRIMARY KEY, habito_name VARCHAR(100), frequencia INT DEFAULT 0, hora DATE DEFAULT CURRENT_DATE, FOREIGN KEY (habito_name) REFERENCES habitos(name) ON DELETE CASCADE)")
    conn.commit()
except:
    print('erro 1')
    conn.rollback()
while True:
    i = input("digite 1 para criar um hábito      digite 2 para acessar informações dos hábitos       digite 3 para sair    digite 4 para apagar todos os dados\n>>>")
    if i == "1":
        try:
            nameHabit = input("Nome do hábito: ")
            cur.execute("INSERT INTO habitos (name) VALUES (%s)",
                        (nameHabit,))
            cur.execute(
                "INSERT INTO records (habito_name) VALUES (%s)", (nameHabit,))
        except:
            print("Erro o nome deve ser único")
            conn.rollback()
        conn.commit()
    elif i == "2":
        while True:
            i = 0
            i = input(
                "opções: 1 marcar frequencia /// 2 deletar hábito /// 3 ver histórico //// 4 para voltar\n>>>")
            if i == "1":
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
            elif i == "2":
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
            elif i == "3":
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
            elif i == "4":
                break
    elif i == "3":
        break
    elif i == "4":

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
