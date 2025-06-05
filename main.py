#from scripts import db_session
from games.black import blackgak
from scripts.initing import init_db
import sqlite3


init_db()
conn = sqlite3.connect('db/project.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM users")
users = [i[0] for i in cursor.fetchall()]
print(users)


