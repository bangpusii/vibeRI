import sqlite3

def init_db():
	connection = sqlite3.connect('viberi.db')
	with open('create.sql','r') as file:
		data = file.read()
	connection.executescript(data)
	connection.commit()
	file.close()
	connection.close()

def save_user(fullname, user_class, phone, email, password):
	connection = sqlite3.connect('viberi.db')
	count = connection.execute('SELECT MAX(user_id) FROM users').fetchone()
	if count[0]:
		user_id = int(count[0])+1
	else:
		user_id = 1
	connection.execute('''
		INSERT INTO  users (user_id, fullname, user_class, phone, email, password) 
		VALUES (?,?,?,?,?,?)''', 
		(user_id, fullname, user_class, phone, email, password)
	)
	connection.commit()
	connection.close()

def save_interest(interest, description):
	connection = sqlite3.connect('viberi.db')
	count = connection.execute('SELECT COUNT(*) FROM interests').fetchone()
	if count[0]:
		interest_id = int(count[0])+1
	else:
		interest_id = 1
	connection.execute('''
		INSERT INTO interests (interest_id, interest, description)
		VALUES (?,?,?)''',
		(interest_id, interest, description)
	)
	connection.commit()
	connection.close()
	
def save_user_interest(user_id, interest_id):
	connection = sqlite3.connect('viberi.db')
	connection.execute('''
		INSERT INTO users_interests (user_id, interest_id)
		VALUES (?,?)''',
		(user_id, interest_id)
	)
	connection.commit()
	connection.close()
	
def save_event(interest, title, description, event_date, location):
	connection = sqlite3.connect('viberi.db')
	count = connection.execute('SELECT COUNT(*) FROM events').fetchone()
	if count[0]:
		event_id = int(count[0])+1
	else:
		event_id = 1
	interest_id = connection.execute('SELECT interest_id FROM interests WHERE interest = ?',(interest,)).fetchone()
	connection.execute('''
		INSERT INTO events (event_id, interest_id, title, description, event_date, location)
		VALUES (?,?,?,?,?,?)''',
		(event_id, interest_id[0], title, description, event_date, location)
	)
	connection.commit()
	connection.close()
	
def save_user_event(user_id, event_id):
	connection = sqlite3.connect('viberi.db')
	connection.execute('''
		INSERT INTO users_events (user_id, event_id)
		VALUES (?,?)''',
		(user_id, event_id)
	)
	connection.commit()
	connection.close()
	
def get_user_info(email):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
	connection.close()
	return info
	
def get_user_id(fullname):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT user_id FROM users WHERE fullname=?',(fullname,)).fetchone()
	connection.close()
	return info
	
def get_all_interest_info():
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM interests').fetchall()
	connection.close()
	return info
	
def get_interest_info(interest):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM interests WHERE interest=?',(interest,)).fetchone()
	connection.close()
	return info
	
def get_all_event_info():
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM events').fetchall()
	connection.close()
	return info
	
def get_one_event_info(interest):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM events WHERE interest_id = (SELECT interest_id FROM interests WHERE interest = ?)',(interest,)).fetchall()
	connection.close()
	return info

def get_event_info(event):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT * FROM events WHERE title = ?',(event,)).fetchone()
	connection.close()
	return info
	
def get_event(event_id):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT title FROM events WHERE event_id = ?',(event_id,)).fetchone()
	connection.close()
	return info
	
def get_user_event_info(user_id):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT event_id FROM users_events WHERE user_id = ?',(user_id,)).fetchall()
	connection.close()
	return info
	
def get_interest(interest_id):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT interest FROM interests WHERE interest_id = ?',(interest_id,)).fetchone()
	connection.close()
	return info

def get_user_interest_info(user_id):
	connection = sqlite3.connect('viberi.db')
	info = connection.execute('SELECT interest_id FROM users_interests WHERE user_id = ?',(user_id,)).fetchall()
	connection.close()
	return info
	
init_db()
	