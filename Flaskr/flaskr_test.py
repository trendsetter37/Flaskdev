import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		flaskr.app.config['TESTING'] = True
		self.app = flaskr.app.test_client()
		flaskr.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_empty_db(self):
		rv = self.app.get('/')
		# encoding string as a byte string. This is needed for Python 3
		# Read more here
		assert 'No entries here so far'.encode() in rv.data
	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password), follow_redirects=True)
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	# What was determined or learned here is that python 3 needs to
	# encode the strings that are compared with the ones in 
	# rv.data
	# *********************************

	# There therefore rv.data is encoded and that should be kept
	# in mind when handeling request and such

	def test_login_logout_with_encoded_strings(self):
		rv = self.login('admin', 'default')
		
		assert 'You were logged in'.encode() in rv.data
		rv = self.logout()
		assert 'You were logged out'.encode() in rv.data
		rv = self.login('adminx', 'default')
		assert 'Invalid username'.encode() in rv.data
		rv = self.login('admin', 'defaultx')
		assert 'Invalid password'.encode() in rv.data

	# Do test messages next 
	def test_messages(self):
		self.login('admin', 'default')
		rv = self.app.post('/add', data=dict(
			title='<Hello>',
			text='<strong>HTML</strong> allowed here'),
		follow_redirects=True)

		# rv.data is a byte string that needs to be converted
		# to a unicode string for python3
		decoded_rv = rv.data.decode()
		assert 'No entries here so far' not in decoded_rv
		assert '<strong>HTML</strong> allowed here' in decoded_rv
		assert '<Hello>' in decoded_rv					 

	def test_request_context(self):
		import flask

		app = flask.Flask(__name__)

		with app.test_request_context('/?name=Peter'):
			assert flask.request.path == '/'
			assert flask.request.args['name'] == 'Peter'
		
		

if __name__ == '__main__':
	unittest.main()