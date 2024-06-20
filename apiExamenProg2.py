from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la conexión a las bases de datos
db_config_1 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'examen2bd1'
}

db_config_2 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'examen2bd2'
}

def connect_to_database(config):
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=3306  # Agregar el puerto por separado
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route('/ordenCompra', methods=['GET'])
def obtener_datos_bd1():
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 1"}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ordenCompra")
    resultados = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(resultados)


@app.route('/ordenCompra/<int:idOrden>', methods=['GET'])
def obtener_orden_compra_por_id(idOrden):
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 1"}), 500

    cursor = connection.cursor(dictionary=True)
    consulta = "SELECT * FROM ordenCompra WHERE IdOrden = %s"
    cursor.execute(consulta, (idOrden,))
    resultado = cursor.fetchone()

    cursor.close()
    connection.close()

    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({"error": "Orden de compra no encontrada"}), 404

@app.route('/inventario', methods=['GET'])
def obtener_datos_bd2():
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 2"}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventario")
    resultados = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(resultados)

@app.route('/inventario/<int:idProducto>', methods=['GET'])
def obtener_producto_por_id(idProducto):
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 2"}), 500

    cursor = connection.cursor(dictionary=True)
    consulta = "SELECT * FROM inventario WHERE IdProducto = %s"
    cursor.execute(consulta, (idProducto,))
    resultado = cursor.fetchone()

    cursor.close()
    connection.close()

    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404
    


@app.route('/insertarorden', methods=['POST'])
def agregar_dato_bd1():
    nuevo_dato = request.json
    connection = connect_to_database(db_config_1)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 1"}), 500

    cursor = connection.cursor()
    consulta = """
    INSERT INTO ordencompra (IdProducto, Cantidad, NombreProducto, Precio, NombreCliente, DireccionCliente, CedulaCliente, TelefonoCliente)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        nuevo_dato['IdProducto'], nuevo_dato['Cantidad'], nuevo_dato['NombreProducto'],
        nuevo_dato['Precio'], nuevo_dato['NombreCliente'], nuevo_dato['DireccionCliente'],
        nuevo_dato['CedulaCliente'], nuevo_dato['TelefonoCliente']
    )

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        id_insertado = cursor.lastrowid
        cursor.close()
        connection.close()
        return jsonify({"id": id_insertado}), 201
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al insertar el dato: {e}"}), 400

@app.route('/insertarinventario', methods=['POST'])
def agregar_dato_bd2():
    nuevo_dato = request.json
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos 2"}), 500

    cursor = connection.cursor()
    consulta = "INSERT INTO inventario (Cantidad, NombreProducto, Precio) VALUES (%s, %s, %s)"
    valores = (nuevo_dato['Cantidad'], nuevo_dato['NombreProducto'], nuevo_dato['Precio'])

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        id_insertado = cursor.lastrowid
        cursor.close()
        connection.close()
        return jsonify({"id": id_insertado}), 201
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al insertar el dato: {e}"}), 400

@app.route('/actualizarInventario', methods=['PUT'])
def actualizar_inventario():
    datos_actualizados = request.json
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500

    cursor = connection.cursor()
    consulta = """
    UPDATE inventario
    SET Cantidad = %s, NombreProducto = %s, Precio = %s
    WHERE IdProducto = %s
    """
    valores = (datos_actualizados['Cantidad'], datos_actualizados['NombreProducto'], datos_actualizados['Precio'], datos_actualizados['IdProducto'])

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"mensaje": "Inventario actualizado correctamente"}), 200
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al actualizar el inventario: {e}"}), 400

@app.route('/actualizarOrdenCompra', methods=['PUT'])
def actualizar_orden_compra():
    datos_actualizados = request.json
    connection = connect_to_database(db_config_1)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500

    cursor = connection.cursor()
    consulta = """
    UPDATE ordencompra
    SET IdProducto = %s, Cantidad = %s, NombreProducto = %s, Precio = %s, NombreCliente = %s,
        DireccionCliente = %s, CedulaCliente = %s, TelefonoCliente = %s
    WHERE IdOrden = %s
    """
    valores = (
        datos_actualizados['IdProducto'], datos_actualizados['Cantidad'], datos_actualizados['NombreProducto'],
        datos_actualizados['Precio'], datos_actualizados['NombreCliente'], datos_actualizados['DireccionCliente'],
        datos_actualizados['CedulaCliente'], datos_actualizados['TelefonoCliente'], datos_actualizados['IdOrden']
    )

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"mensaje": "Orden de compra actualizada correctamente"}), 200
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al actualizar la orden de compra: {e}"}), 400

@app.route('/eliminarInventario/<int:id>', methods=['DELETE'])
def eliminar_inventario(id):
    connection = connect_to_database(db_config_2)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500

    cursor = connection.cursor()
    consulta = "DELETE FROM inventario WHERE IdProducto = %s"
    valores = (id,)

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al eliminar el producto: {e}"}), 400

@app.route('/eliminarOrdenCompra/<int:id>', methods=['DELETE'])
def eliminar_orden_compra(id):
    connection = connect_to_database(db_config_1)
    if connection is None:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500

    cursor = connection.cursor()
    consulta = "DELETE FROM ordencompra WHERE IdOrden = %s"
    valores = (id,)

    try:
        cursor.execute(consulta, valores)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"mensaje": "Orden de compra eliminada correctamente"}), 200
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"error": f"Error al eliminar la orden de compra: {e}"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
