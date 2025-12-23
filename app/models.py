from app import db
from datetime import datetime

class Referencia(db.Model):
    """Modelo para referencias/productos"""
    __tablename__ = 'referencias'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    ficha_tecnica = db.Column(db.Text)  # Puede almacenar JSON como texto
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    ordenes = db.relationship('Orden', backref='referencia', lazy=True)
    inventario = db.relationship('Inventario', backref='referencia', uselist=False)

    def __repr__(self):
        return f'<Referencia {self.codigo} - {self.nombre}>'


class Proceso(db.Model):
    """Modelo para tipos de procesos (Corte, Confección, etc.)"""
    __tablename__ = 'procesos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Proceso {self.nombre}>'


class Orden(db.Model):
    """Modelo para órdenes de producción"""
    __tablename__ = 'ordenes'

    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(50), unique=True, nullable=False)
    orden_compra = db.Column(db.String(50))
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='En Proceso')  # En Proceso, Terminada, Cancelada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_terminacion = db.Column(db.DateTime)
    observaciones = db.Column(db.Text)

    # Relaciones
    procesos_orden = db.relationship('OrdenProceso', backref='orden', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Orden {self.numero_orden}>'

    @property
    def progreso(self):
        """Calcula el progreso de la orden basado en procesos completados"""
        if not self.procesos_orden:
            return 0
        completados = sum(1 for p in self.procesos_orden if p.estado == 'Completado')
        return (completados / len(self.procesos_orden)) * 100


class OrdenProceso(db.Model):
    """Modelo para procesos asignados a una orden"""
    __tablename__ = 'orden_procesos'

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    proceso_id = db.Column(db.Integer, db.ForeignKey('procesos.id'), nullable=False)
    responsable = db.Column(db.String(200))
    tiempo_estimado = db.Column(db.Integer)  # en minutos
    tiempo_real = db.Column(db.Integer)  # en minutos
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, En Proceso, Completado
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    observaciones = db.Column(db.Text)
    orden_secuencia = db.Column(db.Integer, default=0)  # Para ordenar procesos

    # Relaciones
    proceso = db.relationship('Proceso', backref='orden_procesos')

    def __repr__(self):
        return f'<OrdenProceso Orden:{self.orden_id} Proceso:{self.proceso_id}>'


class Inventario(db.Model):
    """Modelo para inventario de productos terminados"""
    __tablename__ = 'inventario'

    id = db.Column(db.Integer, primary_key=True)
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), unique=True, nullable=False)
    cantidad_disponible = db.Column(db.Integer, default=0)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    movimientos = db.relationship('MovimientoInventario', backref='inventario_ref', lazy=True)

    def __repr__(self):
        return f'<Inventario Ref:{self.referencia_id} Cant:{self.cantidad_disponible}>'


class MovimientoInventario(db.Model):
    """Modelo para auditoría de movimientos de inventario"""
    __tablename__ = 'movimientos_inventario'

    id = db.Column(db.Integer, primary_key=True)
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Entrada, Salida
    cantidad = db.Column(db.Integer, nullable=False)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    usuario = db.Column(db.String(100))  # Para auditoría

    # Relaciones
    referencia = db.relationship('Referencia', backref='movimientos')
    orden = db.relationship('Orden', backref='movimientos')

    def __repr__(self):
        return f'<Movimiento {self.tipo} Ref:{self.referencia_id} Cant:{self.cantidad}>'
