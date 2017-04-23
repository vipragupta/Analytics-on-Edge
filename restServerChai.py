from flask import Flask, jsonify, request
#from flaskext.mysql import MySQL
import json

app = Flask(__name__)



@app.route('/post', methods=['GET', 'POST'])
def mypost():
    print "I am here"
    try:
        print "I am here again"
        if(request.method == 'POST'):
            print "Request: " + str(request)
            print request.json

            return jsonify({'StatusCode':'200','Message': 'Success'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)