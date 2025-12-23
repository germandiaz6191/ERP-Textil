from flask import Blueprint, render_template
from app.models import Orden, Referencia, Inventario, OrdenProceso
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Dashboard principal"""
    # Estadísticas
    total_referencias = Referencia.query.filter_by(activo=True).count()
    ordenes_activas = Orden.query.filter_by(estado='En Proceso').count()
    ordenes_terminadas = Orden.query.filter_by(estado='Terminada').count()

    # Órdenes recientes
    ordenes_recientes = Orden.query.order_by(Orden.fecha_creacion.desc()).limit(5).all()

    # Procesos pendientes
    procesos_pendientes = OrdenProceso.query.filter(
        OrdenProceso.estado.in_(['Pendiente', 'En Proceso'])
    ).order_by(OrdenProceso.fecha_inicio).limit(10).all()

    # Inventario bajo (menos de 10 unidades)
    inventario_bajo = Inventario.query.filter(Inventario.cantidad_disponible < 10).all()

    return render_template('dashboard.html',
                           total_referencias=total_referencias,
                           ordenes_activas=ordenes_activas,
                           ordenes_terminadas=ordenes_terminadas,
                           ordenes_recientes=ordenes_recientes,
                           procesos_pendientes=procesos_pendientes,
                           inventario_bajo=inventario_bajo)
