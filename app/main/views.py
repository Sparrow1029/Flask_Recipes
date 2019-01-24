from flask import request, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.app import db
from app.models import Recipe, User
from app.main import blueprint as bp  # blueprint in module __init__.py
from app.utils import flash_errors
from .forms import LoginForm, SearchForm, RecipeForm, NewRecipeForm


def redirect_url(default='main.index'):
    return request.referrer or url_for(default)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Home page"""

    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    # search_names = Recipe.query.all()
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        search_recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=search_recipe.id))

    recipes = Recipe.query.order_by(Recipe.name).all()
    return render_template('index.html', search_names=search_names, recipes=recipes,
                           search_form=search_form)


@bp.route('/category/<head>_<category>', methods=['GET', 'POST'])
def category_view(category, head):

    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    #search_names = [recipe for recipe in db.session.query(Recipe).all()]
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        search_recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=search_recipe.id))

    recipes = Recipe.query.filter(Recipe.category==category).order_by(Recipe.name).all()
    prev_url = redirect_url()
    if any(w in prev_url for w in ['add','edit','del','log']):
        prev_url = url_for('main.index')

    return render_template('category.html', recipes=recipes, head=head,
                           prev_url=prev_url, search_form=search_form,
                           search_names=search_names)


@bp.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe_detail(recipe_id):
    #search
    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    #search_names = [recipe for recipe in db.session.query(Recipe).all()]
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        search_recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=search_recipe.id))

    form = RecipeForm()
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
    ingred = recipe.__dict__['ingred'].split('\n')  # format ingredients for template
    prev_url = redirect_url()
    if any(w in prev_url for w in ['add','edit','del','log']):
        prev_url = url_for('main.index')

    return render_template('recipe_detail.html', recipe=recipe, ingred=ingred,
                           form=form, prev_url=prev_url,
                           search_form=search_form, search_names=search_names)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('main.index'))

    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    #search_names = [recipe for recipe in db.session.query(Recipe).all()]
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=recipe.id))

    return render_template('login.html', form=form, search_form=search_form,
                           search_names=search_names)

@bp.route('/add_new', methods=['GET', 'POST'])
@login_required
def add_new_recipe():
    form = NewRecipeForm()

    if request.args.get('cancel_button') == "Cancel":
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        recipe = Recipe(name=form.name.data, desc=form.desc.data,
                        prep_time=form.prep_time.data, servings=form.servings.data,
                        cal_p_serving=form.cal_p_serving.data, ingred=form.ingred.data,
                        source=form.source.data, note=form.note.data,
                        type=form.type.data, date=form.date.data,
                        main_ingredient=form.main_ingredient.data,
                        category=form.category.data)
        db.session.add(recipe)
        db.session.commit()
        flash('New recipe added.')
        new_recipe_id = Recipe.query.order_by('-id').first()
        return redirect(url_for('main.recipe_detail',
                                recipe_id=new_recipe_id.id))

    #search_names = [recipe for recipe in db.session.query(Recipe).all()]
    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        search_recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=search_recipe.id))

    return render_template('add_new_recipe.html', form=form,
                           search_form=search_form, search_names=search_names)


@bp.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.filter(Recipe.id==recipe_id).first()

    form = RecipeForm(obj=recipe)

    if request.args.get('cancel_button') == "Cancel":
        # prev_url = redirect_url()
        return redirect(url_for('main.recipe_detail', recipe_id=recipe.id))

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.desc = form.desc.data
        recipe.prep_time = form.prep_time.data
        recipe.servings = form.servings.data
        recipe.cal_p_serving = form.cal_p_serving.data
        recipe.ingred = form.ingred.data
        recipe.source = form.source.data
        recipe.note = form.note.data
        recipe.type = form.type.data
        recipe.date = form.date.data
        recipe.main_ingredient = form.main_ingredient.data
        recipe.category = form.category.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.recipe_detail', recipe_id=recipe.id))

    elif request.method == 'GET':
        form.name.data = recipe.name
        form.desc.data = recipe.desc
        form.prep_time.data = recipe.prep_time
        form.servings.data = recipe.servings
        form.cal_p_serving.data = recipe.cal_p_serving
        form.ingred.data = recipe.ingred
        form.source.data = recipe.source
        form.note.data = recipe.note
        form.type.data = recipe.type
        form.date.data = recipe.date
        form.main_ingredient.data = recipe.main_ingredient
        form.category.data = recipe.category

    #search_names = [recipe for recipe in db.session.query(Recipe).all()]
    search_names = [row[0] for row in db.engine.execute("SELECT name FROM recipe;")]
    search_form = SearchForm()
    search = request.args.get('search')
    if search is not None:
        form_data = request.args.get('search')
        if form_data not in search_names:
            return redirect(redirect_url())
        search_recipe = Recipe.query.filter(Recipe.name==form_data).first()
        return redirect(url_for('main.recipe_detail', recipe_id=search_recipe.id))

    return render_template('edit_recipe.html', form=form,
                           search_form=search_form, search_names=search_names)

@bp.route('/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter(Recipe.id==recipe_id).first()
    db.session.delete(recipe)
    db.session.commit()
    flash(f"Recipe '{recipe.name}' Deleted.")
    return redirect(url_for('main.index'))

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
