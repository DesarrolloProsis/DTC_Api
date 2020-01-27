from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#Init app0
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LaVacaLoca16@localhost/mantenimiento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Init db
db = SQLAlchemy(app)


#Inir ma
ma = Marshmallow(app)

#Clases
class Usuarios(db.Model):

    __tablename__ = 'Usuarios'

    Id = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(80), unique = True)
    Email = db.Column(db.String(120), unique = True)

    #Llaves Foraneas
    DTCTecnicoUsuario = relationship("DTCTecnico", uselist=False, back_populates="Usuarios")


    def __init__(self, Id, UserName, Email):
        self.Id = Id
        self.UserName = UserName
        self.Email = Email


class CatalogoRefacciones(db.Model):

    __tablename__ = 'CatalogoRefacciones'

    NoParte = db.Column(db.String(50), primary_key = True, nullable = False)
    TipoServicio = db.Column(db.String(25), nullable = False) 
    Nombre = db.Column(db.String(25), nullable = False)
    Marca = db.Column(db.String(25), nullable = False)
    Precio = db.Column(db.Float, nullable = False)
    Unidad = db.Column(db.Integer, nullable = False)
    YearPieza = db.Column(db.String(5), nullable = False)
    ImagenRefaccion = db.Column(db.Text, nullable = True)       
    Descripcion = db.Column(db.Text, nullable = True)

    #Llaves Foraneas
    DTCTecnicoRefacciones = relationship("DTCTecnico", uselist=False, back_populates="Refaccion")

class CatalogoPlazas(db.Model):

    __tablename__ = 'CatalogoPlazas'
    
    NoPlaza = db.Column(db.Integer, primary_key = True, unique = True)
    NombrePlaza = db.Column(db.String(20), nullable = False)
    Delegacion = db.Column(db.String(20), nullable = False)

    #Llaves Foraneas
    Carril = relationship("CatalogoCarriles", uselist=False, back_populates="Plaza")


class CatalogoCarriles(db.Model):

    __tablename__ = 'CatalogoCarriles'

    NoCapufeLane = db.Column(db.Integer, primary_key = True, unique = True)
    Lane = db.Column(db.String(4), nullable = False, unique = False)
    TipoLane = db.Column(db.String(15), nullable = False)
    PlazaId = db.Column(db.Integer, db.ForeignKey('CatalogoPlazas.NoPlaza'), nullable = False )
    
    #Llaves Foraneas
    Plaza = relationship("CatalogoPlazas", back_populates = "Carril")
    DTCTecnicoCarril = relationship("DTCTecnico", uselist=False, back_populates="Carril")


class DTCEncabezado(db.Model):

    __tablename__ = 'DTCEncabezado'

    Id = db.Column(db.Integer, primary_key = True, unique = True)
    NoConvenio = db.Column(db.Integer, nullable = False)
    NombreEncargado = db.Column(db.String(20), nullable = False)
    Cargo = db.Column(db.String(20), nullable = False)

    #Llaves Foraneas
    DTCTecnicoEncabezado = relationship("DTCTecnico", uselist=False, back_populates="Convenio")


class DTCTecnico(db.Model):

    __tablename__ = 'DTCTecnico'   

    NoReferencia = db.Column(db.String(10), primary_key = True, nullable = False)

    CarrilId = db.Column(db.Integer, db.ForeignKey('CatalogoCarriles.NoCapufeLane'), nullable = False)
    Carril = relationship("CatalogoCarriles",  back_populates = "DTCTecnicoCarril")

    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable = False)
    Usuarios = relationship("Usuarios",  back_populates = "DTCTecnicoUsuario")

    ConvenioId = db.Column(db.Integer, db.ForeignKey('DTCEncabezado.Id'), nullable = False)
    Convenio = relationship("DTCEncabezado",  back_populates = "DTCTecnicoEncabezado")

    RefaccionId = db.Column(db.String(50), db.ForeignKey('CatalogoRefacciones.NoParte'), nullable = False)
    Refaccion = relationship("CatalogoRefacciones",  back_populates = "DTCTecnicoRefacciones")

    NoAXA = db.Column(db.String(8), unique = True)
    FolioFalla = db.Column(db.Integer, unique = True)
    Estatus = db.Column(db.String(30))
    DateFalla = db.Column(db.DateTime)
    DateSiniestro = db.Column(db.DateTime)
    DateElaboracion = db.Column(db.DateTime)
    DateEnvio = db.Column(db.DateTime)
    TipoDictamen = db.Column(db.String(20))
    Descripcion = db.Column(db.Text)
    Diagnostico = db.Column(db.String(30))
    Observacion = db.Column(db.Text)
    Imagen = db.Column(db.Text)

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