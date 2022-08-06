from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.vendedor import Vendedor
from flask_app.models.auto import Auto
bcrypt = Bcrypt(app)  

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registrar():
    
    if not Vendedor.validate_vendedor(request.form):
        return redirect('/')
    nuevo_vendedor= {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Vendedor.crear_vendedor(nuevo_vendedor)
    session['vendedor_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    vendedor = Vendedor.get_by_email(data)
    print(vendedor)
    if not vendedor:
        flash("El correo no corresponde a la contrasena ingresada")
        return redirect("/")
    if not bcrypt.check_password_hash(vendedor.password,request.form['password']):
        flash("No coinciden las contrasenas")
        return redirect("/") 
    session['vendedor_id'] = vendedor.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'vendedor_id' not in session:
        return redirect('/logout')
    un_vendedor = {
        "id" : session['vendedor_id']
    }
    nombre_prueba = Vendedor.get_one(un_vendedor)
    autos = Auto.todos_autos()
    return render_template('dashboard.html', nombre_prueba = nombre_prueba, autos=autos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')








