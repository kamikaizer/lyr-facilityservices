import io
# import pyodbc
# from flask import make_response 
from flask import Blueprint, render_template, redirect,url_for,request,flash,jsonify,json,send_file,current_app
# from flask_ldap3_login import LDAP3LoginManager
# from flask_login import LoginManager,login_required, login_user, UserMixin, current_user, logout_user
# from flask_ldap3_login.forms import LDAPLoginForm
# from .models import *
#from . import conn,conn3
from datetime import *
# from .tiempos import *
# import os
# from datetime import datetime
# import pandas as pd
# from pandas.tseries.offsets import CustomBusinessDay

# def conn_():
#     conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=clloforense03p;'
#                       'Database=PBServforenses;'
#                       'UID=Support03;'
#                       "PWD=GajNH6t$'W{,:8R7;"
#                       'Trusted_Connection=no;')
    # return conn

import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd

url = 'mysql+mysqlconnector://root:root1234@localhost:3306/prueba'
engine = sqlalchemy.create_engine(url)


main = Blueprint('main', __name__)









class Equipment:
    def __init__(self, id, name, user_id=None, is_assigned=False):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.is_assigned = is_assigned

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50) NOT NULL,
            user_id INT,
            is_assigned BIT DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(50) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS change_requests (
            id INT IDENTITY(1,1) PRIMARY KEY,
            equipment_id INT NOT NULL,
            user_id INT NOT NULL,
            is_approved BIT DEFAULT 0
        )
    ''')
    db.commit()

def fetch_all_equipment():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, user_id, is_assigned FROM equipment')
    rows = cursor.fetchall()
    equipment = [Equipment(row[0], row[1], row[2], row[3]) for row in rows]
    return equipment

def fetch_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name FROM users')
    rows = cursor.fetchall()
    users = [User(row[0], row[1]) for row in rows]
    return users

def get_equipment_by_id(equipment_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, user_id, is_assigned FROM equipment WHERE id = ?', (equipment_id,))
    row = cursor.fetchone()
    if row:
        return Equipment(row[0], row[1], row[2], row[3])
    return None

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        return User(row[0], row[1])
    return None

def assign_equipment(equipment_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE equipment SET user_id = ?, is_assigned = 1 WHERE id = ?', (user_id, equipment_id))
    db.commit()

def request_change(equipment_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO change_requests (equipment_id, user_id) VALUES (?, ?)', (equipment_id, user_id))
    db.commit()

def approve_change(request_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE change_requests SET is_approved = 1 WHERE id = ?', (request_id,))
    db.commit()

def return_equipment(equipment_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE equipment SET user_id = NULL, is_assigned = 0 WHERE id = ?', (equipment_id,))
    db.commit()

@main.route('/main')
def index():
    # equipment = fetch_all_equipment()
    # users = fetch_all_users()
    return render_template('main.html')

@main.route('/assign_equipment', methods=['POST'])
def assign_equipment_route():

    rut = int(request.form.get('rut'))
    fecha = request.form.get('fecha')
    tipo = int(request.form.get('tipo'))
    detalle = request.form.get('detalle')

    current_app.logger.debug(request.form)
    
    values = {'rut':rut, 'fecha':fecha, 'tipo':tipo, 'detalle':detalle}
            

    sql = """
            INSERT INTO cotizacion (rut, fecha, tipo, detalle) 
            VALUES (:rut, :fecha, :tipo, :detalle);"""
    
    with engine.connect() as conn:
        conn.execute(text(sql),values)
        conn.commit()
        flash(f'Se a creado una nueva cotización.')

    return redirect(url_for('main.index'))

@main.route('/request_change/<int:equipment_id>', methods=['POST'])
def request_change_route(equipment_id):
    user_id = int(request.form.get('user_id'))

    equipment = get_equipment_by_id(equipment_id)
    user = get_user_by_id(user_id)

    if equipment and user:
        request_change(equipment_id, user_id)
        flash(f'Se ha solicitado el cambio del equipo {equipment.name} al usuario {user.name}.')

    return redirect(url_for('index'))

@main.route('/approve_change/<int:request_id>', methods=['POST'])
def approve_change_route(request_id):
    approve_change(request_id)
    flash('La solicitud de cambio ha sido aprobada.')
    return redirect(url_for('index'))

@main.route('/return_equipment/<int:equipment_id>', methods=['POST'])
def return_equipment_route(equipment_id):
    equipment = get_equipment_by_id(equipment_id)
    if equipment:
        return_equipment(equipment_id)
        flash(f'El equipo {equipment.name} ha sido devuelto y está disponible para asignación.')

    return redirect(url_for('index'))

@main.route('/agregar')
def ingreso():
    return render_template('ingreso.html')

@main.route('/crud')
def crud():
    with engine.connect() as conn:
        sql1 = """select * from cotizacion """
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('crud.html',datos=datos)

@main.route('/aprobar')
def aprobar():
    return render_template('aprobar.html')

@main.route('/panel')
def panel():
    return render_template('panel.html')

@main.route('/perfil')
def perfil():
    return render_template('perfil.html')



