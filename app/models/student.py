from app.extensions import db

class Students:
    def __init__(self, student_id=None, firstname=None, lastname=None, gender=None, course=None, year=None):
        self.student_id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.course = course
        self.year = year

    @staticmethod
    def all(keyword='', sort_order='asc'):
        query = f"""
            SELECT student.student_id, student.firstname, student.lastname, student.gender,
                course.name AS course_name, student.year
            FROM student
            LEFT JOIN course ON student.course = course.code  -- or course.id if you're using numeric FK
            WHERE student.student_id LIKE %s OR student.firstname LIKE %s OR student.lastname LIKE %s
            ORDER BY student.student_id {'ASC' if sort_order.lower() == 'asc' else 'DESC'}
        """

        wildcard_keyword = f"%{keyword}%"
        cursor = db.connection.cursor()
        cursor.execute(query, (wildcard_keyword, wildcard_keyword, wildcard_keyword))
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            INSERT INTO student (student_id, firstname, lastname, gender, course, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.student_id, self.firstname, self.lastname, self.gender, self.course, self.year))
        db.connection.commit()

    @staticmethod
    def edit(student_id):
        conn = db.connection
        cursor = conn.cursor()
        query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    @staticmethod
    def update(student_id, firstname, lastname, gender, course, year):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            UPDATE student
            SET firstname = %s, lastname = %s, gender = %s, course = %s, year = %s
            WHERE student_id = %s
        """
        cursor.execute(query, (firstname, lastname, gender, course, year, student_id))
        db.connection.commit()

    @staticmethod
    def delete(student_id):
        conn = db.connection
        cursor = conn.cursor()
        query = "DELETE FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        db.connection.commit()
