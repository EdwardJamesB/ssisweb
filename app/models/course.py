from app import db

class Courses:
    def __init__(self, id=None, code=None, name=None, college=None):
        self.id = id
        self.code = code
        self.name = name
        self.college = college

    def add(self):
        conn = db.connection
        cursor = conn.cursor()
        query = "INSERT INTO course (code, name, college) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.code, self.name, self.college))
        conn.commit()

    @staticmethod
    def all(keyword=''):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        wildcard = f"%{keyword}%"
        query = """
            SELECT course.id, course.code, course.name, college.name AS college_name
            FROM course
            LEFT JOIN college ON course.college = college.code
            WHERE course.code LIKE %s OR course.name LIKE %s
            ORDER BY course.code ASC
        """
        cursor.execute(query, (wildcard, wildcard))
        return cursor.fetchall()

    @staticmethod
    def get(id):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM course WHERE id = %s"
        cursor.execute(query, (id,))
        return cursor.fetchone()

    @staticmethod
    def update(id, code, name, college):
        conn = db.connection
        cursor = conn.cursor()
        query = "UPDATE course SET code = %s, name = %s, college = %s WHERE id = %s"
        cursor.execute(query, (code, name, college, id))
        conn.commit()

    @staticmethod
    def delete(id):
        conn = db.connection
        cursor = conn.cursor()
        query = "DELETE FROM course WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

    @staticmethod
    def exists(code):
        conn = db.connection
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM course WHERE code = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        return result[0] > 0

