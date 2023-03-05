from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask import flash


@app.route('/recipes/<int:id>/view')
def one_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    user_data = {
        'id':session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    one_recipe = Recipe.get_one(data)
    return render_template("view.html", one_recipe=one_recipe,logged_user=logged_user)


@app.route('/recipe/new')
def recipe_new():
    if "user_id" not in session:
        return redirect('/')
    return render_template("create.html")


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if "user_id" not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipe/new')
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(recipe_data)
    return redirect('/dashboard')

@app.route("/recipes/<int:id>/edit")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    this_recipe = Recipe.get_one(data)
    return render_template("edit.html", this_recipe=this_recipe)

@app.route("/recipes/<int:id>/update", methods=['POST'])
def update_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    data = {
        'id':id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_30': request.form['under_30'],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Recipe.delete(data)
    return redirect('/dashboard')
