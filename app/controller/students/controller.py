from flask import render_template, request, redirect, url_for
from . import student
from app.controller.students.forms import StudentForm
import app.models.student as StudentModel
import app.models.course as CourseModel
import app.models.college as CollegeModel
from app.cloudinary_config import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE_MB = 2

# Show list of students
@student.route('/', endpoint='index')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort', 'asc')
    sort_by = request.args.get('sort_by', 'student_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    offset = (page - 1) * per_page

    students = StudentModel.Students.all(keyword, sort_order, sort_by, limit=per_page, offset=offset)
    total = StudentModel.Students.count(keyword)
    total_pages = (total + per_page - 1) // per_page

    return render_template('student/student.html', students=students, sort_order=sort_order, sort_by=sort_by,
                           page=page, per_page=per_page, total=total, total_pages=total_pages, keyword=keyword)

# Create student
@student.route('/create', methods=['GET', 'POST'])
def create():
    form = StudentForm()

    # Populate dropdowns
    form.gender.choices = [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')]
    form.year.choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    form.course.choices = [("", "-- Please select a course --")] + [
        (c["code"], f'{c["code"]} - {c["name"]}') for c in CourseModel.Courses.all()
    ]

    if request.method == 'POST' and form.validate():
        image_url = None
        file = request.files.get('profile_pic')
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()

            if ext not in ALLOWED_EXTENSIONS:
                return "Invalid file type. Only PNG and JPG are allowed.", 400

            file.seek(0, 2)  # move to end
            size_mb = file.tell() / (1024 * 1024)
            file.seek(0)     # reset

            if size_mb > MAX_FILE_SIZE_MB:
                return f"File too large. Max allowed is {MAX_FILE_SIZE_MB}MB.", 400

            upload_result = cloudinary.uploader.upload(file, folder="students")
            image_url = upload_result.get('secure_url')

        elif request.form.get('remove_pic'):  # Checkbox for default
            image_url = None  # default avatar

        student = StudentModel.Students(
            student_id=form.student_id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            gender=form.gender.data,
            course=form.course.data,
            year=form.year.data,
            image_url=image_url
        )
        try:
            student.add()
            return redirect(url_for('.index'))
        except Exception as e:
            if "1062" in str(e) and "student.PRIMARY" in str(e):
                error = "Student ID already exists."
            else:
                error = "An unexpected error occurred."

            return render_template('student/create.html', form=form, error=error)

    return render_template('student/create.html', form=form)

# Edit student
@student.route('/edit/<string:student_id>', methods=['GET'])
def edit(student_id):
    student = StudentModel.Students.edit(student_id)
    if not student:
        return redirect(url_for('.index'))

    form = StudentForm()

    # 🟢 1. Set choices first
    form.gender.choices = [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')]
    form.year.choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    form.course.choices = [("", "-- Please select a course --")] + [
        (c["code"], f'{c["code"]} - {c["name"]}') for c in CourseModel.Courses.all()
    ]

    # 🟢 2. Now assign values AFTER defining choices
    form.student_id.data = student[0]
    form.firstname.data = student[1]
    form.lastname.data = student[2]
    form.gender.data = student[5]

    # Make sure these match values in choices exactly
    form.course.data = str(student[3]) if student[3] else ""
    form.year.data = str(student[4]) if student[4] else ""

    form.image_url.data = student[6]

    return render_template('student/edit.html', form=form, student_id=student_id)

@student.route('/update/<string:student_id>', methods=['POST'])
def update(student_id):
    form = StudentForm()

    # Repopulate choices
    form.course.choices = [("", "-- Please select a course --")] + [
    (c["code"], f'{c["code"]} - {c["name"]}') for c in CourseModel.Courses.all()
    ]
    form.year.choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')]
    
    # Get data
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    gender = request.form.get('gender')
    course = request.form.get('course')
    year = request.form.get('year')
    remove_pic = request.form.get('remove_pic')  # checkbox

    image_url = form.image_url.data  # current image

    file = request.files.get('profile_pic')
    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return "❌ Invalid file type. Only PNG and JPG are allowed.", 400

        file.seek(0, 2)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)

        if size_mb > MAX_FILE_SIZE_MB:
            return f"❌ File too large. Max allowed is {MAX_FILE_SIZE_MB}MB.", 400

        result = cloudinary.uploader.upload(file, folder="students")
        image_url = result.get('secure_url')
    elif remove_pic:  # checkbox checked
        image_url = None

    StudentModel.Students.update(
        student_id=student_id,
        firstname=firstname,
        lastname=lastname,
        gender=gender,
        course=course,
        year=year,
        image_url=image_url
    )

    return redirect(url_for('student.index'))

# Delete student
@student.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['student_id']
    StudentModel.Students.delete(student_id)
    return redirect(url_for('.index'))
