import os
import pymysql

DB_NAME = os.getenv('DB_NAME', 'mksu_clearance')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
cur = conn.cursor()
cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
conn.commit()
print(f"MySQL database '{DB_NAME}' ready at {DB_HOST}:{DB_PORT}")
