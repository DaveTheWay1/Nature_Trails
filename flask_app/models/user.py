from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$') 
mydb = 'project_views'  

class User: 
    def __init__(self,data):
        self.id = data['id'] 
        self.first_name = data['first_name']
        self.last_name = data['last_name'] 
        self.email = data['email'] 
        self.password = data['password'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_create(request):
        is_valid = True 
        if len(request['first_name']) < 1: 
            flash('Please Enter A First Name', 'regError') 
            is_valid = False 
        elif len(request['first_name']) <2: 
            flash('First Name Must Be At Least Two Characters', 'regError') 
            is_valid = False 
        if len(request['last_name']) < 1: 
            flash('Please Enter A Last Name', 'regError') 
            is_valid = False 
        elif len(request['last_name']) <2: 
            flash('Last Name Must Be At Least Two Characters', 'regError')
            is_valid = False 
        if len(request['email']) < 1: 
            flash('Please Enter An Email', 'regError') 
            is_valid = False
        if not EMAIL_REGEX.match(request['email']): 
            flash("Invalid email address!", 'regError') 
            is_valid = False 
        if len(request['password']) < 1:
            flash('Please Enter A Password', 'regError') 
            is_valid = False 
        elif len(request['password']) <8: 
            flash('Password Must Be At Least Eight Characters', 'regError')
            is_valid = False 
        if len(request['passConf']) < 1: 
            flash('Please Confirm Your Password', 'regError') 
            is_valid = False 
        elif request['password'] != request['passConf']: 
            flash('Passwords Do Not Match', 'regError') 
            is_valid = False 
        print(f"is_valid: {is_valid}") 
        return is_valid 

    @classmethod 
    def save(cls,data): 
        query = ''' 
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);''' 
        results = connectToMySQL(mydb).query_db(query,data) 
        print(f"results: {results}")
        return results 

    @classmethod 
    def getById(cls,data):
        print(data) 
        query = '''
        SELECT * FROM users
        WHERE id = %(id)s;''' 
        results = connectToMySQL(mydb).query_db(query,data) 
        print(f"results: {results}") 
        return cls(results[0]) 

    @classmethod
    def getByEmail(cls,data): 
        print(data)
        query = '''
        SELECT * FROM users
        WHERE email = %(email)s;'''
        results = connectToMySQL(mydb).query_db(query,data) 
        print(f"results: {results}") 
        if len(results) < 1: 
            return False 
        return cls(results[0])