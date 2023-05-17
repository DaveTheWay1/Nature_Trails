from flask import request, redirect, render_template, session, flash
from flask_app.models.post import Post 
from flask_app.models.user import User 
from flask_app import app
from flask_app.models.comment import Comment

@app.route('/post/comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect('/home')

    post_id = request.form['post_id']
    user_id = session['user_id']
    comments_content = request.form['comments_content']

    data = {
        'post_id': post_id,
        'user_id': user_id,
        'comments_content': comments_content
    }
    Comment.saveComment(data)

    return render_template('view_post.html',
        current_user = User.getById({'id': session['user_id']}), 
        post = Post.getById({'id':post_id}))

@app.route('/delete/comment', methods=['POST'])
def delete_comment():
    if 'user_id' not in session:
        return redirect('/home')

    comment_id = request.form['comment_id']
    comment = Comment.getCommentById(comment_id)

    if comment.creator.id != session['user_id']:
        flash('You do not have permission to delete this comment.')
    else:
        Comment.deleteCommentById(comment_id)

    return redirect(f'/view/post/{comment.post_id}')