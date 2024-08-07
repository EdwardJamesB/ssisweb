from app.controller.colleges.forms import CollegeForm 
from flask import render_template, redirect, request, jsonify, url_for
from . import college
import app.models.college as CollegeModel

@college.route('/college')
def index():
    keyword = request.args.get('keyword', default='', type=str)
    colleges = CollegeModel.Colleges.all(keyword)
    
    return render_template("college/index.html", colleges=colleges)

@college.route("/college/create", methods=['POST', 'GET'])
def create():
    form = CollegeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        college = CollegeModel.Colleges(code=form.code.data, name=form.name.data)
        college.add()

        return redirect('/college')

    return render_template('college/create.html', form=form)

@college.route('/college/edit/<id>', methods=['GET'])
def edit(id):
    college = CollegeModel.Colleges.edit(id)

    return render_template('college/edit.html', data=college)

@college.route('/college/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        CollegeModel.Colleges.update(id, code, name)

        return redirect(url_for('.index'))

@college.route('/college/delete', methods=['POST'])
def delete():
    id = request.form['id']

    if id:
        try:
            CollegeModel.Colleges.delete(id)

            return jsonify(success=True, message="Successful")
        except:
            return jsonify(success=False, message="College is referenced in Courses table")

    return jsonify(success=False, message="Failed")