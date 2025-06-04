from .db import Database

def save_keyword_to_db(db,results):
    if not isinstance(results, list):
        results = [results]  # 确保results是一个列表
    for result in results:
        rank = result.get('rank')
        keyword = result.get('keyword')
        url = result.get('url')
        if rank and keyword and url:
             sql="INSERT INTO keywords (ranking, keyword, url) VALUES (%s, %s, %s)"
             params=(rank, keyword, url)
             db.execute(sql, params)
    return 

def save_posts_to_db(db, results):
    if not isinstance(results, list):
        results = [results]  # 确保results是一个列表
    for result in results:
        keyword = result.get('keyword')
        content = result.get('content')
        tags = result.get('tags')
        sql = "INSERT INTO posts (keyword, content,tags) VALUES (%s, %s,%s)"
        params = (keyword, content,tags)
        db.execute(sql, params)
    return 

def search_posts_by_keyword(db, keyword):
    sql = "SELECT * FROM posts WHERE content LIKE %s"
    params = ('%' + keyword + '%',) #对关键词进行模糊查找
    return db.fetch_all(sql, params)

def get_all_posts(db):
    sql = "SELECT * FROM posts"
    rows= db.fetch_all(sql)
    keys=['id', 'content', 'keyword', 'tags', 'sentiment']

    return [dict(zip(keys, row)) for row in rows] 

def insert_sentiment_to_db(db,id,sentiment):
    sql = "UPDATE posts SET sentiment = %s WHERE id = %s"
    params = (sentiment, id)
    db.execute(sql, params) 


