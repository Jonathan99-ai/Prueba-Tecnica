from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User


views = Blueprint('views', __name__)
#ruta para la pagina que muestra la informacion del usuario
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #si se hace un POST se actualizan los datos del usuario
    if request.method == 'POST':
        current_user.email = request.form['email']
        current_user.first_name = request.form['firstName']
        current_user.last_name = request.form['lastName']
        current_user.cellphone = request.form['cellphone']

        db.session.commit()
        flash('Informacion actualizada!', category='success')
    return render_template("home.html", user=current_user)

