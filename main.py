import psycopg2 as ps

connectDB = ps.connect(
    dbname="studentdb",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
print(connectDB)



