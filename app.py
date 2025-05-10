from flask import Flask, render_template, request, flash, redirect, url_for, session
import db

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '0\xd2\xe3\xecBFg\xfc%k\xa5'

@app.route('/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		info = db.get_user_info(email)
		if info and password == info[5]:
			session['fullname'] = info[1]
			return redirect(url_for('home'))
		else:
			flash('Invalid email or password.')
			return render_template('login.html')
	return render_template('login.html')
	
@app.route('/signup')
def signup():
	return render_template('signup.html')
	
@app.route('/logout/')
def logout():
	session['fullname'] = None
	return redirect(url_for('login'))
	
@app.route('/confirmation', methods=['POST'])
def confirmation():
	fullname = request.form.get('fullname')
	user_class = request.form.get('user_class')
	phone = request.form.get('phone')
	email = request.form.get('email')
	password = request.form.get('password')
	info = db.get_user_info(email)
	if info:
		flash('Account already exists. Please sign in.')
		return redirect(url_for('signup'))
	else:
		db.save_user(fullname, user_class, phone, email, password)
		return render_template('confirmation.html')
	
@app.route('/home')
def home():
	session['interest'] = None
	session['event'] = None
	user_id = db.get_user_id(session['fullname'])[0]
	events = []
	interests = []
	marker_event = False
	marker_interest = False
	
	event_ids = db.get_user_event_info(user_id)
	if event_ids:
		print('eventid',event_ids)
		marker_event = True
		for event_id in event_ids:
			event = db.get_event(event_id[0])[0]
			events.append(event)
		print('try',events)
	else:
		event_all = db.get_all_event_info()
		print(event_all)
		for event in event_all:
			events.append(event[2])
		print('except',events)

	interest_ids = db.get_user_interest_info(user_id)
	if interest_ids:
		marker_interest = True
		for interest_id in interest_ids:
			interest = db.get_interest(interest_id[0])[0]
			interests.append(interest)
	else:
		interest_all = db.get_all_interest_info()
		print(interest_all)
		for interest in interest_all:
			interests.append(interest[1])
		
	return render_template('home.html', marker_interest=marker_interest, marker_event=marker_event, events=events, interests=interests)
	
@app.route('/interests')
def interests():
	info = db.get_all_interest_info()
	return render_template('interests.html', info=info)
	
@app.route('/events')
def events():
	info = db.get_all_event_info()
	return render_template('events.html', info=info)
	
@app.route('/createinterest', methods=['POST','GET'])
def createinterest():
	if request.method == 'POST':
		interest = request.form.get('interest').lower()
		description = request.form.get('description')
		info = db.get_interest_info(interest)
		if info:
			flash('This interest already exists!')
			return redirect(url_for('createinterest'))
		else:
			db.save_interest(interest, description)
			flash('Interest created!')
			return redirect(url_for('interests'))
	return render_template('createinterest.html')
	
@app.route('/createevent', methods=['POST','GET'])
def createevent():
	if request.method == 'POST':
		event = request.form.get('event').lower()
		interest = request.form.get('interest')
		description = request.form.get('description')
		event_date = request.form.get('event_date')
		location = request.form.get('location')
		info = db.get_event_info(event)
		if info:
			flash('This event already exists!')
			return redirect(url_for('createevent'))
		else:
			db.save_event(interest, event, description, event_date, location)
			flash('Event created!')
			return redirect(url_for('events'))
	info = db.get_all_interest_info()
	return render_template('createevent.html', info=info)
	
@app.route('/interest/', methods=['POST','GET'])
def interest():
	if request.method == 'POST':
		interest_id = db.get_interest_info(session['interest'])[0]
		user_id = db.get_user_id(session['fullname'])[0]
		try: 
			db.save_user_interest(user_id, interest_id)
			flash("you've joined the interest!")
		except:
			flash("you've already joined this interest!")
		return redirect(f'/interest/?id={session["interest"]}')
	code = request.args.get('id')
	session['interest'] = code
	interest_info = db.get_interest_info(code)
	info = db.get_one_event_info(interest_info[1])
	return render_template('interest.html', interest=interest_info[1], info=info)
	
@app.route('/event/', methods=['POST','GET'])
def event():
	if request.method == 'POST':
		event_id = db.get_event_info(session['event'])[0]
		user_id = db.get_user_id(session['fullname'])[0]
		try:
			db.save_user_event(user_id, event_id)
			flash("you've joined the event!")
		except:
			flash("you've already joined the event!")
		return redirect(f'/event/?id={session["event"]}')
	code = request.args.get('id')
	session['event'] = code
	info = db.get_event_info(code)
	interest = db.get_interest(info[1])[0]
	event_info = info[2:]
	return render_template('event.html', info=event_info, interest=interest)
	
if __name__ == '__main__':
	app.run(debug=True)

