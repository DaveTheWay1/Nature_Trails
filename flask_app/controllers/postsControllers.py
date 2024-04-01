import os
from flask import flash, render_template, request, redirect, session, url_for, send_from_directory 
from werkzeug.utils import secure_filename
from flask_app import app
# from flask import current_app
from flask_app.models.post import Post 
from flask_app.models.user import User 
from flask_app.models.like import Like


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create/post') 
def create_post(): 
    if not session['user_id']: 
        redirect('/home') 
    return render_template('create_post.html', current_user = User.getById({'id': session['user_id']})) 

@app.route('/save/new/post', methods=['post']) 
def save_new(): 
    if not session['user_id']: 
        return redirect('/home') 
    print('0')
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('1')
        print(file)
        print(file.filename)
        data = {
            'location_name':request.form['location_name'],
            'img_path':file.filename,
            'review':request.form['review'],
            'address': request.form['address'],
            'user_id':request.form['user_id']
        }
        print(data)
        Post.save(data)

    print("trying to save post")

    if not Post.validate_create(request.form):

        return redirect('/create/post') 

    print("2")
    print(request.form['location_name'])
    return redirect('/home') 



@app.route('/uploads/<filename>')
def download_file(filename):
    path = Post.getByPath({'img_path':filename})
    print('78')
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename) 

@app.route('/view/post/<int:post_id>')
def view_post(post_id):
    if 'user_id' not in session:
        return redirect('/home')

    post = Post.getById({'id': post_id})
    post.likes_count = len(Like.getLikesByPostId({'post_id': post_id}))

    current_user = User.getById({'id': session['user_id']})

    return render_template('view_post.html', post=post, current_user=current_user)


@app.route('/edit/post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    if 'user_id' not in session:
        return redirect('/home')
    post = Post.getById({'id': post_id})
    # if not post:
    #     flash('Post not found')
    #     return redirect('/home')

    location_name = request.form.get('location_name')
    review = request.form.get('review')
    address = request.form.get('address')
    image = request.files.get('img')

    upload_folder = app.config['UPLOAD_FOLDER']
    filename = Post.save_image(image, upload_folder)

    post.location_name = location_name
    post.review = review
    post.address = address
    post.img_path = filename

    data = {
        'id': post.id,
        'location_name': post.location_name,
        'review': post.review,
        'address': post.address,
        'img_path': post.img_path
    }

    post.update(data)

    return redirect('/home')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 'user_id' not in session:
        return redirect('/home')
    post = Post.getById({'id': post_id})
    if request.method == 'POST':

        location_name = request.form['location_name']
        img = request.files['img']
        review = request.form['review']
        address = request.form['address']

        post.location_name = location_name

        if img:
            img_path = Post.save_image(img, app)
            post.img_path = img_path
        post.review = review
        post.address = address

        post.update()

        return redirect(f'/view/post/{post.id}')
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect('/home')
    Post.deleteById({'id':post_id})
    return redirect('/myposts')

@app.route('/myposts')
def my_posts():
    if 'user_id' not in session:
        return redirect('/home')

    current_user_id = session['user_id']
    current_user = User.getById({'id': current_user_id})
    posts = Post.getPostsByUserId(current_user_id)
    if not posts:
        create_post_message = "Create a Post"
    else:
        create_post_message = None

    return render_template('myposts.html', current_user=current_user, posts=posts, create_post_message=create_post_message)
