from flask import Flask,jsonify,request
from os import *
import subprocess
import zipfile
import commands
app = Flask(__name__)
@app.route("/upgrade")
def ipatch():
        with zipfile.ZipFile("/root/flask/patch.zip", 'r') as zip_ref:
                zip_ref.extractall("/root/flask/")
        cmd="bash /root/flask/patch/s2.sh"
        system(cmd)
        return jsonify({"Status": "Patch install started" ,"log location": "/tmp/upgradelog"})

@app.route("/helm")
def systeminfo():
          #environ["HELM_HOME"]="/root/.helm"
          #cmd="bash /tmp/helm.sh"
          #system(cmd)
          #output = subprocess.check_output(["cat","/tmp/tt" ])
          output = subprocess.check_output([ "helm" ,  "ls" , "--home" , "/root/.helm" , "--kubeconfig" , "/root/.kube/config"])
          return(output)

@app.route('/run', methods=['POST'])
def run():
         data = request.get_json()
         cmd  = data["cmd"] 
         system(cmd)
         return cmd 
                    
@app.route('/out', methods=['POST'])
def out():
     data = request.get_json()
     cmd  = data["cmd"]
     l=commands.getoutput(cmd)
     print(type(l))
     #output = subprocess.check_output('cmd')
     return (l)

app.run(host='0.0.0.0')

