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
        try:
            query = "INSERT INTO course (code, name, college) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.code, self.name, self.college))
            conn.commit()
            print("[DEBUG] Course added successfully")
        except Exception as e:
            print("[ERROR] Failed to add course:", e)

    @staticmethod
    def all(keyword='', sort_order='asc', sort_by='code'):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        wildcard = f"%{keyword}%"

        # Validate inputs
        if sort_by not in ['code', 'name', 'college_name']:
            sort_by = 'code'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        query = f"""
            SELECT course.id, course.code, course.name, college.name AS college_name
            FROM course
            LEFT JOIN college ON course.college = college.id
            WHERE course.code LIKE %s OR course.name LIKE %s OR college.name LIKE %s
            ORDER BY {sort_by} {sort_order}
        """
        cursor.execute(query, (wildcard, wildcard, wildcard))
        return cursor.fetchall()

    @staticmethod
    def get(code):
        conn = db.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM course WHERE code = %s"
        cursor.execute(query, (code,))
        return cursor.fetchone()

    @staticmethod
    def update(original_code, new_code, name, college):
        conn = db.connection
        cursor = conn.cursor()
        query = "UPDATE course SET code = %s, name = %s, college = %s WHERE code = %s"
        cursor.execute(query, (new_code, name, college, original_code))
        conn.commit()

    @staticmethod
    def delete(id):
        conn = db.connection
        cursor = conn.cursor()
        query = "DELETE FROM course WHERE code = %s"
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
