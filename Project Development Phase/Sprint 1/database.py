import ibm_db

import db_conn

db2 = db_conn.DbConn()

class Database:

    def __init__(self):
        self.conn = db2.connect()
        create_query = """CREATE TABLE  IF NOT EXISTS "GSN72184"."CREDENTIALS"(
                        User_ID INTEGER NOT NULL,
                        first_name CHAR(20),
                        last_name CHAR(20),
                        email VARCHAR(200),
                        pwd VARCHAR(20),
                        PRIMARY KEY(User_ID)
                        )"""
        stmt = ibm_db.prepare(self.conn,create_query)
        result=ibm_db.execute(stmt)

    def insert(self,uid,fname,lname,email,pwd):
        
        obj = Database()
        insert_query = f"""insert  into "GSN72184"."CREDENTIALS" values('{uid}','{fname}','{lname}','{email}','{pwd}')"""
        insert_table = ibm_db.exec_immediate(self.conn,insert_query)
        obj.user_table(fname+str(uid))
        print("Inserted Successfull")

    def length_view(self):
        length_query = ibm_db.exec_immediate(self.conn,'SELECT COUNT(*) FROM "GSN72184"."CREDENTIALS"')
        length = ibm_db.fetch_tuple(length_query)[0]
        
        return length
    
    def view(self,email):

        view_query = f"""SELECT email FROM "GSN72184"."CREDENTIALS" WHERE email = '{email}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        result = ibm_db.fetch_row(view_db)

        return result
        
    def lg_view(self,email,pwd):
        view_query = f"""SELECT email,pwd  FROM "GSN72184"."CREDENTIALS" WHERE email = '{email}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        result = ibm_db.fetch_tuple(view_db)

        return result
    
    def user_table(self,user_name):
        create_query = f"""CREATE TABLE  IF NOT EXISTS "GSN72184"."{user_name}"(
                        User_ID INTEGER ,
                        Expense_Amt INTEGER,
                        Expense_name VARCHAR(200),
                        Expense_Date DATE,
                        CONSTRAINT FK_PersonOrder FOREIGN KEY (User_ID)
                        REFERENCES "GSN72184"."CREDENTIALS"(User_ID)
                        )"""
        stmt = ibm_db.prepare(self.conn,create_query)
        result=ibm_db.execute(stmt)