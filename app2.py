import random
import string
from flask import Flask , request , jsonify
#from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from os import *
import subprocess
#import zipfile
import commands

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

key=randomString(24)

system("kubectl delete secret bash")
sec=('kubectl create secret generic bash --from-literal=executor-key={}'.format(key) )
system(sec)

app = Flask(__name__)
app.debug = True
@app.route('/out/<string:apikey>', methods=['POST'])
def out(apikey):
      if [ apikey != key ]:
          return jsonify({"error": "Invalid key", "status_code": 401}) , 401

           

    data = request.get_json()
    cmd  = data["cmd"]
    out = system(cmd)
    if system(cmd) != 0 :
             return jsonify({"message": "BAD SHELL COMMAND" , "Eroor": out }),400

    l = commands.getoutput(cmd)
    print(type(l))
    return (l)

if __name__ == '__main__':
        app.run(host='0.0.0.0' , port=5020 )


