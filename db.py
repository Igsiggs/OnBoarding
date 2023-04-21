import sqlite3
import json

class Db():

    def __init__(self, path):
        self.path=path
        self.db=sqlite3.connect(path, check_same_thread=False, timeout=10)
        self.cursor=self.db.cursor()
        self.commit=self.db.commit()
        self.fetchone=self.cursor.fetchone()

    def get_node(self, id=None):
        query = f"SELECT * FROM NODES WHERE ID={id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return []
        tmp = []
        for rec in result:
            tmp.append({'id':rec[0], 'text':rec[1], 'name':rec[2], 'count_in_row':rec[3]})
        # print(type(tmp))
        return tmp


    def write_user(self, tg_name=None, id_last_connections=None, role=None, user_answer=None):
        self.cursor.execute(f"INSERT INTO USERS (TG_NAME, ID_LAST_CONNECTIONS, ROLE) VALUES ('{tg_name}', {id_last_connections}, '{role}')")
        self.cursor.execute(f"INSERT INTO USER_ANSWER (ID_USER) VALUES ('{tg_name}')")
        self.db.commit()


    def update_user(self, tg_name=None, id_last_connections=None, role=None, user_answer=None):
        a = "UPDATE USERS SET"
        query = []
        if id_last_connections:
            query.append(f" ID_LAST_CONNECTIONS = {id_last_connections} ")
        if role:
            query.append(f" ROLE = {role} ")

        a = a + ','.join(query) + f' WHERE TG_NAME={tg_name}'
        # print(a)
        db.cursor.execute(a)
        self.db.commit()


    def get_user(self, tg_name=None, id_last_connections=None, role=None):
        query = "SELECT * FROM USERS WHERE "
        clauses = []

        if tg_name:
            clauses.append(f" TG_NAME='{tg_name}' ")

        if id_last_connections:
            clauses.append(f" ID_LAST_CONNECTIONS='{id_last_connections}' ")

        if role:
            clauses.append(f" ROLE={role} ")

        query = query + ' AND '.join(clauses)
        # print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return []
        tmp = []
        for rec in result:
            tmp.append({'id':rec[0], 'tg_name':rec[1], 'id_last_connections':rec[2], 'role':rec[3]})
        return tmp


    def get_connections(self, id_in=None, id_out=None, role=None, reverse=None):
        query = "SELECT * FROM CONNECTIONS WHERE "
        clauses = []
        if id_in:
            clauses.append(f" ID_INCOM={id_in} ")
        if id_out:
            clauses.append(f" ID_OUTGO={id_out} ")
        if role:
            clauses.append(f" ROLE={role} ")
        if reverse:
            clauses.append(" REVERS=0 ")
        query = query + ' AND '.join(clauses)
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return []
        tmp = []
        for rec in result:
            tmp.append({'id':rec[0], 'id_outgo':rec[1], 'id_incom':rec[2], 'revers':rec[3],
                'name':rec[4], 'comments':rec[5], 'role':rec[6], 'new_role':rec[7], 'answer_user':rec[8], 'answer_true':rec[9]})
        return tmp


    def delete_user(self, tg_name):
        self.cursor.execute(f"DELETE FROM USERS WHERE TG_NAME={tg_name}")
        self.db.commit()

    def get_photo_pass(self, id_node, id_photo):
        loc = self.cursor.execute(f"SELECT * FROM NODES WHERE ID={id_node}")
        rec = self.cursor.fetchall()
        # print(rec)
        return [{f"{id_photo}": f"{rec[0][id_photo]}"}]

db = Db('Hakaton_db.db')
# print(db.get_connections(id_in=1))
# data = db.update_user('Jora', role=1)
# db.cursor.execute("SELECT PHOTO FROM NODES WHERE ID = 55")
# print(db.cursor.fetchall())
# print(json.loads(data[0]['name']))
