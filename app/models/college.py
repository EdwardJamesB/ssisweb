from app.extensions import db

class Colleges(object):
    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

    @staticmethod
    def all(keyword='', sort_order='asc', sort_by='code'):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        wildcard = f"%{keyword}%"

        if sort_by not in ['code', 'name']:
            sort_by = 'code'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        query = f"""
            SELECT id, code, name
            FROM college
            WHERE code LIKE %s OR name LIKE %s
            ORDER BY {sort_by} {sort_order}
        """
        cursor.execute(query, (wildcard, wildcard))
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

    @staticmethod
    def exists(code):
        conn = db.connection
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM college WHERE code = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0
