import psycopg2

try:
    conn = psycopg2.connect(
        dbname="tourism_project",
        user="capstone_user",
        password="hyn1419",
        host="localhost",
        port="5432"
    )
    print(" Database connection successful!")
except Exception as e:
    print(" Error connecting to database:", e)



