from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import MigrateCommand
from models import *
import os

#Init app0
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LaVacaLoca16@localhost/mantenimiento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)


#Schema Usuario
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('Id', 'UserName', 'Email')

#Init schema
Usuario_Schema = UsuarioSchema()
Usuarios_Schema = UsuarioSchema()

#Crear usuario
@app.route('/product', methods = ['POST']) 
def add_usuario():
    Id = request.json['Id']
    UserName = request.json['UserName']
    Email = request.json['Email']

    new_usuario = Usuarios(Id, UserName, Email)

    db.session.add(new_usuario)
    db.session.commit()

    return Usuario_Schema.jsonify(new_usuario)


if __name__ == '__main__':
    app.run(debug=True)