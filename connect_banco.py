import mysql.connector


def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="empresas",
    )

    return conn
