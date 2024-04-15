from flask import Flask
from flask import Flask, request, jsonify
from database.user_repository import UserRepository
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.register_blueprint(auth_bp)

user_repo = UserRepository()

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Persona {self.nombre}>"

@app.route('/persona', methods=['POST'])
def crear_persona():
    data = request.json
    nueva_persona = Persona(nombre=data['nombre'], dni=data['dni'], fecha_nacimiento=data['fecha_nacimiento'])
    db.session.add(nueva_persona)
    db.session.commit()
    return jsonify({'message': 'Persona creada exitosamente'}), 201

@app.route('/persona/<int:id>', methods=['GET'])
def obtener_persona(id):
    persona = Persona.query.get(id)
    if persona:
        return jsonify({'id': persona.id, 'nombre': persona.nombre, 'dni': persona.dni, 'fecha_nacimiento': str(persona.fecha_nacimiento)})
    else:
        return jsonify({'message': 'Persona no encontrada'}), 404

@app.route('/persona/<int:id>', methods=['PUT'])
def actualizar_persona(id):
    persona = Persona.query.get(id)
    if persona:
        data = request.json
        persona.nombre = data.get('nombre', persona.nombre)
        persona.dni = data.get('dni', persona.dni)
        persona.fecha_nacimiento = data.get('fecha_nacimiento', persona.fecha_nacimiento)
        db.session.commit()
        return jsonify({'message': 'Persona actualizada exitosamente'})
    else:
        return jsonify({'message': 'Persona no encontrada'}), 404

@app.route('/persona/<int:id>', methods=['DELETE'])
def eliminar_persona(id):
    persona = Persona.query.get(id)
    if persona:
        db.session.delete(persona)
        db.session.commit()
        return jsonify({'message': 'Persona eliminada exitosamente'})
    else:
        return jsonify({'message': 'Persona no encontrada'}), 404

@app.route('/personas', methods=['GET'])
def obtener_todas_personas():
    personas = Persona.query.all()
    personas_json = [{'id': persona.id, 'nombre': persona.nombre, 'dni': persona.dni, 'fecha_nacimiento': str(persona.fecha_nacimiento)} for persona in personas]
    return jsonify(personas_json)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)