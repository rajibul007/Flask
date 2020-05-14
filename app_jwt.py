from flask import Flask , request , jsonify 
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from os import *
import subprocess
import zipfile
import commands
  
token1 = urandom(10)
    
print(token1) 



class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = token1

jwt = JWT(app, authenticate, identity)

@app.route('/out', methods=['POST'])
@jwt_required()
def out():
         data = request.get_json()
         cmd  = data["cmd"]
         out = system(cmd)
         if system(cmd) != 0 :
             return jsonify({"message": "BAD SHELL COMMAND" , "Eroor": out }),400

         l = commands.getoutput(cmd)
         print(type(l))
         return (l)

if __name__ == '__main__':

    app.run(host='0.0.0.0' , port=5000 )

