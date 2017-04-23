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

            response = {'StatusCode':'200','Message':'Success',"distance" :"10.4","elevation":"5.1","active":"23","floors":"5.3","bp":"123/78","steps":"123","pulse":"98","date":"2017-04-23","hour":"3"}
            response = json.dumps(response)
            return response

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)