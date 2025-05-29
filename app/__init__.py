from flask import Flask, render_template
from app.extensions import db
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    # ✅ Initialize extensions AFTER app is defined
    bootstrap.init_app(app)
    db.init_app(app)
    CSRFProtect(app)

    # Register blueprints
    from app.controller.colleges import college as college_blueprint
    app.register_blueprint(college_blueprint, url_prefix="/college")
    
    from app.controller.students import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix="/student")

    from app.controller.courses import course as course_blueprint
    app.register_blueprint(course_blueprint, url_prefix="/course")

    @app.route("/")
    def layout():
        return render_template("layout.html")

    @app.route("/Course")
    def course():
        return render_template("/course/course.html")

    @app.route("/Student")
    def student():
        return render_template("/student/student.html")

    return app

    
