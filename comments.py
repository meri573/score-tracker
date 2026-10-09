import db

def add_comment(result_id, content, user_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, result_id)
            VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, result_id])

def get_comments(result_id):
    sql = """SELECT u.username, c.id, c.content, c.user_id, c.sent_at 
            FROM comments c, users u
            WHERE c.user_id = u.id AND c.result_id = ?
            ORDER BY c.sent_at DESC"""
    return(db.query(sql, [result_id]))

def get_comment(comment_id):
    sql = "SELECT id, content, result_id, user_id FROM comments WHERE id = ?"
    comment = db.query(sql, [comment_id])
    return comment[0] if comment else None

def get_user_comments(user_id):
    sql = """SELECT id, content, sent_at, result_id
            FROM comments
            WHERE user_id = ?
            ORDER BY sent_at DESC"""
    return(db.query(sql, [user_id]))

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])