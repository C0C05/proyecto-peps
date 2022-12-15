from __future__ import print_function
from __main__ import app
from flask import request,session,redirect,send_file
from bd import obtener_conexion
import json
import sys
import logging


@app.before_request
def before_request():
    if request.path != '/static/index.html' and request.path != '/static/registro.html' and request.path != '/static/functions.js':
        if request.path.startswith('/static') and 'user' not in session:
            return redirect('/static/index.html')

@app.route('/whoami', methods=['GET'])
def whoami():
    ret={"user": "{}".format(session["user"]) }
    code=200
    return json.dumps(ret), code


@app.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        cred_json = request.json
        username = cred_json['username']
        hash = cred_json['hash']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                 #cursor.execute("SELECT perfil FROM users WHERE user = %s and passHash= %s",(username,hash))
                 cursor.execute("SELECT user FROM users WHERE user = '" + username +"' and passHash= '" + hash + "'")
                 user = cursor.fetchone()
                 if user is None:
                     print("INSERT INTO users(user,passHash) VALUES('"+ username +"','"+  hash+"')") 
                     cursor.execute("INSERT INTO users(user,passHash) VALUES('"+ username +"','"+  hash+"')")
                     if cursor.rowcount == 1:
                         conexion.commit()
                         ret={"status": "OK" }
                         code=200
                     else:
                         ret={"status": "ERROR" }
                         code=500
                 else:
                   ret = {"status": "ERROR","mensaje":"user/pass erroneo" }
                   code=200
            conexion.close()
        except:
            print("Excepcion al registrar al user")   
            ret={"status":"ERROR"}
            code=500
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code
    
@app.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        cred_json = request.json
        username = cred_json['username']
        hash = cred_json['hash']
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT passHash FROM users WHERE user = '" + username +"' and passHash= '" + hash + "'")
                usuario = cursor.fetchone()
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
                code = 401
            else:
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE users set accessDate = now() where user = '{}'".format(username))
                ret = {"status": "OK" }
                session["user"]=username
                session["hash"]=usuario[0]
                code=200
        except:
            print("Excepcion al validar al usuario")   
            ret={"status":"ERROR"}
            code=500
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/logout",methods=['GET'])
def logout():
    session.clear()
    return json.dumps({"status":"OK"}),200
