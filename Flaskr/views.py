from flaskr import *
@app.route('/')
def show_entries():
	''' This will also serve as the main page '''
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?,?)',
					[request.form['title'], request.form['text']]) # this isn't safe yet
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error=None
	if request.method == 'POST': # User is logging in
		#print("request was a post") # Its stopping here and going no further.
		if request.form['username'] != app.config['USERNAME']:
			#print("username was not valid")
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			#print("password was not valid")
			error = 'Invalid password'
		else:
			#print("made it to logged in")
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	else:
		pass
		#print("request was a get")
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))