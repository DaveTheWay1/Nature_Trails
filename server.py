from flask_app import app
from flask_app.controllers import usersControllers, postsControllers,login_regControllers, commentsControllers, likesControllers

upload_folder = app.config['UPLOAD_FOLDER']
if __name__=="__main__":
    app.run(port=5001, debug=True)