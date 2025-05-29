from app.extensions import db

class Courses:
    @staticmethod
    def all():
        query = "SELECT code, name FROM course"
        cursor = db.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
