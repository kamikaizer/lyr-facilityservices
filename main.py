import io
# import pyodbc
# from flask import make_response 
from flask import Blueprint,session, render_template, redirect,url_for,request,flash,jsonify,json,send_file,current_app
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
            INSERT INTO cotizacion (rut, fecha, tipo, detalle,estado) 
            VALUES (:rut, :fecha, :tipo, :detalle,0);"""
    
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
        sql1 = """select * from cotizacion where estado = 0 """
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('crud.html',datos=datos)

@main.route('/aprobar')
def aprobar():
    with engine.connect() as conn:
        sql1 = """select * from cotizacion where estado = 1"""
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('aprobar.html',datos=datos)

@main.route('/panel')
def panel():
    return render_template('panel.html')

@main.route('/perfil',methods=['POST','GET'])
def perfil():
    with engine.connect() as conn:
        sql1 = """select * from sol_vacaciones where username = '"""+session['nombre']+"';"
        datos = conn.execute(text(sql1)).fetchall()
    
    return render_template('perfil.html',datos=datos)

@main.route('/rrhh')
def rrhh():
     with engine.connect() as conn:
        sql1 = """select * from users """
        datos = conn.execute(text(sql1)).fetchall()
        sql1 = """select * from sol_vacaciones where estado=0 """
        datos1 = conn.execute(text(sql1)).fetchall()
        return render_template('rrhh.html',datos=datos,datos1=datos1)
    

@main.route('/factura')
def factura():
    return render_template('factura.html')

@main.route('/ct')
def ct():
    return render_template('ct.html')

@main.route('/edicion',methods=['POST','GET'])
def edicion():
    id = request.args.get('id')
    with engine.connect() as conn:
        sql1 = """select * from cotizacion where id= """+id
        datos = conn.execute(text(sql1)).fetchone()
        sql1 = """select * from material where id_cotizacion= """+id
        materiales = conn.execute(text(sql1)).fetchall()
        sql1 = """select sum(valor_neto) as 'valor' from material where id_cotizacion= """+id
        valor = conn.execute(text(sql1)).fetchone()
        if valor[0] is None:
            valor = 0
        else:
            valor = float(valor[0])


        sql1 = """select * from cotizacion where id= """+id
        datos = conn.execute(text(sql1)).fetchone()
        sql1 = """select * from mano_obra where id_cotizacion= """+id
        manos_obra = conn.execute(text(sql1)).fetchall()
        sql1 = """select sum(valor_neto) as 'valor' from mano_obra where id_cotizacion= """+id
        valor_obra = conn.execute(text(sql1)).fetchone()
        if valor_obra[0] is None:
            valor_obra = 0
        else:
            valor_obra = float(valor_obra[0])
        
        current_app.logger.debug(valor)
        return render_template('edicion.html',datos=datos,materiales=materiales,manos_obra=manos_obra,valor=valor,valor_obra=valor_obra)

@main.route('/material', methods=['POST','GET'])
def material():
    
    if request.method == 'POST':
        proveedor = request.form.get('proveedor')
        factura = request.form.get('factura')
        valor = int(request.form.get('valor'))
        glosa = request.form.get('glosa')
        cotizacion = int(request.form.get('cotizacion'))


        values = {'proveedor':proveedor, 'factura':factura, 'valor':valor, 'glosa':glosa,'cotizacion':cotizacion}
            

        sql = """
                INSERT INTO prueba.material(id_cotizacion, proveedor, factura, valor_neto)
                  VALUES(:cotizacion, :proveedor, :factura, :valor);
                  """
    
        with engine.connect() as conn:
            conn.execute(text(sql),values)
            conn.commit()

        return jsonify('success')
    
@main.route('/mano_obra', methods=['POST','GET'])
def mano_obra():
    
    if request.method == 'POST':
        current_app.logger.debug(request.form)
        cantidad = int(request.form.get('cantidad'))
        dias = int(request.form.get('dias'))
        valor = int(request.form.get('valor'))
        
        cotizacion = int(request.form.get('cotizacion'))


        values = {'cantidad':cantidad, 'dias':dias, 'valor':valor, 'cotizacion':cotizacion,'valor_neto':cantidad*dias*valor}
            

        sql = """
                INSERT INTO prueba.mano_obra(id_cotizacion, cantidad, precio, dias,valor_neto)
                VALUES(:cotizacion, :cantidad, :valor, :dias,:valor_neto);

                """
    
        with engine.connect() as conn:
            conn.execute(text(sql),values)
            conn.commit()

        return jsonify('success')

@main.route('/aprobar_cotizacion',methods=['POST','GET'])
def aprobar_cotizacion():
    if request.method == 'POST':
        
        cotizacion = request.form.get('cotizacion')


            

        sql = """update cotizacion set estado = 1 where id = """+cotizacion+";"
    
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        return jsonify('success')
    
@main.route('/sol_vacaciones',methods=['POST','GET'])
def sol_vacaciones():
    current_app.logger.debug("aqazwsxqazwsx")
    if request.method == 'POST':
        current_app.logger.debug("asds fvdssdfasba")
        id_user = request.form.get('id_user')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')

        current_app.logger.debug(request)

            

        values = {'id_user':id_user, 'start_date':start_date, 'end_date':end_date, 'reason':reason}
            

        sql = """
                INSERT INTO sol_vacaciones
                (fechainicio, fechafin, detalle, estado, username)
                VALUES(:start_date, :end_date, :reason, 0, :id_user);

                """
    
        with engine.connect() as conn:
            conn.execute(text(sql),values)
            conn.commit()

        return redirect(url_for('main.perfil'))
        

@main.route('/documentos')
def documentos():
    return render_template('documentos.html')





