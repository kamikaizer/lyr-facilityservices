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

# url = 'mysql+mysqlconnector://root:root1234@localhost:3306/prueba'
# engine = sqlalchemy.create_engine(url)


main = Blueprint('main', __name__)




