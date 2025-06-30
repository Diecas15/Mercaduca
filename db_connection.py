import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="MercaducaBD",
            user="postgres",
            password="12345",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
