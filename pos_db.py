
import sqlite3

class position_db:

	m_db_connection = None
	m_db_cursor = None

	def __init__(self):
		# Create table
		self.m_db_connection = sqlite3.connect('term_position.db')
		self.m_db_cursor = self.m_db_connection.cursor()

	# Generic Query
	def query(self, query):
		return self.m_db_cursor.execute(query)

	# Create a table
	def create_table(self):
		return self.m_db_cursor.execute('CREATE TABLE IF NOT EXISTS term_pos (TERM TEXT, POSITION INT)')

	# Add a term and its position into the database
	def add_term(self, term, position):
		return self.m_db_cursor.execute('INSERT INTO term_pos VALUES (?, ?)', (term, position))

	def get_term(self, term):
		return self.m_db_cursor.execute('SELECT POSITION FROM term_pos WHERE TERM=?', (term))

	# Print contents of database
	def print_db(self):
		term_row = self.m_db_cursor.execute('SELECT * FROM term_pos')
		for row in term_row:
			print ('TERM: {0} \t POSITION: {1}'.format(str(row[0]), str(row[1])))

	# Commit all changes and close connection
	def close_connection(self):
		self.m_db_connection.commit()
		self.m_db_connection.close()