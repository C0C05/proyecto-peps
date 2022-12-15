import os
def cargarVariables():
    os.environ['DB_USERNAME']='root'
    os.environ['DB_PASSWORD']='1234'
    os.environ['DB_DATABASE']='db_exploits'
    os.environ['DB_HOST']='mysql'
    os.environ['DB_PORT']='3306'
    os.environ['PORT']='8080'
    os.environ['HOST']='0.0.0.0'
