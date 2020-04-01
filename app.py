from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.secret_key = str(hash(str(time.time())+'123'))
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@127.0.0.1:3306/cold-transfer"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
