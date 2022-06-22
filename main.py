import psycopg2

# Функция, создающая структуру БД (таблицы)

def create_table():
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone_number;
            DROP TABLE client;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                name VARCHAR (40) NOT NULL,
                lastname VARCHAR (40) NOT NULL,
                e_mail VARCHAR (40) NOT NULL UNIQUE
        );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_number(
                id SERIAL PRIMARY KEY,
                phone_number CHAR(12) UNIQUE,
                client_id INTEGER REFERENCES client(id)
        );
        """)
    conn.commit()

# Функция, позволяющая добавить нового клиента

def put_client(name, lastname, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client (name, lastname, e_mail)
            VALUES(%s, %s, %s);
        """, (name, lastname, email))
        conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента

def put_number(name, lastname, number):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, lastname FROM client WHERE name=%s AND lastname=%s ;
            """, (name, lastname))
        client_inform = cur.fetchone()
    if name == client_inform[1] and lastname == client_inform[2]:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phone_number (phone_number, client_id)
                VALUES(%s, %s);
            """, (number, client_inform[0]))
    else:
        print('Такого клиента в базе не существует')
    conn.commit()

# Функция, позволяющая изменить данные о клиенте

def update_client(name, lastname, email, id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client SET name=%s, lastname=%s, e_mail=%s
            WHERE id=%s;
            """, (name, lastname, email, id))
        cur.execute("""
            SELECT * FROM client
            WHERE id=%s;
            """, (id,))
        print(cur.fetchone())
    conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента

def delete_number(name, lastname, phone):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM client WHERE name=%s AND lastname=%s ;
            """, (name, lastname))
        client_id = cur.fetchone()
        if client_id is None:
            print('Такого клиента не обнаружено')
        else:
            cur.execute("""
            DELETE FROM phone_number WHERE client_id=%s AND phone_number=%s;
            """, (client_id, phone))
    conn.commit()

# Функция, позволяющая удалить существующего клиента

def delete_client(name, lastname):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM client WHERE name=%s AND lastname=%s ;
            """, (name, lastname))
        client_id = cur.fetchone()
        if client_id is None:
            print('Такого клиента не обнаружено')
        else:
            cur.execute("""
                DELETE FROM phone_number WHERE client_id=%s;
                """, (client_id))
            cur.execute("""
            DELETE FROM client WHERE id=%s;
            """, client_id)
    conn.commit()

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)

def search_client(parametr):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT name, lastname, e_mail, phone_number FROM client c
            join phone_number p on p.client_id=c.id
            WHERE name=%s OR lastname=%s OR e_mail=%s OR phone_number=%s;
            """,(parametr,parametr, parametr, parametr))
        client_inform = cur.fetchall()
        if client_inform == []:
            print('Такого слиента в базе нет')
        else:
            print(client_inform)
    conn.commit()




conn = psycopg2.connect(database='client_netology', user='postgres', password='postmetal34@')

#нужно cursor не прописывать в каждой функции,
#а прописать его здесь и потом передавать в функцию как параметр
# также, надо поэкспериментировать с классами

create_table()

put_client('Name#1', 'Lastname#1', 'email#1@gmail.com')
put_client('Name#2', 'Lastname#2', 'email#2@gmail.com') #позже сделать проверку на существование клиента
put_client('Name#3', 'Lastname#3', 'email#3@gmail.com')

put_number('Name#1', 'Lastname#1', '89998887766')# позже сделать проверку на уникальность номера
put_number('Name#2', 'Lastname#2', '89998886655')
put_number('Name#3', 'Lastname#3', '89998885544')

# update_client('Name4', 'Lastname4', 'email#4@gmail.com', 1)

# delete_number('Name#2', 'Lastname#2', '89998886655') # позже создать проверку на наличие данного телефона

# delete_client('Name2', 'Lastname#2')

# search_client('Lastname#1')
conn.close()
# разработать код работы функций
