from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Vendedor:
    def __init__(self,data):

        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
    
    @classmethod
    def crear_vendedor(cls, data):
        query = "INSERT INTO vendedores (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('vendedores_autos').query_db(query, data)
    
    @classmethod
    def all_vendedores(cls):
        query = "SELECT * FROM vendedores;"
        vendedores_db =  connectToMySQL('vendedores_autos').query_db(query)
        vendedores =[]
        for vendedor in vendedores_db:
            vendedores.append(cls(vendedor))
        return vendedores
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM vendedores WHERE email = %(email)s;"
        results = connectToMySQL('vendedores_autos').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM vendedores WHERE id = %(id)s;"
        results = connectToMySQL('vendedores_autos').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_vendedor(vendedor):
        is_valid = True
        query = "SELECT * FROM vendedores WHERE email = %(email)s;"
        results = connectToMySQL('vendedores_autos').query_db(query,vendedor)
        if len(vendedor['first_name']) < 3:
            flash("Deben ser minimo 3 caracteres.")
            is_valid = False
        if len(vendedor['last_name']) < 3:
            flash("Deben ser minimo 3 caracteres")
            is_valid = False
        if len(results) >= 1:
            flash("El correo ya ha sido utilizado.")
            is_valid =False
        if not EMAIL_REGEX.match(vendedor['email']): 
            flash("Correo no valido!")
            is_valid = False
        if len(vendedor['password']) < 5:
            flash("Deben ser minimo 3 caracteres")
            is_valid = False
        if vendedor['password']!= vendedor['confirm']:
            flash("Las contrasenas no coinciden.")
            is_valid = False
        return is_valid



            
    
