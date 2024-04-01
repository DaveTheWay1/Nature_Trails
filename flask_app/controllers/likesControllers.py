from flask import request, redirect, session, flash
from flask_app.models.like import Like
from flask_app import app

@app.route('/like', methods=['POST'])
def like_post():
    if 'user_id' not in session:
        return redirect('/home')

    post_id = request.form['post_id']
    user_id = session['user_id']

    existing_like = Like.getLikeByPostAndUser(post_id, user_id)
    if existing_like:
        Like.deleteLike(existing_like.id)
    else:
        data = {
            'post_id': post_id,
            'user_id': user_id
        }
        Like.saveLike(data)

    return redirect(f'/view/post/{post_id}')
