import os
from flask import Flask, flash, render_template, redirect, request, session
from wtforms.fields.simple import TextAreaField
from wtforms.widgets import CheckboxInput, ListWidget

from flask_app import model
import datetime
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import BooleanField, StringField, SelectMultipleField, PasswordField, SelectField, DateField, TimeField, IntegerField, EmailField, validators, FloatField, FieldList
from flask_session import Session
from functools import wraps
from flask_talisman import Talisman
import pyotp
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Talisman(app, content_security_policy={
    'default-src' : '\'none\'',
    'style-src': [ 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css' ],
    'img-src' : ['\'self\'', 'data:'],
    'script-src' : '\'none\''
  })
CSRFProtect(app)
Session(app)
QRcode(app)


def login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not 'user' in session:
      return redirect('/login')
    return func(*args, **kwargs)
  return wrapper


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

class IngredientForm(FlaskForm):
  name = StringField("name", validators=[validators.DataRequired()])


class PizzaForm(FlaskForm):
  name = StringField("name", validators=[validators.DataRequired()])
  price = FloatField("price", validators=[validators.DataRequired()])
  description = StringField(label="description")
  ingredients = SelectMultipleField('ingredients', coerce=int,
                                    widget=ListWidget(prefix_label=False),
                                    option_widget=CheckboxInput())


@app.route('/ingredient/', methods=['GET', 'POST'])
def ingredient():
  form = IngredientForm()
  connection = model.connect()
  var = request.args.get("success")
  if not var is None:
    if (var == '1'):
      flash("Modification réussie.", category="success")
      return redirect(request.path, code=302)
    else:
      flash("Erreur lors de la modification", category="danger")
      return redirect(request.path, code=302)
  if form.validate_on_submit():
    try:
      model.add_ingredient(connection=connection,name=form.name.data)
      flash("Ajout réussie.", category="success")
      return redirect(request.path, code=302)
    except Exception as e :
      flash("Erreur lors de l'ajout.", category="danger")
      app.log_exception(e)
  return render_template('ingredient.html', ingredients=model.ingredients(connection), pizzaiolo=session["user"]["pizzaiolo"], form=form)


@app.route('/pizza/<int:pizza_id>', methods=['GET'])
def pizza(pizza_id):
  connection = model.connect()
  return 'Pizza {0}'.format(pizza_id)

@app.route('/pizza', methods=['GET', 'POST'])
def pizza_list():
  form = PizzaForm()
  connection = model.connect()

  ingredients_list = model.ingredients(connection)

  # Créer les choix pour le champ ingredients
  form = PizzaForm()
  form.ingredients.choices = [(i['id'], i['name']) for i in ingredients_list]
  var = request.args.get("success")
  if not var is None:
    if (var == '1'):
      flash("Modification réussie.", category="success")
      return redirect(request.path, code=302)
    else:
      flash("Erreur lors de la modification", category="danger")
      return redirect(request.path, code=302)

  if form.validate_on_submit():
    try:
      # Ajouter la pizza
      model.add_pizza(
        connection=connection,
        name=form.name.data,
        price=form.price.data,
        description=form.description.data
      )
      pizza_id = model.get_last_id(connection=connection, table='pizzas')
      # Ajouter les ingrédients sélectionnés
      for ingredient_id in form.ingredients.data:
        model.add_pizza_ingredient(connection, pizza_id, ingredient_id)
      flash("Ajout réussie.", category="success")
      return redirect(request.path, code=302)
    except Exception as e :
      flash("Erreur lors de l'ajout.", category="danger")
      app.log_exception(e)
  return render_template('pizza.html',pizzas=model.pizzas(connection), ingredients=model.ingredients(connection), pizzaiolo=session["user"]["pizzaiolo"], form=form)

class LoginForm(FlaskForm):
  email = EmailField('email')
  username = StringField("username", validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired()])

class SigninForm(FlaskForm):
  email = EmailField("email", validators=[validators.DataRequired()])
  username = StringField("username", validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      user = model.get_user(connection, username=form.username.data, password=form.password.data)
      if model.totp_enabled(connection, user):
        session['totp_user'] = user
        return redirect('/totp')
      session['user'] = user
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('login.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  if 'user' in session:
    return redirect('/')
  form = SigninForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      model.add_user(connection, form.email.data, form.username.data, form.password.data)
      return redirect('/signin')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('inscription.html', form=form)


@app.route('/logout', methods = ['POST'])
@login_required
def logout():
  session.pop('user')
  flash('Déconnexion réussie !')
  return redirect('/')


class PasswordChangeForm(FlaskForm):
  old_password = PasswordField('old_password', validators=[validators.DataRequired()])
  new_password = PasswordField('new_password', validators=[validators.DataRequired(),
                                                           validators.EqualTo('password_confirm')])
  password_confirm = PasswordField('password_confirm', validators=[validators.DataRequired()])
  totp_enabled = BooleanField('totp_enabled')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = PasswordChangeForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      email = session['user']['email']
      model.change_password(connection, email, form.old_password.data, form.new_password.data)
      totp_secret = session['totp_secret'] if form.totp_enabled.data else None
      model.update_totp_secret(connection, session['user']['id'], totp_secret)
      flash('Mot de passe modifié !')
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  totp_secret = pyotp.random_base32()
  session['totp_secret'] = totp_secret
  totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
    name=session['user']['email'], issuer_name='Soccer')
  return render_template('change_password.html', form=form, totp_uri=totp_uri)


class UserCreationForm(FlaskForm):
  email = EmailField('email', validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired(),
                                                   validators.EqualTo('confirm')])
  confirm = PasswordField('confirm', validators=[validators.DataRequired()])


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
  form = UserCreationForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      model.add_user(connection, form.email.data, form.password.data)
      flash('Nouvel utilisateur créé !')
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('create_user.html', form=form)


class TotpForm(FlaskForm):
  totp = StringField('totp', validators=[
     validators.DataRequired(),
     validators.Length(min=6, max=6)])


@app.route('/totp', methods=['GET', 'POST'])
def totp():
  if 'totp_user' not in session:
    return redirect('/')
  user = session['totp_user']
  connection = model.connect()
  if not model.totp_enabled(connection, user):
    return redirect('/')
  form = TotpForm()
  if form.validate_on_submit():
    try:
      totp_secret = model.totp_secret(connection, user)
      totp_code = form.totp.data
      if pyotp.TOTP(totp_secret).verify(totp_code):
        session['user'] = user
        return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('totp.html', form=form)

@app.route('/delete_ingredient', methods=['GET'])
def delete_ingredient_route():
  try:
    ingredient_id = request.args.get("ingredient_id")
    connection = model.connect()
    model.delete_ingredient(connection, ingredient_id)
    return redirect('/ingredient?success=1')
  except Exception as e :
    return redirect('/ingredient?success=0')

@app.route('/delete_pizza', methods=['GET'])
def delete_pizza_route():
  try:
    pizza_id = request.args.get("pizza_id")
    connection = model.connect()
    model.delete_pizza(connection, pizza_id)
    return redirect('/pizza?success=1')
  except Exception as e :
    return redirect('/pizza?success=0')

@app.route('/availabilite', methods=['GET'])
def change_availabilite():
  try:
    ingredient_id = request.args.get("ingredient_id")
    value = request.args.get("value") == "True"
    connection = model.connect()
    model.change_ingredient_availabilite(connection, ingredient_id, value)
    return redirect('/ingredient?success=1')
  except Exception as e:
    return redirect('/ingredient?success=0')


@app.route('/edit_pizza/<int:pizza_id>', methods=['POST'])
def edit_pizza(pizza_id):
  if not session.get("user", {}).get("pizzaiolo"):
    flash("Accès non autorisé.", category="danger")
    return redirect("/pizza")

  try:
    connection = model.connect()

    # Récupérer les données du formulaire
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    ingredients = request.form.getlist('ingredients')  # Récupère tous les ingrédients cochés

    # Mettre à jour la pizza
    model.update_pizza(connection=connection, id=pizza_id, name=name, price=price, description=description)

    # Supprimer les anciens ingrédients
    model.delete_recette_pizza(connection=connection, id_pizza=pizza_id)

    # Ajouter les nouveaux ingrédients
    for ingredient_id in ingredients:
      model.add_pizza_ingredient(connection=connection, id_pizza=pizza_id, id_ingredient=ingredient_id)

    flash("Pizza modifiée avec succès.", category="success")

  except Exception as e:
    connection.rollback()
    app.log_exception(e)
    flash("Erreur lors de la modification de la pizza.", category="danger")

  return redirect("/pizza")


class SearchForm(FlaskForm):
  ingredient = SelectField('Ingrédient', coerce=int)


# Dans routes.py
@app.route('/search', methods=['GET', 'POST'])
def search():
  connection = model.connect()
  form = SearchForm()

  # Charger la liste des ingrédients pour le select
  ingredients = model.ingredients(connection)
  form.ingredient.choices = [(i['id'], i['name']) for i in ingredients]

  results = []
  if form.validate_on_submit():
    # Requête pour trouver les pizzas avec l'ingrédient sélectionné
    results = model.get_pizzas_from_ingredients(connection, form.ingredient.data)

  return render_template(
    'recherche.html',
    form=form,
    results=results
  )
