from flask_app.config.mysqlconnection import connectToMySQL 
mydb = 'project_views' 
import os
import uuid
from flask_app.models.user import User 
from flask_app.models.comment import Comment
from flask import flash 

class Post: 
    def __init__(self,data):
        self.id = data['id'] 
        self.location_name = data['location_name']
        self.img_path =  data['img_path']
        self.review = data['review']
        self.address = data['address']
        self.creator = None
        self.comments = []

    @staticmethod
    def validate_create(request): 
        is_valid = True 
        if len(request['location_name']) < 4: 
            flash('Location name must be longer than 4 Characters') 
            is_valid = False 
        if len(request['review']) <4:
            flash('Review Must Be Longer Than 4 Characters') 
            is_valid = False 
        return is_valid

    @classmethod 
    def save(cls,data): 
        query = '''
        INSERT INTO posts
        (location_name, img_path, review, address, user_id)
        VALUES (%(location_name)s, %(img_path)s, %(review)s, %(address)s, %(user_id)s);'''
        results = connectToMySQL(mydb).query_db(query,data) 
        print(f"results: {results}") 
        return results 
    
    @staticmethod
    def save_image(image, upload_folder):
        if not image:
            return None

        filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]

        image.save(os.path.join(upload_folder, filename))

        return filename
    

    @classmethod
    def deleteById(cls,data):
        query  = '''
        DELETE FROM posts
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query,data)
        print('it gets here')
        return results

    @classmethod
    def update(cls, data):
        query = '''
        UPDATE posts
        SET location_name = %(location_name)s,
        review = %(review)s,
        img_path = %(img_path)s,
        address = %(address)s
        WHERE id = %(id)s;
        '''
        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts LEFT JOIN users ON users.id = posts.user_id;"
        results = connectToMySQL(mydb).query_db(query)
        lst = []
        for i in results: 
            obj = cls(i)
            temp = { 
                'id':i['users.id'], 
                'first_name':i['first_name'],
                'last_name':i['last_name'],
                'email':i['email'], 
                'password':i['password'], 
                'created_at':i['users.created_at'], 
                'updated_at':i['users.updated_at'], 
            }
            obj.creator= User(temp) 
            lst.append(obj)
        return lst 

    @classmethod
    def getById(cls, data):
        query = '''
        SELECT * FROM posts
        LEFT JOIN users ON users.id = posts.user_id
        WHERE posts.id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        if results:
            post_data = results[0]
            this_post = cls(post_data)
            this_post.comments = Comment.getCommentsByPostId({'post_id': this_post.id})
            this_post_creator = {
                'id': post_data['users.id'],
                'first_name': post_data['first_name'],
                'last_name': post_data['last_name'],
                'email': post_data['email'],
                'password': post_data['password'],
                'created_at': post_data['users.created_at'],
                'updated_at': post_data['users.updated_at'],
            }
            this_post.creator = User(this_post_creator)
            return this_post
        return None
    
    @classmethod
    def getByPath(cls,data):
        print(data)
        query = '''
        SELECT * FROM posts
        WHERE posts.img_path = %(img_path)s;
        '''
        results = connectToMySQL(mydb).query_db(query,data)
        print(f"results: {results}")
        return results 


    @classmethod
    def getPostsByUserId(cls, user_id):
        query = '''
        SELECT * FROM posts
        WHERE user_id = %(user_id)s;
        '''
        data = {'user_id': user_id}
        results = connectToMySQL(mydb).query_db(query, data)
        posts = []
        for result in results:
            post = Post(result)
            posts.append(post)
        return posts
