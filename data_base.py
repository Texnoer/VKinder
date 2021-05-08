import sqlalchemy


db = ''
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

def save_database(profile_user, result):
    name = profile_user["name"] + ' ' + profile_user["last_name"]
    connection.execute('''INSERT INTO iduser(userid, name, likeuser) VALUES(%s, %s, %s);''', (profile_user["id"], name, result))

def check_id_user(iduser):
    response = connection.execute('''SELECT * FROM iduser 
                                        WHERE userid = %s;''', (iduser)).fetchall()
    if len(response) == 0:
        return True