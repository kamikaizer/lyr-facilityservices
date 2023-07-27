import functools

from flask import (
    Blueprint, flash,jsonify, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
# from flaskr.db import get_db
import hashlib




auth = Blueprint('auth', __name__)

# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template('auth/register.html')

# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('index'))

#         flash(error)

#     return render_template('auth/login.html')

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encripta la contraseña ingresada para compararla con la almacenada en la base de datos
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='prueba'
        )
        # Verifica las credenciales en la base de datos
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
        user = cursor.fetchone()
        current_app.logger.debug(user)
        

        if user:
            session['username'] = username
            session['nombre'] = user[4]+" "+user[5]
            session['fecha'] = user[8]
            session['cargo'] = user[9]
            current_app.logger.debug(session['nombre'])


            

            return redirect('/dashboard')
        else:
            error = 'Usuario o contraseña incorrectos.'
            return render_template('/login.html', error=error)

    return render_template('/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        current_app.logger.debug(request)
        name = request.form['name']
        apellido = request.form['apellido']
        cargo = request.form['cargo']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha = request.form['fecha']

        role = 'user'  # Por defecto, todos los usuarios se registran como 'user'
        password = name+"."+apellido
        username = password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='prueba'
        )
        # Verifica si el usuario maestro ya existe
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE role='master'")
        master_user = cursor.fetchone()

        if master_user:
            role = 'user'  # Si el usuario maestro existe, registra nuevos usuarios como 'user'
        else:
            role = 'master'  # Si el usuario maestro no existe, registra el nuevo usuario como 'master'

        # Inserta el nuevo usuario en la base de datos
        
        cursor.execute("""INSERT INTO users (username, password, role,nombre, apellido, correo, telefono,fecha,cargo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (username, hashed_password, role,name,apellido,correo,telefono,fecha,cargo))
        db.commit()
        cursor.close()

        return jsonify('success')

@auth.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('/auth/dashboard.html')
    else:
        return redirect('/login')

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')