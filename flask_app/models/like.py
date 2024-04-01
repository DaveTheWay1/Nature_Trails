from flask_app.config.mysqlconnection import connectToMySQL 
mydb = 'project_views' 

class Like:
    def __init__(self, data):
        self.id = data['id']
        self.post_id = data['post_id']
        self.user_id = data['user_id']

    @classmethod
    def saveLike(cls, data):
            query = """
            INSERT INTO liked_posts (post_id, user_id)
            VALUES (%(post_id)s, %(user_id)s)
            """
            like_id = connectToMySQL(mydb).query_db(query, data)
            print(f"results: {like_id}") 
            print('5')
            return like_id

    @classmethod
    def deleteLike(cls, like_id):
        query = """
        DELETE FROM liked_posts
        WHERE id = %(like_id)s
        """
        data = {'like_id': like_id}
        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def getLikesByPostId(cls, data):
        query = """
        SELECT * FROM liked_posts
        WHERE post_id = %(post_id)s
        """
        results = connectToMySQL(mydb).query_db(query, data)
        likes = []
        for result in results:
            like = Like(result)
            likes.append(like)
        return likes
    
    @classmethod
    def getLikeByPostAndUser(cls, post_id, user_id):
        query = """
        SELECT * FROM liked_posts
        WHERE post_id = %(post_id)s AND user_id = %(user_id)s
        """
        data = {
            'post_id': post_id,
            'user_id': user_id
        }
        result = connectToMySQL(mydb).query_db(query, data)
        if result:
            return Like(result[0])
        else:
            return None
