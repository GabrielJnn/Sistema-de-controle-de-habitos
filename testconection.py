import psycopg2


conn = psycopg2.connect(
    "dbname=sistema_de_controle_de_habitos user=postgres password=jose369875")

try:
   # i = input("Conectado ao sistema de controle de hábitos\ndigite 1 para criar um hábito      digite 2 para acessar informações dos hábitos       digite 3 para sair\n>>>")
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
    i = input("digite 1 para criar um hábito      digite 2 para acessar informações dos hábitos       digite 3 para sair\n>>>")
    if i == "1":
        try:
            nameHabit = input("Nome do hábito: ")
            cur.execute("INSERT INTO habitos (name) VALUES (%s)",
                        (nameHabit,))
            cur.execute(
                "INSERT INTO records (habito_name) VALUES (%s)", (nameHabit,))
            conn.commit()
        except:
            print("erro")
            conn.rollback()
    elif i == "2":
        while True:
            i = 0
            i = input(
                "opções: 1 marcar frequencia /// 2 deletar hábito /// 3 ver histórico //// 4 para sair\n>>>")
            if i == "1":
                # try:
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
                    "UPDATE records SET frequencia = frequencia + 1 WHERE id = %s", (i2,))

                conn.commit()
            elif i == "2":
                pass
            elif i == "3":
                cur.execute("SELECT habito_name, frequencia FROM records")
                print(cur.fetchall())
            elif i == "4":
                break
    elif i == "3":
        break

try:

    cur.execute("DROP TABLE IF EXISTS records")
    cur.execute("DROP TABLE IF EXISTS habitos")
    conn.commit()
    cur.close
    conn.close()
    print("bom")
except:
    cur.close()
    conn.close()
    print("ruim")
