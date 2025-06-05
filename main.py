from scripts import db_session
from scripts.user import User
import random
from black import blackgak



db_session.global_init("db/bot.db")
dbs = db_session.create_session()
dbs.commit()

blackgak()
