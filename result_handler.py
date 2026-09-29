import db

def get_results():
    sql = """SELECT u.username, r.user_id, r.id, r.game, r.time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at
            FROM users u, results r  
            WHERE r.user_id = u.id"""

    return db.query(sql)

def get_result(result_id):
    sql = """SELECT u.username, r.user_id, r.id, r.game, r.time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at, r.description
            FROM users u, results r  
            WHERE r.user_id = u.id AND r.id = ?"""

    result = db.query(sql, [result_id])
    return result[0] if result else None

def update_result(result_id, description):
    sql = "UPDATE results SET description = ? WHERE id = ?"
    db.execute(sql, [description, result_id])

def delete_result(result_id):
    sql = "DELETE FROM results WHERE id = ?"
    db.execute(sql, [result_id])

def search_results(query):
    sql = """SELECT u.username, r.id, r.game, r.time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at
            FROM users u, results r  
            WHERE r.user_id = u.id AND (u.username LIKE ? OR r.game LIKE ? OR r.time LIKE ? OR r.grade LIKE ? OR r.score LIKE ? OR r.submitted_at LIKE ?)"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like, like, like])