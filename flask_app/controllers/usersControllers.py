from flask_app import app
from flask import render_template, session
from flask_app.models.post import Post
from flask_app.models import user

@app.route('/home') 
def dashboard():
    if 'user_id' in session: 
        posts = Post.get_all()
    return render_template('home_page.html', posts=posts,
                        current_user = user.User.getById({'id': session['user_id']}))