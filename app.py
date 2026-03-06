from flask import Flask, render_template, request, redirect, url_for, flash, session
import re

import json

PAISES_FILE = 'paises.json'
PRECIOS_IMPUESTOS_FILE = 'precios_impuestos.json'

# Utilidades para países
def cargar_paises():
    try:
        with open(PAISES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_paises(paises):
    with open(PAISES_FILE, 'w', encoding='utf-8') as f:
        json.dump(paises, f, ensure_ascii=False, indent=2)

# Utilidades para precios e impuestos
def cargar_precios_impuestos():
    try:
        with open(PRECIOS_IMPUESTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_precios_impuestos(data):
    with open(PRECIOS_IMPUESTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mensajes flash y sesión

DATA_FILE = 'user_data.txt'
PRODUCTS_FILE = 'productos.json'

EMAIL_REGEX = r'^([\w\.-]+)@([\w\.-]+)\.([a-zA-Z]{2,})$'


# --- LOGIN ---
def leer_usuarios():
    usuarios = []
    nombre = None
    correo = None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('Nombre:'):
                    nombre = line.split(':', 1)[1].strip()
                elif line.startswith('Correo:'):
                    correo = line.split(':', 1)[1].strip()
                if nombre and correo:
                    usuarios.append({'nombre': nombre, 'correo': correo})
                    nombre = None
                    correo = None
    except FileNotFoundError:
        pass
    return usuarios

def agregar_usuario(nombre, correo):
    # Limpiar nombre y correo de espacios y saltos de línea
    nombre = nombre.strip().replace('\n', ' ')
    correo = correo.strip().replace('\n', '')
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(f'Nombre: {nombre}\nCorreo: {correo}\n')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Ingrese su correo electrónico.', 'error')
        else:
            usuarios = leer_usuarios()
            for usuario in usuarios:
                correo_usuario = usuario['correo'].strip().lower()
                if correo_usuario == email:
                    session['user_email'] = correo_usuario
                    flash('Inicio de sesión exitoso.', 'success')
                    return redirect(url_for('dashboard'))
            flash('Correo no registrado. Regístrese primero.', 'error')
    return render_template('login.html')
# Panel principal/dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        flash('Debe iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Rutas para cada sección
@app.route('/paises')
def paises():
    if 'user_email' not in session:
        flash('Debe iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    paises = cargar_paises()
    return render_template('paises.html', paises=paises)

@app.route('/precios_impuestos')
def precios_impuestos():
    if 'user_email' not in session:
        flash('Debe iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    productos = cargar_productos()
    paises = cargar_paises()
    monedas = ['CRC', 'USD', 'EUR', 'BRL']
    return render_template('precios_impuestos.html', productos=productos, paises=paises, monedas=monedas)

@app.route('/consulta')
def consulta():
    if 'user_email' not in session:
        flash('Debe iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    productos = cargar_productos()
    paises = cargar_paises()
    monedas = ['CRC', 'USD', 'EUR', 'BRL']
    return render_template('consulta.html', productos=productos, paises=paises, monedas=monedas)

# --- CARGAR USUARIO DESDE TXT EN LOGIN ---
@app.route('/login/cargar', methods=['POST'])
def login_cargar():
    file = request.files.get('file')
    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        # Sobrescribe el archivo de usuarios con el contenido cargado
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        flash('Usuarios cargados correctamente. Ahora puede iniciar sesión con un correo válido.', 'success')
    else:
        flash('Por favor, seleccione un archivo .txt válido.', 'error')
    return redirect(url_for('login'))

# --- REGISTRO ---
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Todos los campos son requeridos.', 'error')
        elif not re.match(EMAIL_REGEX, email):
            flash('El correo electrónico no es válido.', 'error')
        else:
            # Verificar si el correo ya existe
            usuarios = leer_usuarios()
            for usuario in usuarios:
                if usuario['correo'].lower() == email.lower():
                    flash('El correo ya está registrado. Inicie sesión.', 'error')
                    return redirect(url_for('registrar'))
            agregar_usuario(name, email)
            flash('¡Registro exitoso! Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('login'))
    return render_template('index.html')

# El registro también puede cargar datos desde archivo
@app.route('/registrar/cargar', methods=['POST'])
def registrar_cargar():
    file = request.files.get('file')
    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        flash('Usuarios cargados correctamente. Ahora puede iniciar sesión con un correo válido.', 'success')
    else:
        flash('Por favor, seleccione un archivo .txt válido.', 'error')
    return redirect(url_for('registrar'))


# --- Gestión de productos ---
def cargar_productos():
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_productos(productos):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)

@app.route('/productos', methods=['GET'])
def productos():
    if 'user_email' not in session:
        flash('Debe iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    productos = cargar_productos()
    consulta_resultado = None
    return render_template('productos_gestion.html', productos=productos, consulta_resultado=consulta_resultado)

# Añadir país
@app.route('/paises/agregar', methods=['POST'])
def agregar_pais():
    nombre = request.form.get('nombre_pais', '').strip()
    if not nombre:
        flash('El nombre del país es requerido.', 'error')
    else:
        paises = cargar_paises()
        if nombre in paises:
            flash('El país ya está registrado.', 'error')
        else:
            paises.append(nombre)
            guardar_paises(paises)
            flash('País agregado exitosamente.', 'success')
    return redirect(url_for('productos'))

# Registrar precio e impuesto para producto y país
@app.route('/precios_impuestos/agregar', methods=['POST'])
def agregar_precio_impuesto():
    producto = request.form.get('producto_precio')
    pais = request.form.get('pais_precio')
    moneda = request.form.get('moneda_precio')
    try:
        precio = float(request.form.get('precio_valor'))
        impuesto = float(request.form.get('impuesto_valor'))
    except (TypeError, ValueError):
        flash('Precio e impuesto deben ser números.', 'error')
        return redirect(url_for('productos'))
    if not producto or not pais or not moneda:
        flash('Todos los campos son requeridos.', 'error')
        return redirect(url_for('productos'))
    data = cargar_precios_impuestos()
    # Buscar si ya existe registro para ese producto y país
    for entry in data:
        if entry['producto'] == producto and entry['pais'] == pais:
            entry['precio'] = precio
            entry['impuesto'] = impuesto
            entry['moneda'] = moneda
            break
    else:
        data.append({'producto': producto, 'pais': pais, 'precio': precio, 'impuesto': impuesto, 'moneda': moneda})
    guardar_precios_impuestos(data)
    flash('Precio e impuesto registrados/actualizados.', 'success')
    return redirect(url_for('productos'))

# Consulta avanzada de producto por país
@app.route('/productos/consulta_avanzada', methods=['GET'])
def consulta_avanzada():
    producto = request.args.get('producto_consulta')
    moneda_destino = request.args.get('moneda_consulta')
    paises = cargar_paises()
    productos = cargar_productos()
    precios_impuestos = cargar_precios_impuestos()
    monedas = ['CRC', 'USD', 'EUR', 'BRL']
    resultado = []
    # Tasas de cambio (ejemplo, pueden ser actualizadas)
    tasas = {
        'CRC': 1,
        'USD': 540,
        'EUR': 590,
        'BRL': 110
    }
    if producto and moneda_destino:
        for pais in paises:
            entry = next((e for e in precios_impuestos if e['producto'] == producto and e['pais'] == pais), None)
            if entry:
                # Convertir precio a moneda destino
                precio_crc = entry['precio'] * tasas[entry['moneda']] if entry['moneda'] != 'CRC' else entry['precio']
                precio_destino = precio_crc / tasas[moneda_destino]
                impuesto = entry['impuesto']
                costo_total = precio_destino + (precio_destino * impuesto)
                resultado.append({
                    'pais': pais,
                    'precio': round(precio_destino, 2),
                    'impuesto': impuesto,
                    'costo_total': round(costo_total, 2),
                    'moneda': moneda_destino
                })
            else:
                resultado.append({'pais': pais, 'precio': 'N/A', 'impuesto': 'N/A', 'costo_total': 'N/A', 'moneda': moneda_destino})
    consulta_resultado = resultado if resultado else None
    return render_template('productos.html', productos=productos, paises=paises, precios_impuestos=precios_impuestos, consulta_resultado=consulta_resultado, monedas=monedas)

@app.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form.get('nombre', '').strip()
    precio = request.form.get('precio', '').strip()
    if not nombre or not precio:
        flash('Todos los campos son requeridos para agregar producto.', 'error')
    else:
        try:
            precio = float(precio)
        except ValueError:
            flash('El precio debe ser un número.', 'error')
            return redirect(url_for('productos'))
        productos = cargar_productos()
        productos.append({'nombre': nombre, 'precio': precio})
        guardar_productos(productos)
        flash('Producto agregado exitosamente.', 'success')
    return redirect(url_for('productos'))

@app.route('/productos/modificar', methods=['POST'])
def modificar_producto():
    id = request.form.get('id')
    nuevo_nombre = request.form.get('nuevo_nombre', '').strip()
    nuevo_precio = request.form.get('nuevo_precio', '').strip()
    productos = cargar_productos()
    try:
        id = int(id)
        if id < 0 or id >= len(productos):
            flash('Producto no encontrado.', 'error')
            return redirect(url_for('productos'))
        if nuevo_nombre:
            productos[id]['nombre'] = nuevo_nombre
        if nuevo_precio:
            try:
                productos[id]['precio'] = float(nuevo_precio)
            except ValueError:
                flash('El precio debe ser un número.', 'error')
                return redirect(url_for('productos'))
        guardar_productos(productos)
        flash('Producto modificado exitosamente.', 'success')
    except Exception:
        flash('Error al modificar producto.', 'error')
    return redirect(url_for('productos'))

@app.route('/productos/borrar', methods=['POST'])
def borrar_producto():
    id = request.form.get('id')
    productos = cargar_productos()
    try:
        id = int(id)
        if id < 0 or id >= len(productos):
            flash('Producto no encontrado.', 'error')
        else:
            productos.pop(id)
            guardar_productos(productos)
            flash('Producto borrado exitosamente.', 'success')
    except Exception:
        flash('Error al borrar producto.', 'error')
    return redirect(url_for('productos'))

@app.route('/productos/consultar', methods=['GET'])
def consultar_producto():
    consulta = request.args.get('consulta', '').strip().lower()
    productos = cargar_productos()
    resultado = None
    if consulta:
        for p in productos:
            if p['nombre'].lower() == consulta:
                resultado = f"Producto: {p['nombre']}<br>Precio: ${p['precio']}"
                break
        if not resultado:
            resultado = 'Producto no encontrado.'
    else:
        resultado = 'Ingrese un nombre para consultar.'
    return render_template('productos.html', productos=productos, consulta_resultado=resultado)


# --- CERRAR SESIÓN ---
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
