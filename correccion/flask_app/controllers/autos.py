from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models.auto import Auto
from flask_app.models.vendedor import Vendedor

@app.route('/agregar')
def nuevo_auto():
    if 'vendedor_id' not in session:
        return redirect('/logout')

    data_vendedor = {
        "id":session['vendedor_id']
    }
    vendedor = Vendedor.get_one(data_vendedor) 
    return render_template('new.html', vendedor = vendedor)

@app.route('/agregar/auto', methods=['POST'])
def agregar_auto():

    if 'vendedor_id' not in session:
        return redirect('/logout')

    if not Auto.validar_auto(request.form):
        return redirect('/agregar')
        
    nuevo_auto = {
        "price" : request.form['price'],
        "model" : request.form['model'],
        "make" : request.form['make'],
        "year" : request.form['year'],
        "description" : request.form['description'],
        "vendedor_id": session['vendedor_id'],
    }
    Auto.crear_auto(nuevo_auto)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def mostrar(id):

    if 'vendedor_id' not in session:
        return redirect('/logout')
    data_auto = {
        "id":id
    }

    vendedor = Auto.vendedor_auto(data_auto)
    print (vendedor)
    auto = Auto.ver_uno(data_auto)
    print(auto)
    return render_template('show.html', auto = auto, vendedor=vendedor )

@app.route('/eliminar/<int:id>')
def eliminar_auto(id):

    if 'vendedor_id' not in session:
        return redirect('/logout')

    data = {
        "id":id
    }

    Auto.destroy(data)
    return redirect('/dashboard')

@app.route('/editar/<int:id>')
def editar(id):
    if 'vendedor_id' not in session:
        return redirect('/logout')

    data_auto = {
        "id": id
    }
    dato = Auto.ver_uno(data_auto)
    return render_template('edit.html', dato=dato)

@app.route('/editar/auto', methods = ['POST'])
def editar_auto():
    print(request.form["price"])
    if 'vendedor_id' not in session:
        return redirect('/logout')

    if not Auto.validar_auto(request.form):
        return redirect('/editar/'+ request.form["id"])

    data_auto = {
        "id": request.form["id"],
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"]
    }

    Auto.edit(data_auto)
    return redirect('/dashboard')
