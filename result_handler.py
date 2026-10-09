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

def add_result(time, score, description, user_id, classes):
    sql = """INSERT INTO results (time, score, description, submitted_at, user_id) 
            VALUES (?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [time, score, description, user_id])

    result_id = db.las_insert_id()

    sql = "INSERT INTO result_classes (result_id, title, value) VALUES (?,?,?)"
    for class_title, class_value in classes:
        print(class_title, class_value)
        db.execute(sql, [result_id, class_title, class_value])

def update_result(result_id, description):
    sql = "UPDATE results SET description = ? WHERE id = ?"
    db.execute(sql, [description, result_id])

def delete_result(result_id):
    sql = "DELETE FROM results WHERE id = ?"
    db.execute(sql, [result_id])

def search_results(query):
    sql = """SELECT u.username, r.id, r.time, r.score, r.submitted_at
            FROM users u, results r, result_classes c
            WHERE r.user_id = u.id AND r.id = c.result_id AND (u.username LIKE ? OR r.time LIKE ? OR r.score LIKE ? OR r.submitted_at LIKE ? OR c.value LIKE ?)
            ORDER BY r.submitted_at desc"""
    #sql = "SELECT u.username, r.id, r.time, r.score, r.submitted_at FROM users u, results r, result_classes c WHERE r.user_id = u.id AND r.id = c.result_id AND (u.username LIKE ? OR r.time LIKE ? OR r.score LIKE ? OR r.submitted_at LIKE ? OR c.value LIKE ?)"
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like, like])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title]=[]
    for title, value in result:
        classes[title].append(value)

    print(classes["rule"])
    print(classes["game"])

    return classes

def get_classes(result_id):
    sql = "SELECT title, value FROM result_classes WHERE result_id = ? ORDER BY id"
    temp = db.query(sql, [result_id])
    print(temp)
    for result in temp:
        for thing in result:
            print(thing)
    classes = {}
    for title, value in temp:
        classes[title]=[]
    for title, value in temp:
        classes[title].append(value)
    print(classes)
    return classes