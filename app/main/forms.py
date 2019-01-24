from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
        SelectField, TextAreaField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from datetime import datetime as dt
from app.models import Recipe, User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    search = StringField('search', render_kw={"placeholder":"Search"}, validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField('Recipe name', validators=[DataRequired()])
    desc = StringField('Description', description="i.e: Sauce, Entrée, Rub..",
                       validators=[DataRequired(), Length(min=0, max=64)])
    prep_time = StringField('Prep Time')
    servings = StringField('Number of Servings')
    cal_p_serving = StringField('Calories per Serving')
    ingred = TextAreaField('Ingredients', description="Place each ingredient on a\
                         new line", validators=[DataRequired()])
    source = StringField('Source')
    note = TextAreaField('Cooking Instructions', description="Detailed cooking\
                       instructions go here", validators=[DataRequired()])
    type = StringField('Nationality/Cuisine')
    date = StringField('Date added', default=dt.strftime(dt.now(), '%m/%d/%Y'))
    main_ingredient = StringField('Main Ingredient', validators=[Length(min=0,
                                                                       max=32)])
    category = SelectField('Category', choices=[('Main', 'Main'), ('Starter', 'Appetizer'),
                                                ('Other', 'Other'),
                                                ('Breakfast', 'Breakfast'),
                                                ('Dessert', 'Dessert'), ('Side', 'Side'),
                                                ('SoupSalad', 'Soup/Salad')])
    submit = SubmitField('Save Changes')

class NewRecipeForm(RecipeForm):
    """Same as RecipeForm, just with a different Submit button...
    probably not necessary."""
    submit = SubmitField('Add Recipe')
