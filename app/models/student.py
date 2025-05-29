from app.extensions import db

class Student:
    def __init__(self, student_id=None, firstname=None, lastname=None, course=None, year=None, gender=None):
        self.student_id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.gender = gender

    @staticmethod
    def all(keyword='', sort='asc'):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        query = f"""
            SELECT student.*, course.name AS course_name 
            FROM student
            LEFT JOIN course ON student.course = course.code
            WHERE student_id LIKE %s OR firstname LIKE %s OR lastname LIKE %s
            ORDER BY student_id {'ASC' if sort == 'asc' else 'DESC'}
        """
        wildcard = f"%{keyword}%"
        cursor.execute(query, (wildcard, wildcard, wildcard))
        return cursor.fetchall()

    def add(self):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            INSERT INTO student (student_id, firstname, lastname, course, year, gender)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.student_id, self.firstname, self.lastname, self.course, self.year, self.gender))
        db.connection.commit()

    @staticmethod
    def get(student_id):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        return cursor.fetchone()

    @staticmethod
    def update(student_id, firstname, lastname, course, year, gender):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            UPDATE student
            SET firstname = %s, lastname = %s, course = %s, year = %s, gender = %s
            WHERE student_id = %s
        """
        cursor.execute(query, (firstname, lastname, course, year, gender, student_id))
        db.connection.commit()

    @staticmethod
    def delete(student_id):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        db.connection.commit()