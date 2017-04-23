from flask import Flask, jsonify, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Abcd@1234'
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.route('/post', methods=['GET', 'POST'])
def mypost():
    try:
        print "########\n"
        print(request.json)
        email = request.json.get('email')
        password = request.json.get('password')
        print email 
        print password
        print "########\n"
        cursor.callproc('spCreateUser',(email, password))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return jsonify({'StatusCode':'200','Message': 'User creation success'})
        else:
            return jsonify({'StatusCode':'1000','Message': str(data[0])})

        return jsonify({'Email': args['email'], 'Password': args['password']})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
