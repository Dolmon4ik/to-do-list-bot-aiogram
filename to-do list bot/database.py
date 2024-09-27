import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users('id' INTEGER, \
                                                    'username' INTEGER, \
                                                    PRIMARY KEY('id' AUTOINCREMENT))")

    result = cur.execute("SELECT * FROM users").fetchall()
    print(result)
    cur.execute("CREATE TABLE IF NOT EXISTS notes('n_id' INTEGER, \
                                                    'user_id' INTEGER, \
                                                    'note' varchar(32), \
                                                    PRIMARY KEY('n_id' AUTOINCREMENT))")
    con.commit()

async def add_id(user_id):
    user = cur.execute("SELECT * FROM users WHERE username == {key}".format(key = user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users (username) VALUES ({key})".format(key = user_id))
        con.commit()

async def add_note(note_id, user_sender_id):
    cur.execute("INSERT INTO notes (note, user_id) VALUES ('{note}', '{id}')".format(note = str(note_id), id = user_sender_id))
    con.commit()


async def remove_note(note_id, user_sender_id):
    cur.execute("DELETE FROM notes WHERE note = ('{key}') AND user_id = ('{id}')".format(key = str(note_id), id = user_sender_id))
    con.commit()
