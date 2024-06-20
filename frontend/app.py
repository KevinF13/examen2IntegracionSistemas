from flask import Flask, render_template, request, jsonify
import requests
import random
import csv
from io import TextIOWrapper

app = Flask(__name__)

def get_random_pokemon_image():
    pokemon_id = random.randint(1, 898)  # Asumiendo que hay 898 Pokémon en la PokeAPI
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    data = response.json()
    return data['sprites']['front_default']

def obtener_producto_por_id(product_id):
    try:
        url = f'http://127.0.0.1:5000/inventario/{product_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener el producto - Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener el producto: {str(e)}")
        return None

def obtener_orden_compra_por_id(orden_id):
    try:
        url = f'http://127.0.0.1:5000/ordenCompra/{orden_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener la orden de compra - Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener la orden de compra: {str(e)}")
        return None

@app.route('/')
def home():
    inventario_data = obtener_inventario()
    for producto in inventario_data:
        producto['imagen'] = get_random_pokemon_image()
    return render_template('ordenes.html', inventario_data=inventario_data)

@app.route('/inventario')
def inventario():
    inventario_data = obtener_inventario()
    return render_template('inventario.html', inventario_data=inventario_data)

@app.route('/facturacion')
def facturacion():
    orden_id = request.args.get('id')
    orden = None
    if orden_id:
        orden = obtener_orden_compra_por_id(orden_id)
    return render_template('facturacion.html', orden=orden)

@app.route('/actualizarDesdeCSV', methods=['POST'])
def actualizar_desde_csv():
    try:
        if 'archivo_csv' not in request.files:
            return jsonify({"error": "No se ha proporcionado un archivo CSV"}), 400
        
        csv_file = request.files['archivo_csv']
        
        if csv_file.filename == '':
            return jsonify({"error": "El nombre del archivo está vacío"}), 400
        
        if not csv_file.filename.endswith('.csv'):
            return jsonify({"error": "El archivo no es un archivo CSV válido"}), 400
        
        # Leer el contenido del archivo CSV
        csv_text = TextIOWrapper(csv_file.stream, encoding='utf-8')
        csv_reader = csv.DictReader(csv_text)

        data_to_send = []
        for row in csv_reader:
            # Construir el objeto JSON esperado por la API de actualización
            data_to_update = {
                "Cantidad": int(row['Cantidad']),
                "IdProducto": int(row['IdProducto']),
                "NombreProducto": row['NombreProducto'],
                "Precio": row['Precio']
            }
            data_to_send.append(data_to_update)
        
        # Hacer la solicitud PUT para actualizar el inventario por cada línea del CSV
        url = 'http://127.0.0.1:5000/actualizarInventario'
        for data_update in data_to_send:
            response = requests.put(url, json=data_update)
            if response.status_code != 200:
                return jsonify({"error": f"Error al actualizar el inventario: {response.text}"}), response.status_code
        
        # Obtener el inventario actualizado para renderizar la página inventario.html
        inventario_data = obtener_inventario()
        return render_template('inventario.html', inventario_data=inventario_data)
    
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo CSV: {str(e)}"}), 500

def obtener_inventario():
    try:
        url = 'http://127.0.0.1:5000/inventario'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener el inventario - Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener el inventario: {str(e)}")
        return []

if __name__ == '__main__':
    app.run(debug=True, port=8080)
