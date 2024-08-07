from app import db

class Colleges(object):
    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

    def all(keyword):
        cursor = db.cursor()
        query = f"SELECT * FROM colleges WHERE name LIKE '%{keyword}%' OR code LIKE '%{keyword}%'"
        cursor.execute(query)

        return cursor.fetchall()

    def add(self):
        cursor = db.cursor()
        query = f"INSERT INTO colleges (code, name) VALUES ('{self.code}', '{self.name}')"
        cursor.execute(query)
        db.commit()

    def edit(id):
        cursor = db.cursor()
        query = f"SELECT * FROM colleges WHERE id = {id}"
        cursor.execute(query)

        return cursor.fetchone()

    def update(id, code, name):
        cursor = db.cursor()
        query = f"UPDATE colleges SET code = '{code}', name = '{name}' WHERE id = {id}"
        cursor.execute(query)
        db.commit()

    def delete(id):
        cursor = db.cursor()
        query = f"DELETE from colleges WHERE id = {id}"
        cursor.execute(query)
        db.commit()