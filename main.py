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
#                       'Database=PBServforenses;'zz
#                       'UID=Support03;'
#                       "PWD=GajNH6t$'W{,:8R7;"
#                       'Trusted_Connection=no;')
    # return conn

import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd
try:
    url = 'mysql+mysqlconnector://root:@localhost:3306/prueba'
except:
    username = 'criss0106'
    password = 'lyrfacilityservices'
    host = 'criss0106.mysql.pythonanywhere-services.com'
    port = '3306'
    database = 'criss0106$prueba'

    # Construye la URL de conexión
    url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'

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

# @main.route('/assign_equipment', methods=['POST'])
# def assign_equipment_route():

#     rut = int(request.form.get('rut'))
#     fecha = request.form.get('fecha')
#     tipo = int(request.form.get('tipo'))
#     detalle = request.form.get('detalle')

#     current_app.logger.debug(request.form)
    
#     values = {'rut':rut, 'fecha':fecha, 'tipo':tipo, 'detalle':detalle}
            

#     sql = """
#             INSERT INTO cotizacion (rut, fecha, tipo, detalle,estado) 
#             VALUES (:rut, :fecha, :tipo, :detalle,0);"""
    
#     with engine.connect() as conn:
#         conn.execute(text(sql),values)
#         conn.commit()
#         flash(f'Se a creado una nueva cotización.')

#     return redirect(url_for('main.index'))

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
    with engine.connect() as conn:
        sql = """select * from clientes"""
        clientes = conn.execute(text(sql)).fetchall()
    return render_template('ingreso.html',clientes=clientes)

@main.route('/agrega_clientes', methods=['POST'])
def agrega_clientes():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        rut = request.form.get('rut')
        dv = request.form.get('dv')


        values = {'nombre':nombre, 'rut':rut, 'dv':dv}
            

        sql = """
                INSERT INTO prueba.clientes(nombre, rut, dv)
                VALUES(:nombre, :rut, :dv);

                """
    
        with engine.connect() as conn:
            conn.execute(text(sql),values)
            conn.commit()

        return jsonify('success')

@main.route('/crud')
def crud():
    with engine.connect() as conn:
        sql1 = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa  where cot.estado = 0 """
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('crud.html',datos=datos)

@main.route('/aprobar',methods=['POST','GET'])
def aprobar():
    with engine.connect() as conn:
        sql1 = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa  where cot.estado = 1 and orden_compra is NULL"""
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('aprobar.html',datos=datos)
    
@main.route('/insert_oc',methods=['POST','GET'])
def insert_oc():
    try:
        oc = request.form.get('oc')
    except:
        oc = None
    id_cotizacion = request.args.get('id')
    current_app.logger.debug(oc)
    current_app.logger.debug(id_cotizacion)
    if(oc):
        sql = "UPDATE prueba.cotizacion SET orden_compra ="+oc+" where id="+id_cotizacion
    else:
        sql = "UPDATE prueba.cotizacion SET orden_compra =-1 where id="+id_cotizacion

    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
        sql1 = """select * from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa where cot.estado = 1 and orden_compra is NULL"""
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('aprobar.html',datos=datos)
    

@main.route('/insert_factura',methods=['POST','GET'])
def insert_factura():
    try:
        factura = request.form.get('factura')
    except:
        factura = None
    id_cotizacion = request.args.get('id')

    sql = "UPDATE prueba.cotizacion SET factura ="+factura+" where id="+id_cotizacion

    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
        sql1 = """select * from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa where cot.estado = 1 and factura is NULL"""
        datos = conn.execute(text(sql1)).fetchall()
        return render_template('documentos.html',datos=datos)
        

@main.route('/panel')
def panel():
    with engine.connect() as conn:
        sql1 = """select * from users"""
        datos = conn.execute(text(sql1)).fetchall()
    return render_template('panel.html',datos=datos)

@main.route('/usuarios',methods=['POST','GET'])
def usuarios():
    current_app.logger.debug(request.form)
    checkbox_data = request.form

    for key, value in checkbox_data.items():
        print(f"Checkbox {key} está {'marcado' if value == 'on' else 'desmarcado'}")
        partes = str(key).split('-')
        current_app.logger.debug(partes)
        if (partes[0] == 'CT'):
            rol=1
        elif (partes[0] == 'COT'):
            rol=2
        else:
            rol=3

        sql = 'update users set role = '+str(rol)+' where id = '+str(partes[1])
    
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
    with engine.connect() as conn:
        sql1 = """select * from users"""
        datos = conn.execute(text(sql1)).fetchall()
    return render_template('panel.html',datos=datos)

@main.route('/perfil',methods=['POST','GET'])
def perfil():
    with engine.connect() as conn:
        datos_user = """select * from users where username='"""+session['username']+"';"
        datos_user = conn.execute(text(datos_user)).fetchall()
        sql1 = """select * from sol_vacaciones where username = '"""+session['username']+"';"
        datos = conn.execute(text(sql1)).fetchall()

    dias_por_mes = 30
    fecha_actual = datetime.now().date()
    diferencia = (fecha_actual - datos_user[0].fecha_contrato).days
    
    meses_transcurridos = float(diferencia / dias_por_mes)
    dias=round(meses_transcurridos*1.25,1)
    try:
        dias_pedidos=(datos[0].fechafin-datos[0].fechainicio ).days
    except:
        dias_pedidos=0

    current_app.logger.debug(dias_pedidos)

    return render_template('perfil.html',datos=datos,datos_user=datos_user,dias=dias,dias_pedidos=dias_pedidos)

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
    precio_total=0
    id_cotizacion = request.args.get('id')
    with engine.connect() as conn:
        sql_materiales = """select * from material where id_cotizacion="""+id_cotizacion
        materiales = conn.execute(text(sql_materiales)).fetchall()
        sql_cotización = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa where cot.id="""+id_cotizacion
        cotizacion = conn.execute(text(sql_cotización)).fetchall()

    for mat in materiales:
        precio_total+=mat.valor_neto *mat.cantidad* 1.19
    return render_template('ct.html',materiales=materiales,id_cotizacion=id_cotizacion,precio_total=precio_total,cotizacion=cotizacion)

@main.route('/edicion',methods=['POST','GET'])
def edicion():
    id = request.args.get('id')
    valor=0
    valor_obra = 0
    with engine.connect() as conn:
        sql1 = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa  where cot.id= """+id
        datos = conn.execute(text(sql1)).fetchone()
        sql1 = """select * from material where id_cotizacion= """+id
        materiales = conn.execute(text(sql1)).fetchall()
        sql1 = """select valor_neto,cantidad from material where id_cotizacion= """+id
        valores = conn.execute(text(sql1)).fetchall()
        if valores is None:
            valor = 0
        else:
            for i in valores:
                val=float(i.cantidad*float(i.valor_neto))
                valor+=val
                
        sql1 = """select * from mano_obra where id_cotizacion= """+id
        manos_obra = conn.execute(text(sql1)).fetchall()
        sql1 = """select valor_neto from mano_obra where id_cotizacion= """+id
        valores_obra = conn.execute(text(sql1)).fetchall()
        if valores_obra is None:
            valor_obra = 0
        else:
            for i in valores_obra:
                val=float(i.valor_neto)
                valor_obra+=val
        
        current_app.logger.debug(valor)
        return render_template('edicion.html',datos=datos,materiales=materiales,manos_obra=manos_obra,valor=valor,valor_obra=valor_obra)

@main.route('/material', methods=['POST','GET'])
def material():
    
    if request.method == 'POST':
        # proveedor = request.form.get('proveedor')
        cantidad = request.form.get('cantidad')
        valor = int(request.form.get('valor'))
        glosa = request.form.get('glosa')
        cotizacion = int(request.form.get('cotizacion'))
        # sql1 = """select max(id) as 'maximo' from cotizacion"""
        # cotizacion = conn.execute(text(sql1)).fetchone()
        # cotizacion=int(cotizacion)+1

        values = { 'valor':valor, 'glosa':glosa,'cotizacion':cotizacion,'cantidad':cantidad}
            

        sql = """
                INSERT INTO prueba.material(id_cotizacion, valor_neto,glosa,cantidad)
                  VALUES(:cotizacion, :valor, :glosa, :cantidad);
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
        glosa = request.form.get('glosa')
        dias = int(request.form.get('dias'))
        valor = int(request.form.get('valor'))
        
        cotizacion = int(request.form.get('cotizacion'))


        values = {'cantidad':cantidad, 'dias':dias, 'valor':valor,'glosa':glosa, 'cotizacion':cotizacion,'valor_neto':cantidad*dias*valor}
            

        sql = """
                INSERT INTO prueba.mano_obra(id_cotizacion, cantidad, precio, dias,valor_neto,glosa)
                VALUES(:cotizacion, :cantidad, :valor, :dias,:valor_neto,:glosa);

                """
    
        with engine.connect() as conn:
            conn.execute(text(sql),values)
            conn.commit()

        return jsonify('success')

@main.route('/aprobar_cotizacion',methods=['POST','GET'])
def aprobar_cotizacion():
    if request.method == 'POST':
        
        cotizacion = request.form.get('cotizacion')
        detalle = request.form.get('detalle')
        hoy = str(date.today() )

            

        sql = 'update cotizacion set estado = 1, detalle="'+detalle+'",fecha="'+hoy+'" where id = '+cotizacion
    
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
        dias= request.form.get('dias_acumulados')
        current_app.logger.debug(float(dias))
        current_app.logger.debug(end_date)
        current_app.logger.debug(start_date)
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()

        if(float(dias) <= (end_date-start_date).days):
            flash('¡ERROR! Solicitaste mas días de los disponibles.')
            
            return redirect(url_for('main.perfil'))
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
    with engine.connect() as conn:
        sql1 = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa  where cot.estado = 1 and factura is null"""
        datos = conn.execute(text(sql1)).fetchall()
    return render_template('documentos.html',datos=datos)

@main.route('/ingreso_factura')
def ingreso_factura():
    return render_template('ingreso_factura.html')

@main.route('/crud_factura')
def crud_factura():
    return render_template('crud_factura.html')

@main.route('/ingreso_cotizacion',methods=['POST','GET'])
def ingreso_cotizacion():
    
    # sql = """
    #             INSERT INTO cotizacion
    #             (estado)
    #             VALUES(0);

    #             """
    
    with engine.connect() as conn:
        sql = """select * from clientes"""
        clientes = conn.execute(text(sql)).fetchall()
    #     conn.execute(text(sql))
    #     conn.commit()
    #     sql1 = """select max(id) from cotizacion"""
    #     id_max = conn.execute(text(sql1)).fetchone()[0]

    return render_template('ingreso_cotizacion.html',clientes=clientes)

@main.route('/datos_cotizacion',methods=['POST','GET'])
def datos_cotizacion():
    empresa = str(request.form.get('empresa'))
    solicitante = str(request.form.get('solicitante'))

    current_app.logger.debug(empresa)
    current_app.logger.debug(solicitante)


    values = { 'empresa':empresa, 'solicitante':solicitante}
            
    
    sql = """
                INSERT INTO cotizacion
                (estado,rut_empresa,solicitante)
                VALUES(0, :empresa, :solicitante);

                """
    
    with engine.connect() as conn:
        conn.execute(text(sql),values)
        conn.commit()

    return jsonify('success')


@main.route('/delete_cotizacion',methods=['POST','GET'])
def delete_cotizacion():

    id_cotizacion = request.args.get('id')
    sql = """delete from cotizacion where id ="""+id_cotizacion
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/delete_material',methods=['POST','GET'])
def delete_material():

    id_material = request.args.get('id')
    sql = """delete from material where id ="""+id_material
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/delete_mano_obra',methods=['POST','GET'])
def delete_mano_obra():

    id_mano_obra = request.args.get('id')
    sql = """delete from mano_obra where id ="""+id_mano_obra
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/delete_user',methods=['POST','GET'])
def delete_user():

    id_user = request.args.get('id')
    sql = """delete from users where id ="""+id_user
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/delete_vacaciones',methods=['POST','GET'])
def delete_vacaciones():

    id_solicitud = request.args.get('id')
    sql = """delete from sol_vacaciones where id ="""+id_solicitud
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/delete_cliente',methods=['POST','GET'])
def delete_cliente():

    rut = request.args.get('id')
    sql = """delete from clientes where rut ="""+rut
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    return jsonify('success')

@main.route('/edita_materiales',methods=['POST','GET'])
def edita_materiales():

    id_material = request.args.get('id')
    
    
    with engine.connect() as conn:
        sql = """select * from material where id ="""+id_material
        materiales = conn.execute(text(sql)).fetchone()


    return render_template('edita_materiales.html',materiales=materiales)

@main.route('/edita_users',methods=['POST','GET'])
def edita_users():

    id_user = request.args.get('id')
    
    
    with engine.connect() as conn:
        sql = """select * from users where id ="""+id_user
        datos = conn.execute(text(sql)).fetchone()


    return render_template('edita_users.html',datos=datos)
@main.route('/update_materiales',methods=['POST','GET'])
def update_materiales():
    if request.method == 'POST':
        cantidad = str(request.form.get('cantidad'))
        valor = str(request.form.get('valor'))
        glosa = str(request.form.get('glosa'))
        id_material = str(request.form.get('id_material'))
        
        sql = 'update material SET valor_neto ="'+valor+'", glosa ="'+glosa+'" , cantidad="'+cantidad+'" WHERE id = '+id_material

        current_app.logger.debug(sql)
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        return jsonify('success')
    
@main.route('/update_users',methods=['POST','GET'])
def update_users():
    if request.method == 'POST':
        username = request.form['username']
        nombre = request.form['name']
        apellido = request.form['apellido']
        rol = request.form['rol']
        correo = request.form['correo']
        telefono = request.form['telefono']
        contrato = request.form['contrato']
        id = request.form['id']
        current_app.logger.debug(username)
        
        sql = 'update users SET username ="'+username+'", nombre ="'+nombre+'" , apellido="'+apellido+'", role="'+rol+'", correo="'+correo+'", telefono="'+telefono+'", fecha_contrato="'+contrato+'" WHERE id = '+id

        current_app.logger.debug(sql)
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        return jsonify('success')
    
@main.route('/edita_mano_obra',methods=['POST','GET'])
def edita_mano_obra():

    id_mano_obra = request.args.get('id')
    
    
    with engine.connect() as conn:
        sql = """select * from mano_obra where id ="""+id_mano_obra
        mano_obra = conn.execute(text(sql)).fetchone()


    return render_template('edita_mano_de_obra.html',mano_obra=mano_obra)

@main.route('/edita_cliente',methods=['POST','GET'])
def edita_cliente():

    id = request.args.get('id')
    
    
    with engine.connect() as conn:
        sql = """select * from clientes where id ="""+id
        datos_cliente = conn.execute(text(sql)).fetchone()


    return render_template('edita_cliente.html',datos_cliente=datos_cliente)

@main.route('/update_mano_obra',methods=['POST','GET'])
def update_mano_obra():
    if request.method == 'POST':
        cantidad = str(request.form.get('cantidad'))
        glosa = str(request.form.get('glosa'))
        dias = str(request.form.get('dias'))
        valor = str(request.form.get('valor'))
        id_mano_obra = str(request.form.get('id_mano_obra'))
        valor_neto=str(int(cantidad)*int(dias)*float(valor))
        
        sql = 'update mano_obra SET precio ="'+valor+'", glosa ="'+glosa+'" , cantidad="'+cantidad+'", dias="'+dias+'",valor_neto="'+valor_neto+'" WHERE id = '+id_mano_obra

        current_app.logger.debug(sql)
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        return jsonify('success')

@main.route('/update_cliente',methods=['POST','GET'])
def update_cliente():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        rut = request.form.get('rut')
        dv = request.form.get('dv')
        nombre = request.form.get('nombre')

        
        sql = 'update clientes SET rut ="'+rut+'", dv ="'+dv+'" , nombre="'+nombre+'" WHERE id = '+id_cliente

        current_app.logger.debug(sql)
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        return jsonify('success')


@main.route('/historico')
def historico():
    with engine.connect() as conn:
        sql1 = """select cot.id,cot.fecha,cot.detalle,cot.estado,cot.rut_empresa,cot.solicitante,cot.orden_compra,cot.factura,cli.rut ,cli.dv,cli.nombre  from cotizacion  cot inner join clientes cli on cli.rut=cot.rut_empresa where cot.estado = 1 and factura is not null"""
        datos = conn.execute(text(sql1)).fetchall()
    return render_template('historico.html',datos=datos)

@main.route('/gastos')
def gastos():

    with engine.connect() as conn:
        sql = """select * from users"""
        sql1 = """select ren.id, ren.fecha_rendicion, ren.tipo_gasto, ren.descripcion, ren.empleado, ren.monto_gasto from rendicion ren"""
        users = conn.execute(text(sql)).fetchall()
        gastos = conn.execute(text(sql1)).fetchall()
    return render_template('gastos.html', users=users, gastos=gastos)

@main.route('/agrega_gastos',methods=['POST','GET'])
def agrega_gastos():
    fecha_rendicion = str(request.form.get('fecha_rendicion'))
    tipo_gasto = str(request.form.get('tipo_gasto'))
    descripcion = str(request.form.get('descripcion'))
    empleado = str(request.form.get('empleado'))
    monto_gasto = str(request.form.get('monto_gasto'))
    try:
        archivo = str(request.form.get('archivo'))
    except:
        archivo = ""
    
    current_app.logger.debug(fecha_rendicion)
    current_app.logger.debug(tipo_gasto)
    current_app.logger.debug(descripcion)
    current_app.logger.debug(empleado)
    current_app.logger.debug(monto_gasto)
    current_app.logger.debug(archivo)


    values = { 'fecha_rendicion':fecha_rendicion, 'tipo_gasto':tipo_gasto , 'descripcion':descripcion, 'empleado':empleado,'monto_gasto':monto_gasto,'archivo':archivo}
            
    
    sql = """
                INSERT INTO rendicion
                (fecha_rendicion,tipo_gasto,descripcion,empleado,monto_gasto,archivo)
                VALUES(:fecha_rendicion, :tipo_gasto, :descripcion, :empleado, :monto_gasto, :archivo);

                """
    
    with engine.connect() as conn:
        conn.execute(text(sql),values)
        conn.commit()

    return jsonify('success')

@main.route('/Inventario')
def Inventario():

    with engine.connect() as conn:
        sql = """select * from users"""
        sql1 = """select inv.id, inv.nombre, inv.descripcion, inv.valor_unitario, inv.cantidad from inventario inv"""
        users = conn.execute(text(sql)).fetchall()
        inventario = conn.execute(text(sql1)).fetchall()
    return render_template('inventario.html', users=users, inventario=inventario)

@main.route('/agrega_inventario',methods=['POST','GET'])
def agrega_inventario():
    nombre = str(request.form.get('nombre'))
    descripcion = str(request.form.get('descripcion'))
    valor_unitario = str(request.form.get('valor_unitario'))
    cantidad = str(request.form.get('cantidad'))
    try:
        archivo = str(request.form.get('archivo'))
    except:
        archivo = ""
    
    current_app.logger.debug(nombre)
    current_app.logger.debug(descripcion)
    current_app.logger.debug(valor_unitario)
    current_app.logger.debug(cantidad)
    current_app.logger.debug(archivo)


    values = { 'nombre':nombre,'descripcion':descripcion,'valor_unitario':valor_unitario,'cantidad':cantidad,'archivo':archivo}
            
    
    sql = """
                INSERT INTO inventario
                (nombre,descripcion,valor_unitario,cantidad,archivo)
                VALUES(:nombre,:descripcion,:valor_unitario,:cantidad,:archivo);

                """
    
    with engine.connect() as conn:
        conn.execute(text(sql),values)
        conn.commit()

    return jsonify('success')


@main.route('/gastos_clientes')
def gastos_clientes():

    return render_template('gastos_clientes.html')

@main.route('/ingreso_servicio')
def ingreso_servicio():
    

    return render_template('ingreso_servicio.html')