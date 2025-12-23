from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Proceso, OrdenProceso
from app import db
from datetime import datetime

bp = Blueprint('procesos', __name__, url_prefix='/procesos')

@bp.route('/')
def index():
    """Listar todos los procesos configurados"""
    procesos = Proceso.query.filter_by(activo=True).all()
    return render_template('procesos/index.html', procesos=procesos)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Crear nuevo tipo de proceso"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        # Validar que el nombre no exista
        if Proceso.query.filter_by(nombre=nombre).first():
            flash('El proceso ya existe', 'error')
            return render_template('procesos/form.html')

        proceso = Proceso(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(proceso)
        db.session.commit()

        flash(f'Proceso {nombre} creado exitosamente', 'success')
        return redirect(url_for('procesos.index'))

    return render_template('procesos/form.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar proceso existente"""
    proceso = Proceso.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        # Validar nombre único
        existe = Proceso.query.filter(
            Proceso.nombre == nombre,
            Proceso.id != id
        ).first()

        if existe:
            flash('El nombre del proceso ya existe', 'error')
            return render_template('procesos/form.html', proceso=proceso)

        proceso.nombre = nombre
        proceso.descripcion = descripcion

        db.session.commit()

        flash(f'Proceso {nombre} actualizado exitosamente', 'success')
        return redirect(url_for('procesos.index'))

    return render_template('procesos/form.html', proceso=proceso)

@bp.route('/actualizar-estado/<int:id>', methods=['POST'])
def actualizar_estado(id):
    """Actualizar estado de un proceso en una orden"""
    orden_proceso = OrdenProceso.query.get_or_404(id)

    estado = request.form.get('estado')
    responsable = request.form.get('responsable')
    tiempo_real = request.form.get('tiempo_real')
    observaciones = request.form.get('observaciones')

    orden_proceso.estado = estado
    orden_proceso.responsable = responsable or orden_proceso.responsable
    orden_proceso.observaciones = observaciones

    if tiempo_real:
        orden_proceso.tiempo_real = int(tiempo_real)

    # Actualizar fechas según estado
    if estado == 'En Proceso' and not orden_proceso.fecha_inicio:
        orden_proceso.fecha_inicio = datetime.utcnow()
    elif estado == 'Completado' and not orden_proceso.fecha_fin:
        orden_proceso.fecha_fin = datetime.utcnow()

    db.session.commit()

    flash('Estado del proceso actualizado', 'success')
    return redirect(url_for('ordenes.ver', id=orden_proceso.orden_id))

@bp.route('/seguimiento')
def seguimiento():
    """Ver seguimiento de todos los procesos activos"""
    procesos_activos = OrdenProceso.query.join(OrdenProceso.orden).filter(
        OrdenProceso.estado.in_(['Pendiente', 'En Proceso'])
    ).order_by(OrdenProceso.fecha_inicio).all()

    return render_template('procesos/seguimiento.html', procesos=procesos_activos)
