from app import create_app, db
from app.models import Referencia, Proceso, Orden, OrdenProceso, Inventario, MovimientoInventario

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Referencia': Referencia,
        'Proceso': Proceso,
        'Orden': Orden,
        'OrdenProceso': OrdenProceso,
        'Inventario': Inventario,
        'MovimientoInventario': MovimientoInventario
    }

@app.cli.command()
def init_db():
    """Inicializar base de datos con datos de ejemplo"""
    db.create_all()

    # Crear procesos estándar si no existen
    if Proceso.query.count() == 0:
        procesos = [
            Proceso(nombre='Corte', descripcion='Proceso de corte de tela'),
            Proceso(nombre='Confección', descripcion='Proceso de confección de prendas'),
            Proceso(nombre='Terminación', descripcion='Procesos de terminado y acabado'),
            Proceso(nombre='Control de Calidad', descripcion='Verificación de calidad'),
            Proceso(nombre='Empaque', descripcion='Empaque final del producto')
        ]
        for p in procesos:
            db.session.add(p)
        db.session.commit()
        print('Procesos estándar creados')

    print('Base de datos inicializada')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
