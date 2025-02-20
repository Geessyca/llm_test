import mysql.connector

class Database:
    def __init__ (self, host, user, password, database, port):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port
        }

    def connect_db(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            raise (f"Erro ao conectar: {err}")

    def insert_data(self, question, answer):
        feedback=None
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO qa (question, answer, feedback) VALUES (%s, %s, %s)"
                cursor.execute(sql, (question, answer, feedback))
                conn.commit()
                inserted_id = cursor.lastrowid  
                cursor.close()
                conn.close()
                return inserted_id
        except mysql.connector.Error as err:
            raise f"Erro ao conectar: {err}"
        
        
        
    def update_feedback(self, code_id, feedback = None):
        feedback_dict={
            True:"positivo",
            False:"negativo"
        }
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            feedback_enum = feedback_dict.get(feedback, None)
            sql = "UPDATE qa SET feedback = %s WHERE id = %s"
            cursor.execute(sql, (feedback_enum, code_id))
            conn.commit()
            cursor.close()
            conn.close()
            return(f"Feedback atualizado para '{feedback_enum}' no ID {code_id}")

    def fetch_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM qa")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            cursor.close()
            conn.close()
