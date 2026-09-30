import db

def add_comment(result_id, content, user_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, result_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, result_id])