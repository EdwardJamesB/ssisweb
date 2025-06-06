from app.controller.colleges.forms import CollegeForm 
from flask import render_template, redirect, request, jsonify, url_for
from . import college
import app.models.college as CollegeModel
from app.controller.colleges.forms import CollegeForm, DeleteCollegeForm

@college.route('/', endpoint='index') 
def index():
    keyword = request.args.get('keyword', default='', type=str)
    sort_order = request.args.get('sort', 'asc')  # asc or desc
    sort_by = request.args.get('sort_by', 'code')  # code or name
    colleges = CollegeModel.Colleges.all(keyword, sort_order, sort_by)
    return render_template("college/college.html", colleges=colleges, sort_order=sort_order)

@college.route("/college/create", methods=['POST', 'GET'])
def create():
    form = CollegeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        if CollegeModel.Colleges.exists(form.code.data):
            error = "College code already exists!"
            return render_template('college/create.html', form=form, error=error)

        college = CollegeModel.Colleges(code=form.code.data, name=form.name.data)
        college.add()

        return redirect(url_for('college.index', sort='asc'))

    return render_template('college/create.html', form=form)

@college.route('/edit/<string:id>', methods=['GET'])
def edit(id):
    college = CollegeModel.Colleges.edit(id)

    return render_template('college/edit.html', data=college)

@college.route('/college/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        CollegeModel.Colleges.update(id, code, name)

        print("College updated successfully")
        return redirect(url_for('.index'))

@college.route('/delete', methods=['POST'])
def delete():
    form = DeleteCollegeForm()
    if form.validate_on_submit():
        CollegeModel.Colleges.delete(form.id.data)
        return redirect(url_for(".index"))
    return "Invalid delete request", 400