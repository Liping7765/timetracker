import mysql.connector
import streamlit as st


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**st.secrets["mysql"])

    def run_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


    def create_table(self):
        SQL = """
                CREATE TABLE IF NOT EXISTS timecards (
                    timecard_id INT AUTO_INCREMENT PRIMARY KEY,
                    catagory VARCHAR(255) NOT NULL,
                    start_time DECIMAL(20,8) NOT NULL,
                    end_time DECIMAL(20,8) NOT NULL,
                    record_created_at datetime default current_timestamp
                );
            """
        self.run_query(SQL)
        self.conn.commit()

    # get all records from table for demo 
    def get_all(self):
        sql = "SELECT * from timecards;"
        return self.run_query(sql)

    # get records by id 
    def get_by_id(self, id = 0):
        @st.experimental_memo(ttl=600)
        def inner(id = 0):
            sql = f"SELECT * from timecards where timecard_id = {id};"
            return self.run_query(sql)
        return inner(id)

    # get records by id 
    def filter_by_id(self, id = 0):
        def inner(id = 0):
            sql = f"SELECT * from timecards where timecard_id >= {id};"
            return self.run_query(sql)
        return inner(id)

    # get records by grade
    # def filter_by_grade(self, grade = 1):
    #     def inner(grade = 1):
    #         sql = f"SELECT * from timecards where grade = {grade};"
    #         return self.run_query(sql)
    #     return inner(grade)



    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.  
    def add_record(self, catagory, start_time, end_time):
        @st.experimental_memo(ttl=600)
        def add(catagory, start_time, end_time):
            sql = ('INSERT INTO timecards(catagory, start_time, end_time)'
                        f' VALUES ( "{catagory}", {start_time}, {end_time})')
            self.run_query(sql)
            self.conn.commit()
        return add(catagory, start_time, end_time)
        
    def update_record_with_id(self, id, field, value):
        #validation check to ensure id exists 
        rows = self.get_by_id(id)
        st.write(rows)
        if not len(rows):
            st.write("data doesnot exist")
            return 

        @st.experimental_memo(ttl=600)
        def update(id, field, value):
            sql = f'UPDATE students SET {field} = {value} WHERE student_id = {id}'

            if field in ("firstname", "lastname"):
                sql = f'UPDATE students SET {field} = "{value}" WHERE student_id = {id}'

            self.run_query(sql)
            self.conn.commit()
        return update(id, field, value)

    def delete_with_id(self, id):

        @st.experimental_memo(ttl=600)
        def delete(id):
            sql = f'Delete from students WHERE student_id = {id}'
            self.run_query(sql)
            self.conn.commit()

        return delete(id)
   





