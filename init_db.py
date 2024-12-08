from flask_app import model
connection = model.connect()
model.create_database(connection)
model.fill_database(connection)
model.add_user(connection, 'admin@example.com', 'admin','Secret1234**')