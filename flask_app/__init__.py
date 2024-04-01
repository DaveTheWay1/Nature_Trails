from flask import Flask

UPLOAD_FOLDER = '/Users/ramirez-vazquez/Desktop/python_project/views/flask_app/uploads'


app = Flask(__name__)
app.secret_key = "hello"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER