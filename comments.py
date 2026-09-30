import db

def add_comment(result_id, content, user_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, result_id)
            VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, result_id])

def get_comments(result_id):
    sql = """SELECT u,username c.content, c.user_id, c.sent_at 
            FROM comments c, users u 
            WHERE c.user_id = u.id AND result_id = ?"""
    db.execute(sql, [result_id])

def get_users_comments(user_id):
    sql = """SELECT content, sent_at 
            FROM comments
            WHERE user_id = ?"""
    db.execute(sql, [user_id])