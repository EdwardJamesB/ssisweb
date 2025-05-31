from flask import render_template, request, redirect, url_for
from . import course
from app.controller.courses.forms import CourseForm
from app.controller.courses.forms import DeleteCourseForm
import app.models.course as CourseModel
import app.models.college as CollegeModel

# Show list of courses
@course.route('/', endpoint='index')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort')

    if not sort_order:
        sort_order = 'asc'

    courses = CourseModel.Courses.all(keyword, sort_order)
    return render_template('course/course.html', courses=courses, sort_order=sort_order)

# Create course
@course.route('/create', methods=['GET', 'POST'])
def create():
    form = CourseForm()
    colleges = CollegeModel.Colleges.all()
    form.college.choices = [(c['id'], c['name']) for c in colleges]

    if request.method == 'POST':
        print("[DEBUG] Form submitted")
        print("Form data:", request.form)
        print("Form errors:", form.errors)

        if form.validate():
            print("[DEBUG] Form validated ✅")
            if CourseModel.Courses.exists(form.code.data):
                print("[DEBUG] Course already exists ❌")
                error = "Course code already exists!"
                return render_template('course/create.html', form=form, error=error)

            course = CourseModel.Courses(
                code=form.code.data,
                name=form.name.data,
                college=form.college.data
            )
            print("[DEBUG] Adding course:", course.code, course.name, course.college)
            course.add()
            return redirect(url_for('.index'))
        
        print("[DEBUG] Submitted college value:", form.college.data)

    return render_template('course/create.html', form=form)

# Edit course
@course.route('/edit/<string:code>', methods=['GET'])
def edit(code):
    course = CourseModel.Courses.get(code)
    if not course:
        return redirect(url_for('.index'))

    colleges = CollegeModel.Colleges.all()
    return render_template('course/edit.html', data=(course['code'], course['name'], course['college']), colleges=CollegeModel.Colleges.all())

# Update course
@course.route('/update', methods=['POST'])
def update():
    original_code = request.form['original_code']
    new_code = request.form['code']
    name = request.form['name']
    college = request.form['college']

    CourseModel.Courses.update(original_code, new_code, name, college)
    print("Course updated successfully")
    return redirect(url_for('.index'))


# Delete course
@course.route('/delete', methods=['POST'])
def delete():
    form = DeleteCourseForm()

    if form.validate_on_submit():
        CourseModel.Courses.delete(form.code.data)
        return redirect(url_for('.index'))

    return "Invalid delete request", 400
