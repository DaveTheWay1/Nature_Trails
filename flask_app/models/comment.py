from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models.user import User
mydb = 'project_views'  

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comments_content = data['comments_content']
        self.post_id = data['post_id']
        self.user_id = data['user_id']
        self.creator = User.getById({'id': self.user_id})
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def saveComment(cls, data):
        query = """
        INSERT INTO comments (comments_content, post_id, user_id)
        VALUES (%(comments_content)s, %(post_id)s, %(user_id)s)
        """
        comment_id = connectToMySQL(mydb).query_db(query, data)
        return comment_id
    
    @classmethod
    def getCommentsByPostId(cls, data):
        query = """
        SELECT * FROM comments
        WHERE post_id = %(post_id)s
        """
        results = connectToMySQL(mydb).query_db(query, data)
        comments = []
        for result in results:
            comment = cls(result)
            comment.creator = User.getById({'id': comment.user_id})
            comments.append(comment)
        return comments
    
    @classmethod
    def getCommentById(cls, comment_id):
        query = """
        SELECT * FROM comments
        WHERE id = %(comment_id)s
        """
        data = {'comment_id': comment_id}
        result = connectToMySQL(mydb).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    @classmethod
    def deleteCommentById(cls, comment_id):
        query = """
        DELETE FROM comments
        WHERE id = %(comment_id)s
        """
        data = {'comment_id': comment_id}
        connectToMySQL(mydb).query_db(query, data)