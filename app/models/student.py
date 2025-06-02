from app.extensions import db

class Students:
    def __init__(self, student_id=None, firstname=None, lastname=None, gender=None, course=None, year=None, image_url=None):
        self.student_id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.course = course
        self.year = year
        self.image_url = image_url

    @staticmethod
    def all(keyword='', sort_order='asc', sort_by='student_id'):
        conn = db.connection
        cursor = conn.cursor()
        wildcard = f"%{keyword}%"

        # Validate sort_by and sort_order to prevent SQL injection
        valid_sort_columns = {
            'student_id': 'student.student_id',
            'firstname': 'student.firstname',
            'lastname': 'student.lastname',
            'course': 'course.name',
            'year': 'student.year'
        }
        sort_column = valid_sort_columns.get(sort_by, 'student.student_id')
        sort_order = 'ASC' if sort_order == 'asc' else 'DESC'

        query = f"""
            SELECT student.student_id, student.firstname, student.lastname, course.name AS course_name, student.year, student.gender, student.image_url
            FROM student
            LEFT JOIN course ON student.course = course.code
            WHERE student.student_id LIKE %s
            OR student.firstname LIKE %s
            OR student.lastname LIKE %s
            OR course.name LIKE %s
            OR student.year LIKE %s
            ORDER BY {sort_column} {sort_order}
        """
        cursor.execute(query, (wildcard, wildcard, wildcard, wildcard, wildcard))
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            INSERT INTO student (student_id, firstname, lastname, gender, course, year, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.student_id, self.firstname, self.lastname, self.gender, self.course, self.year, self.image_url))
        db.connection.commit()

    @staticmethod
    def edit(student_id):
        conn = db.connection
        cursor = conn.cursor()
        query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    @staticmethod
    def update(student_id, firstname, lastname, gender, course, year, image_url):
        conn = db.connection
        cursor = conn.cursor()
        query = """
            UPDATE student
            SET firstname = %s, lastname = %s, gender = %s, course = %s, year = %s, image_url = %s
            WHERE student_id = %s
        """
        cursor.execute(query, (firstname, lastname, gender, course, year, image_url, student_id))
        conn.commit()

    @staticmethod
    def delete(student_id):
        conn = db.connection
        cursor = conn.cursor()
        query = "DELETE FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        db.connection.commit()
