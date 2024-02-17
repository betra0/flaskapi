from flask import Flask, jsonify
import mysql.connector


""" 
            verbos HTTP
GET: Solicita datos del servidor
POST: Envía datos al servidor
PUT: Actualiza un recurso existente en el servidor.
PATCH: permite modificar solo los campos que se desean modificar en el recurso
DELETE: Elimina un recurso específico en el servidor.
 """


configdb = {
                'host': 'localhost',
                'user': 'dany',
                'port': 3306,
                'password': '12345',
                'database':'flask',
                }

app = Flask(__name__)




""" @app.route('/ruta', methods=['POST']) """
@app.route('/')
def raiz():
    return "Inicio"

@app.route('/data')
def getdata():
    connection = mysql.connector.connect(**configdb)
    cursor = connection.cursor()
    try:
        # la consulta con la bd 
        pass
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        

    return

@app.route('/contacto')
def contacto():
    return " estas en la pagina de contacto"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')