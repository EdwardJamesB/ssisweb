from app.extensions import db

class Colleges(object):
    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

    @staticmethod
    def all(keyword='', sort_order='asc'):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)

        # Validate sort_order
        sort_order = sort_order.upper()
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'ASC'

        query = """
            SELECT id, code, name FROM college
            WHERE name LIKE %s OR code LIKE %s
            ORDER BY code {}
        """.format('ASC' if sort_order.lower() == 'asc' else 'DESC')
        wildcard_keyword = f"%{keyword}%"
        cursor.execute(query, (wildcard_keyword, wildcard_keyword))
        return cursor.fetchall()

    def add(self):
        conn = db.connection
        cursor = conn.cursor()
        query = "INSERT INTO college (code, name) VALUES (%s, %s)"
        cursor.execute(query, (self.code, self.name))
        conn.commit()
        cursor.close()

    @staticmethod
    def edit(id):
        conn = db.connection
        cursor = conn.cursor()
        query = "SELECT * FROM college WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def update(id, code, name):
        conn = db.connection
        cursor = conn.cursor()
        query = "UPDATE college SET code = %s, name = %s WHERE id = %s"
        cursor.execute(query, (code, name, id))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete(id):
        conn = db.connection
        cursor = conn.cursor()
        query = "DELETE FROM college WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
