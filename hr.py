from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import os

# Crear el Blueprint para el módulo de Recursos Humanos
hr_bp = Blueprint('hr', __name__)

# Configurar la ruta donde se almacenarán los documentos subidos
DOCUMENTS_UPLOAD_FOLDER = '/Users/bayronfuentealba/Desktop/proyectos negocio/lyr-facilityservices/uploads/documents'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Configurar la extensión de archivos permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta principal del módulo de Recursos Humanos
@hr_bp.route('/hr')
def hr_index():
    # Obtener la lista de documentos almacenados
    documents = os.listdir(DOCUMENTS_UPLOAD_FOLDER)
    return render_template('hr/index.html',documents=documents)

# Ruta para subir un documento
@hr_bp.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if request.method == 'POST':
        # Verificar si se envió un archivo
        if 'document' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'danger')
            return redirect(request.url)
        file = request.files['document']
        # Verificar si se seleccionó un archivo válido
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Guardar el archivo en la carpeta de documentos
            filename = secure_filename(file.filename)
            file.save(os.path.join(DOCUMENTS_UPLOAD_FOLDER, filename))
            flash('El archivo se ha subido correctamente', 'success')
            return redirect(url_for('hr.hr_index'))
        else:
            flash('Formato de archivo no permitido', 'danger')
    return render_template('hr/upload_document.html')

# Ruta para solicitar vacaciones
@hr_bp.route('/vacation_request', methods=['GET', 'POST'])
def vacation_request():
    if request.method == 'POST':
        # Procesar el formulario de solicitud de vacaciones
        # Aquí puedes agregar la lógica para almacenar la solicitud en la base de datos, enviar notificaciones, etc.
        flash('La solicitud de vacaciones se ha enviado', 'success')
        return redirect(url_for('hr.hr_index'))
    return render_template('hr/vacation_request.html')
