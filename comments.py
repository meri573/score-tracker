import db

def add_comment(result_id, content, user_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, result_id)
            VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, result_id])

def get_comments(result_id):
    sql = """SELECT u.username, c.content, c.user_id, c.sent_at 
            FROM comments c, users u
            WHERE c.user_id = u.id AND c.result_id = ?"""
    return(db.query(sql, [result_id]))

def get_user_comments(user_id):
    sql = """SELECT content, sent_at, result_id
            FROM comments
            WHERE user_id = ?"""
    return(db.query(sql, [user_id]))