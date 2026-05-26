from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config
import pymysql


# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Initialize extensions
mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='/static'  )

    app.config.from_object(Config)
    
