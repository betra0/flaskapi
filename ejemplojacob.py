

from flask import Flask, request, jsonify
import mysql.connector 

configbd = {
                'host': 'localhost',
                'user': 'root',
                'port': 3306,
                'password': '12345',
                'database':'apitest',
}

app = Flask(__name__)

""" 
            verbos HTTP
GET: Solicita datos del servidor
POST: Envía datos al servidor
PUT: Actualiza un recurso existente en el servidor.
PATCH: permite modificar solo los campos que se desean modificar en el recurso
DELETE: Elimina un recurso específico en el servidor.
 """


@app.route("/", methods=['GET', 'POST']) #endpoint
def raiz():
    if request.method == 'GET':
        return "esta ES LA RAIZ usado GET"
    else:
        return "esta ES LA RAIZ usado post  o otro "
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        #Guadar usuarios que manda el cliente a la api en la bd
        datain = request.get_json()
        name =datain.get('name')
        edad = datain.get('edad')
        mail = datain.get('mail')
        """ contraseña = datain.get('password') """
        #conectar con bd 
        conexion = mysql.connector.connect(**configbd)
        cursor = conexion.cursor()

        try:
            sql = "INSERT INTO usuarios (nombre, mail, edad) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, mail, int(edad)))

            conexion.commit()
            

            return jsonify({'success': True, 'message':'Consulta con exito'}), 200
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message':'error en la peticion',
                            'error': str(e)}), 500
        finally:
            cursor.close()
            conexion.close()
            #lo que esta aca se ejecuta si o si 

    elif request.method == 'GET':
        # MANDARLE los user de la bd al cliente
        #recuperar datos el la query
        name = request.args.get('name', default="", type=str)  # Parámetro opcional, por defecto será una cadena vacía
        
        edad = request.args.get('edad', default=None, type=int)
        print('edad', edad, type(edad))

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

            

        conexion = mysql.connector.connect(**configbd)
        cursor = conexion.cursor(dictionary=True)
        try:
            sql = f"SELECT id, nombre, mail, edad FROM usuarios {where}"
            cursor.execute(sql, parametros)
            resultados = cursor.fetchall()
            

            return jsonify({'success': True, 'message':'Consulta con exito',
                            'data':resultados}), 200
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message':'error en la peticion',
                            'error': str(e)}), 500
        finally:
            cursor.close()
            conexion.close()
    
    return 'User'

#desplegar un servidor web de DESARROLLO con tu api
if __name__ == '__main__':
    #esto se ejecuta solo en desarrollo
    app.run( debug= True, port=5000, host='0.0.0.0')