from flask import render_template, request, redirect, url_for
from . import course
from app.controller.courses.forms import CourseForm
import app.models.course as CourseModel
import app.models.college as CollegeModel

# Show list of courses
@course.route('/', endpoint='index')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort', 'asc')
    courses = CourseModel.Courses.all(keyword, sort_order)
    return render_template('course/course.html', courses=courses, sort_order=sort_order)

# Create course
@course.route('/create', methods=['GET', 'POST'])
def create():
    form = CourseForm()
    colleges = CollegeModel.Colleges.all()
    form.college.choices = [(c['code'], c['name']) for c in colleges]

    if request.method == 'POST' and form.validate():
        if CourseModel.Courses.exists(form.code.data):
            error = "Course code already exists!"
            return render_template('course/create.html', form=form, error=error)

        course = CourseModel.Courses(
            code=form.code.data,
            name=form.name.data,
            college=form.college.data
        )
        course.add()
        return redirect(url_for('.index'))

    return render_template('course/create.html', form=form)

# Edit course
@course.route('/edit/<string:code>', methods=['GET'])
def edit(code):
    course = CourseModel.Courses.get(code)
    if not course:
        return redirect(url_for('.index'))
    return render_template('course/edit.html', data=course)

# Update course
@course.route('/update/<string:code>', methods=['POST'])
def update(code):
    name = request.form['name']
    college = request.form['college']
    CourseModel.Courses.update(code, name, college)
    return redirect(url_for('.index'))

# Delete course
@course.route('/delete', methods=['POST'])
def delete():
    code = request.form['code']
    CourseModel.Courses.delete(code)
    return redirect(url_for('.index'))
