from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#Inicializa el blueprint
auth = Blueprint('auth', __name__)

#Crea la ruta para el inicio de sesion
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #Verifica que haya un metodo POST
        #obtiene los datos ingresados en el formulario
        email = request.form.get('email') 
        password = request.form.get('password')

        #Hace una consulta a la base de datos para verificar que el email ingresado exista
        user = User.query.filter_by(email=email).first()
        # si el email esta registrado se verifica que la contraseña sea correcta
        if user:
            if check_password_hash(user.password, password):
                flash('Sesion iniciada exitosamente!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            #si la contraseña no es correcta se avisa con un mensaje flash
            else:
                flash('Contraseña incorrecta, intentelo de nuevo.', category='error')
        #si el email no esta registrado se avisa con un mensaje flash
        else:
            flash('El correo electronico no existe.', category='error')

    #retorna el login renderizado al navegador
    return render_template("login.html", user=current_user)

#ruta para cerrar sesion
@auth.route('logout')
@login_required
def logout():
    logout_user()
    #redirecciona a iniciar sesion
    return redirect(url_for('auth.login'))

#ruta para el registro de un usuario
@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        #obtiene los datos ingresados en el formulario
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        cellphone = request.form.get('cellphone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #hace una consulta para verificar que el usuario no exista
        user = User.query.filter_by(email=email).first()
        #si el usuario ya existe muestra el mensaje
        if user:
            flash('El correo ya existe.', category='error')
        #mensajes para indicar la forma correcta que debe tener la informacion ingresada en el formulario
        elif len(email) < 4:
            flash('El correo debe tener mas de 4 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('Ingrese el primer nombre.', category='error')
        elif len(last_name) < 2:
            flash('Ingrese el primer apellido.', category='error')
        elif len(cellphone) < 10:
            flash('El telefono celular debe tener al menos 10 digitos.', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden.', category='error')
        elif len(password1) < 7:
            flash('La contraseña debe tener al menos 7 caracteres.', category='error')
        else:
            # añade el nuevo usuario a la base de datos y muestra un mensaje de cuenta creada
            new_user = User(email=email, first_name=first_name, last_name=last_name, cellphone=cellphone, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()   
            login_user(new_user, remember=True)         
            flash('Cuenta creada!', category='success')
            return redirect(url_for('views.home'))

    #renderiza la pagina de registro
    return render_template("sign_up.html", user=current_user)


