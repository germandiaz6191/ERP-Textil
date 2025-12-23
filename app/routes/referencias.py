from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Referencia, Inventario
from app import db

bp = Blueprint('referencias', __name__, url_prefix='/referencias')

@bp.route('/')
def index():
    """Listar todas las referencias"""
    referencias = Referencia.query.filter_by(activo=True).all()
    return render_template('referencias/index.html', referencias=referencias)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    """Crear nueva referencia"""
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        ficha_tecnica = request.form.get('ficha_tecnica')

        # Validar que el código no exista
        if Referencia.query.filter_by(codigo=codigo).first():
            flash('El código de referencia ya existe', 'error')
            return render_template('referencias/form.html')

        referencia = Referencia(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            ficha_tecnica=ficha_tecnica
        )

        db.session.add(referencia)
        db.session.flush()  # Para obtener el ID

        # Crear registro de inventario
        inventario = Inventario(referencia_id=referencia.id, cantidad_disponible=0)
        db.session.add(inventario)

        db.session.commit()

        flash(f'Referencia {codigo} creada exitosamente', 'success')
        return redirect(url_for('referencias.index'))

    return render_template('referencias/form.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar referencia existente"""
    referencia = Referencia.query.get_or_404(id)

    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        ficha_tecnica = request.form.get('ficha_tecnica')

        # Validar código único (excepto la misma referencia)
        existe = Referencia.query.filter(
            Referencia.codigo == codigo,
            Referencia.id != id
        ).first()

        if existe:
            flash('El código de referencia ya existe', 'error')
            return render_template('referencias/form.html', referencia=referencia)

        referencia.codigo = codigo
        referencia.nombre = nombre
        referencia.descripcion = descripcion
        referencia.ficha_tecnica = ficha_tecnica

        db.session.commit()

        flash(f'Referencia {codigo} actualizada exitosamente', 'success')
        return redirect(url_for('referencias.index'))

    return render_template('referencias/form.html', referencia=referencia)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Desactivar referencia (soft delete)"""
    referencia = Referencia.query.get_or_404(id)
    referencia.activo = False
    db.session.commit()

    flash(f'Referencia {referencia.codigo} desactivada', 'success')
    return redirect(url_for('referencias.index'))

@bp.route('/ver/<int:id>')
def ver(id):
    """Ver detalle de referencia"""
    referencia = Referencia.query.get_or_404(id)
    return render_template('referencias/detalle.html', referencia=referencia)
