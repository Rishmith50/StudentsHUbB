import mysql.connector
from db_config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )


if __name__ == "__main__":
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Connected database:", cursor.fetchone()[0])
    cursor.close()
    connection.close()