from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Inventario, Referencia, MovimientoInventario
from app import db
from datetime import datetime

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('/')
def index():
    """Ver inventario actual"""
    inventarios = Inventario.query.join(Inventario.referencia).filter(
        Referencia.activo == True
    ).all()
    return render_template('inventario/index.html', inventarios=inventarios)

@bp.route('/ajustar/<int:id>', methods=['GET', 'POST'])
def ajustar(id):
    """Ajustar inventario manualmente"""
    inventario = Inventario.query.get_or_404(id)

    if request.method == 'POST':
        tipo = request.form.get('tipo')  # Entrada o Salida
        cantidad = int(request.form.get('cantidad'))
        observaciones = request.form.get('observaciones')

        if tipo == 'Entrada':
            inventario.cantidad_disponible += cantidad
        elif tipo == 'Salida':
            if inventario.cantidad_disponible < cantidad:
                flash('No hay suficiente inventario disponible', 'error')
                return redirect(url_for('inventario.ajustar', id=id))
            inventario.cantidad_disponible -= cantidad

        # Registrar movimiento
        movimiento = MovimientoInventario(
            referencia_id=inventario.referencia_id,
            tipo=tipo,
            cantidad=cantidad,
            observaciones=observaciones
        )
        db.session.add(movimiento)

        db.session.commit()

        flash(f'Inventario ajustado: {tipo} de {cantidad} unidades', 'success')
        return redirect(url_for('inventario.index'))

    return render_template('inventario/ajustar.html', inventario=inventario)

@bp.route('/movimientos/<int:referencia_id>')
def movimientos(referencia_id):
    """Ver historial de movimientos de una referencia"""
    referencia = Referencia.query.get_or_404(referencia_id)
    movimientos = MovimientoInventario.query.filter_by(
        referencia_id=referencia_id
    ).order_by(MovimientoInventario.fecha.desc()).all()

    return render_template('inventario/movimientos.html',
                           referencia=referencia,
                           movimientos=movimientos)

@bp.route('/reporte')
def reporte():
    """Generar reporte de inventario"""
    inventarios = Inventario.query.join(Inventario.referencia).filter(
        Referencia.activo == True
    ).all()

    # Calcular estadísticas
    total_referencias = len(inventarios)
    total_unidades = sum(i.cantidad_disponible for i in inventarios)
    referencias_bajo_stock = sum(1 for i in inventarios if i.cantidad_disponible < 10)

    return render_template('inventario/reporte.html',
                           inventarios=inventarios,
                           total_referencias=total_referencias,
                           total_unidades=total_unidades,
                           referencias_bajo_stock=referencias_bajo_stock)
