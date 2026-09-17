import db

def get_results():
    sql = """SELECT u.username, r.id, r.game, r.result_time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at
            FROM users u, results r  
            WHERE r.user_id = u.id"""
    print(sql)
    temp = db.query(sql)
    print(temp)

    return db.query(sql)

def get_result(result_id):
    sql = """SELECT u.username, r.id, r.game, r.result_time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at, r.result_description
            FROM users u, results r  
            WHERE r.user_id = u.id AND r.id = ?"""

    return db.query(sql, [result_id])

def delete_result(result_id):
    sql = "DELETE FROM results WHERE id = ?"
    db.execute(sql, [result_id])