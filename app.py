from flask import Flask, jsonify, request
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
                'user': 'root',
                'port': 3306,
                'password': '12345',
                'database':'apitest',
                }

app = Flask(__name__)




""" @app.route('/ruta', methods=['POST']) """
@app.route('/')
def raiz():
    return "hola"

@app.route('/user', methods=['POST','GET'])
def user():

    if request.method =='GET':
        name = request.args.get('name', default="", type=str)  # Parámetro opcional, por defecto será una cadena vacía
        edad = request.args.get('edad', default=None, type=int)
        print(name, edad)
        connection = mysql.connector.connect(**configdb)
        cursor = connection.cursor(dictionary=True)
        where = ""
        count = 0
        parametros = []
        if name != '' or edad != None:
            where = "where"
            
            if name != '':
                where = f'{where} nombre = %s'
                count += 1
                parametros.append(name)
            if edad != None:
                if count ==1:
                    where = f'{where} AND'
                where = f'{where} edad = %s'
                parametros.append(edad)
            print(f'este es el where: {where}')

        try:
            # Consulta SQL para insertar un nuevo usuario
            sql = f"SELECT * FROM usuarios {where}"
            cursor.execute(sql, parametros)
            resultados = cursor.fetchall()
            
            print(resultados)
            return jsonify({'success': True, 'message':'Consulta con exito', 'data':resultados}), 200

        except Exception as e:
            print(str(e))
            return jsonify({'success': False, 'message':'error en la peticion','error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    


    
    elif request.method == 'POST':
        datain =  request.get_json()
        nombre = datain.get('name') 
        edad = datain.get('edad')
        mail = datain.get('mail')

        print(datain)
        print(nombre)

        connection = mysql.connector.connect(**configdb)
        cursor = connection.cursor()
        
        try:
            # Consulta SQL para insertar un nuevo usuario
            sql = "INSERT INTO usuarios (nombre, mail, edad) VALUES (%s, %s, %s)"

            # Ejecuta la consulta SQL
            cursor.execute(sql, (nombre, mail, int(edad)))
            connection.commit()
            return jsonify({'success': True, 'message':'Consulta con exito'}), 200

        except Exception as e:
            print(str(e))
            return jsonify({'success': False, 'message':'error en la peticion','error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

        

    

@app.route('/contacto')
def contacto():
    return " estas en la pagina de contacto"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')