from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Auto:
    def __init__(self,data):

        self.id= data['id']
        self.model = data['model']
        self.year = data['year']
        self.price = data['price']
        self.make = data['make']
        self.description= data['description']
        self.vendedor_id = data['vendedor_id']

    @classmethod
    def crear_auto(cls, data):
        query = "INSERT INTO autos (model, year, price, make, description, vendedor_id, created_at, updated_at) VALUES (%(model)s, %(year)s, %(price)s, %(make)s, %(description)s, %(vendedor_id)s, NOW(), NOW())"
        results = connectToMySQL('vendedores_autos').query_db(query, data)
        return results

    @classmethod
    def ver_uno(cls,data):
        query  = "SELECT * FROM autos WHERE id = %(id)s;"
        result = connectToMySQL('vendedores_autos').query_db(query,data)
        return cls(result[0])

    @classmethod
    def edit(cls, data):
        query = "UPDATE autos SET model=%(model)s,year=%(year)s, price=%(price)s, make=%(make)s, description=%(description)s WHERE autos.id = %(id)s;"
        return connectToMySQL('vendedores_autos').query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM autos WHERE id = %(id)s;"
        results = connectToMySQL('vendedores_autos').query_db(query,data)
        return results
    
    @staticmethod
    def validar_auto(auto):
        is_valid = True
        if auto['price'] =="" or int(auto['price']) < 1000:
            is_valid = False
            flash("El campo no puede estar vacío o el precio no puede ser menor a 1000")
        if len(auto['model']) < 3:
            is_valid = False
            flash("Como mínimo debe tener tres letras")
        if len(auto['make']) < 3:
            is_valid = False
            flash("Como mínimo debe tener tres letras")
        if len(auto['description']) < 2:
            is_valid = False
            flash("La descripción debe tener como minimo una palabra")
        if auto['year'] =="":
            is_valid = False
            flash("Ingresa un año")
        return is_valid
    
    @classmethod
    def todos_autos(cls):
        query = "SELECT * FROM autos JOIN vendedores ON autos.vendedor_id = vendedores.id;"
        autos_db = connectToMySQL('vendedores_autos'). query_db(query)
        todos_autos = []
        for d in autos_db:
            todos_autos.append(cls(d))
        return autos_db 
    
    @classmethod
    def vendedor_auto(cls, data):
        query = "SELECT vendedores.first_name, vendedores.last_name FROM vendedores JOIN autos ON autos.vendedor_id = vendedores.id WHERE autos.id = %(id)s;"
        auto_vendedor = connectToMySQL('vendedores_autos'). query_db(query, data)
        return (auto_vendedor[0])

    