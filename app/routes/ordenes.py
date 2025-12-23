from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Orden, Referencia, Proceso, OrdenProceso, Inventario, MovimientoInventario
from app import db
from datetime import datetime

bp = Blueprint('ordenes', __name__, url_prefix='/ordenes')

@bp.route('/')
def index():
    """Listar todas las órdenes"""
    estado = request.args.get('estado', '')

    query = Orden.query

    if estado:
        query = query.filter_by(estado=estado)

    ordenes = query.order_by(Orden.fecha_creacion.desc()).all()
    return render_template('ordenes/index.html', ordenes=ordenes, estado_filtro=estado)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    """Crear nueva orden"""
    if request.method == 'POST':
        numero_orden = request.form.get('numero_orden')
        orden_compra = request.form.get('orden_compra')
        referencia_id = request.form.get('referencia_id')
        cantidad = request.form.get('cantidad')
        observaciones = request.form.get('observaciones')

        # Validar que el número de orden no exista
        if Orden.query.filter_by(numero_orden=numero_orden).first():
            flash('El número de orden ya existe', 'error')
            referencias = Referencia.query.filter_by(activo=True).all()
            return render_template('ordenes/form.html', referencias=referencias)

        orden = Orden(
            numero_orden=numero_orden,
            orden_compra=orden_compra,
            referencia_id=referencia_id,
            cantidad=cantidad,
            observaciones=observaciones
        )

        db.session.add(orden)
        db.session.commit()

        flash(f'Orden {numero_orden} creada exitosamente', 'success')
        return redirect(url_for('ordenes.asignar_procesos', id=orden.id))

    referencias = Referencia.query.filter_by(activo=True).all()
    return render_template('ordenes/form.html', referencias=referencias)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar orden existente"""
    orden = Orden.query.get_or_404(id)

    if request.method == 'POST':
        numero_orden = request.form.get('numero_orden')
        orden_compra = request.form.get('orden_compra')
        cantidad = request.form.get('cantidad')
        observaciones = request.form.get('observaciones')

        # Validar número único
        existe = Orden.query.filter(
            Orden.numero_orden == numero_orden,
            Orden.id != id
        ).first()

        if existe:
            flash('El número de orden ya existe', 'error')
            referencias = Referencia.query.filter_by(activo=True).all()
            return render_template('ordenes/form.html', orden=orden, referencias=referencias)

        orden.numero_orden = numero_orden
        orden.orden_compra = orden_compra
        orden.cantidad = cantidad
        orden.observaciones = observaciones

        db.session.commit()

        flash(f'Orden {numero_orden} actualizada exitosamente', 'success')
        return redirect(url_for('ordenes.ver', id=id))

    referencias = Referencia.query.filter_by(activo=True).all()
    return render_template('ordenes/form.html', orden=orden, referencias=referencias)

@bp.route('/asignar-procesos/<int:id>', methods=['GET', 'POST'])
def asignar_procesos(id):
    """Asignar procesos a una orden"""
    orden = Orden.query.get_or_404(id)

    if request.method == 'POST':
        # Eliminar procesos existentes
        OrdenProceso.query.filter_by(orden_id=id).delete()

        # Obtener procesos seleccionados
        procesos_ids = request.form.getlist('procesos[]')
        responsables = request.form.getlist('responsables[]')
        tiempos = request.form.getlist('tiempos[]')

        for i, proceso_id in enumerate(procesos_ids):
            orden_proceso = OrdenProceso(
                orden_id=id,
                proceso_id=proceso_id,
                responsable=responsables[i] if i < len(responsables) else None,
                tiempo_estimado=int(tiempos[i]) if i < len(tiempos) and tiempos[i] else None,
                orden_secuencia=i + 1
            )
            db.session.add(orden_proceso)

        db.session.commit()

        flash(f'Procesos asignados a orden {orden.numero_orden}', 'success')
        return redirect(url_for('ordenes.ver', id=id))

    procesos = Proceso.query.filter_by(activo=True).all()
    return render_template('ordenes/asignar_procesos.html', orden=orden, procesos=procesos)

@bp.route('/ver/<int:id>')
def ver(id):
    """Ver detalle de orden"""
    orden = Orden.query.get_or_404(id)
    return render_template('ordenes/detalle.html', orden=orden)

@bp.route('/completar/<int:id>', methods=['POST'])
def completar(id):
    """Marcar orden como terminada y trasladar a inventario"""
    orden = Orden.query.get_or_404(id)

    # Verificar que todos los procesos estén completados
    procesos_pendientes = [p for p in orden.procesos_orden if p.estado != 'Completado']

    if procesos_pendientes:
        flash('No se puede completar la orden. Hay procesos pendientes.', 'error')
        return redirect(url_for('ordenes.ver', id=id))

    # Marcar orden como terminada
    orden.estado = 'Terminada'
    orden.fecha_terminacion = datetime.utcnow()

    # Trasladar a inventario
    inventario = Inventario.query.filter_by(referencia_id=orden.referencia_id).first()

    if inventario:
        inventario.cantidad_disponible += orden.cantidad
    else:
        inventario = Inventario(
            referencia_id=orden.referencia_id,
            cantidad_disponible=orden.cantidad
        )
        db.session.add(inventario)

    # Registrar movimiento
    movimiento = MovimientoInventario(
        referencia_id=orden.referencia_id,
        tipo='Entrada',
        cantidad=orden.cantidad,
        orden_id=orden.id,
        observaciones=f'Entrada desde orden {orden.numero_orden}'
    )
    db.session.add(movimiento)

    db.session.commit()

    flash(f'Orden {orden.numero_orden} completada y trasladada a inventario', 'success')
    return redirect(url_for('ordenes.ver', id=id))

@bp.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    """Cancelar orden"""
    orden = Orden.query.get_or_404(id)
    orden.estado = 'Cancelada'
    db.session.commit()

    flash(f'Orden {orden.numero_orden} cancelada', 'success')
    return redirect(url_for('ordenes.index'))
