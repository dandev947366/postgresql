import psycopg2 as ps
from psycopg2 import sql, errors, DatabaseError

def connect_db():
    """Function to connect to the PostgreSQL database."""
    try:
        conn = ps.connect(
            dbname="studentdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        print("Connection to the database established successfully")
        return conn
    except (Exception, ps.DatabaseError) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None       
        
def create_student_table():
    """Function to create the students table in the database."""
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS students ("
                    "student_id SERIAL PRIMARY KEY, "
                    "name TEXT, "
                    "address TEXT, "
                    "age INT, "
                    "number TEXT);")
        conn.commit()
        print("Student table created successfully")
    except (Exception, ps.DatabaseError) as error:
        print(f"Error while creating PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def insert_data():
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        
        # Parameterized query to prevent SQL injection
        insert_query = """
            INSERT INTO students (name, address, age, number) 
            VALUES (%s, %s, %s, %s)
        """
        values = ('John', '123 Some Street', 23, '1234567890')

        cur.execute(insert_query, values)
        
        conn.commit()
        print("Data added successfully")
    except (Exception, DatabaseError) as error:
        print(f"Error while inserting data into PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
               
def insert_data_from_user():
    name = input("Enter name: ")
    address = input("Enter address: ")
    age = input("Enter age: ")
    number = input("Enter number: ")
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        
        insert_query = """
                INSERT INTO students (name, address, age, number) 
                VALUES (%s, %s, %s, %s)
            """
        values = (name, address, age, number)
        cur.execute(insert_query, values)
            
        conn.commit()
        print("Data added successfully")
    except (Exception, DatabaseError) as error:
        print(f"Error while inserting data into PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
            
def get_student_by_number(student_number):
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return None
        
        cur = conn.cursor()
        
        # Parameterized query to retrieve student by number
        query = """
            SELECT name, address, age, number
            FROM students
            WHERE number = %s
        """
        
        cur.execute(query, (student_number,))
        
        student = cur.fetchone()  # Fetch the first row
        
        if student:
            student_info = {
                'name': student[0],
                'address': student[1],
                'age': student[2],
                'number': student[3]
            }
            print(f"Student found with number {student_number}: {student_info}")
            return student_info
        else:
            print(f"No student found with number {student_number}")
            return None
        
    except (Exception, DatabaseError) as error:
        print(f"Error while fetching student from PostgreSQL: {error}")
        return None
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
            
def update_data():
    """Function to update student data in the students table."""
    student_number = input("Enter student number to update: ")
    name = input("Enter new name: ")
    address = input("Enter new address: ")
    age = input("Enter new age: ")
    number = input("Enter new number: ")
    
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        
        # Parameterized query to update student data
        update_query = """
            UPDATE students
            SET name = %s, address = %s, age = %s, number = %s
            WHERE number = %s
        """
        values = (name, address, age, number, student_number)
        
        cur.execute(update_query, values)
            
        conn.commit()
        print("Data updated successfully")
    except (Exception, DatabaseError) as error:
        print(f"Error while updating data in PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def update_fields():
    """Function to update specific fields of a student in the students table."""
    student_number = input("Enter student number to update: ")
    
    fields = {
        "1": ("name", "Enter new name: "),
        "2": ("address", "Enter new address: "),
        "3": ("age", "Enter new age: "),
    }

    print("Which field would you like to update?")
    for key in fields:
        print(f"{key}: {fields[key][0]}")

    field_choice = input("Enter the number corresponding to the field to update: ")
    
    if field_choice not in fields:
        print("Invalid choice")
        return
    
    field_name = fields[field_choice][0]
    prompt_message = fields[field_choice][1]
    new_value = input(prompt_message)

    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        
        # Construct the update query dynamically based on the selected field
        update_query = """
            UPDATE students
            SET {} = %s
            WHERE number = %s
        """.format(field_name)
        
        values = (new_value, student_number)
        
        cur.execute(update_query, values)
            
        conn.commit()
        print(f"{field_name.capitalize()} updated successfully")
    except (Exception, DatabaseError) as error:
        print(f"Error while updating data in PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def delete_data():
    student_number = input("Enter student number you want to delete: ")
    conn = None
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cur = conn.cursor()
        select_query = """
            SELECT * FROM students
            WHERE number = %s
        """
        
        cur.execute(select_query, (student_number,))
        student = cur.fetchone()
        if student:
            print(f"Student to be deleted: Name: {student[1]}, Address: {student[2]}, Age: {student[3]}, Number: {student[4]}")
            delete_query = """
                DELETE FROM students
                WHERE number = %s
            """
            cur.execute(delete_query, (student_number,))
            conn.commit()
            print(f"Student with number {student_number} deleted successfully")
        else:
            print(f"No student found with number {student_number}")
        
    except (Exception, DatabaseError) as error:
        print(f"Error while deleting data in PostgreSQL table: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    
    
# student_number = "4"
# student_info = get_student_by_number(student_number)
# if student_info:
#     print(f"Student Info: {student_info}")
# update_data()
# update_fields()
delete_data()