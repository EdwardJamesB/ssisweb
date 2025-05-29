from flask import Blueprint, render_template, request, redirect, url_for
import app.models.student as StudentModel
from app.controller.students.forms import StudentForm

student = Blueprint('student', __name__, url_prefix='/student')

@student.route('/', methods=['GET'])
def index():
    keyword = request.args.get('keyword', default='', type=str)
    students = StudentModel.Student.all(keyword)
    return render_template('student/student.html', students=students)

@student.route('/create', methods=['GET', 'POST'])
def create():
    form = StudentForm(request.form)
    if request.method == 'POST' and form.validate():
        s = StudentModel.Student(
            student_id=form.student_id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            course=form.course.data,
            year=form.year.data,
            gender=form.gender.data
        )
        s.add()
        return redirect(url_for('student.index'))
    return render_template('student/create.html', form=form)

@student.route('/edit/<string:id>', methods=['GET'])
def edit(id):
    student = StudentModel.Student.edit(id)
    return render_template('student/edit.html', data=student)

@student.route('/update/<string:id>', methods=['POST'])
def update(id):
    StudentModel.Student.update(
        id,
        request.form['firstname'],
        request.form['lastname'],
        request.form['course'],
        request.form['year'],
        request.form['gender']
    )
    return redirect(url_for('student.index'))

@student.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    StudentModel.Student.delete(id)
    return redirect(url_for('student.index'))
