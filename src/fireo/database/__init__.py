from fireo.database.database import Database

db = Database()

connection = db.connect
list_collections = db.list_collections