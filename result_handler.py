import db

def get_results():
    sql = """SELECT u.username, r.id, r.game, r.result_time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at
            FROM users u, results r  
            WHERE r.user_id = u.id"""
    print(sql)
    temp = db.query(sql)
    print(temp)

    return db.query(sql)


#, r.result_time, r.grade, r.score, r.twentyg_mode, r.big_mode, r.submitted_at r.user_id 