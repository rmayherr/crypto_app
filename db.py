import configparser
import ibm_db


def connecto_db():
	try:
		filename = "db.ini"
		cfg = configparser.ConfigParser()
		cfg.read(filename)
		con_str = 'DATABASE=' + cfg['CRYPTO']['database'] + \
				  ';HOSTNAME=' + cfg['CRYPTO']['hostname'] + \
				  ';PORT=' + cfg['CRYPTO']['port'] + \
				  ';PROTOCOL=' + cfg['CRYPTO']['protocol'] + \
			 	 ';UID=' + cfg['CRYPTO']['uid'] + \
			  	';PWD=' + cfg['CRYPTO']['pwd']
		con = ibm_db.connect(con_str, '', '')
	except Exception as e:
		print('Error occured!\n\t', str(e), ibm_db.conn_errormsg())
	else:
		return con

def query(con, sql=""):
	try:
		if sql != '':
			stmt = ibm_db.exec_immediate(con, sql)
	except Exception as e:
		print('Error occured in query!\n\t', str(e),
			  ibm_db.stmt_error(), ibm_db.stmt_errormsg())
	else:
		return stmt

def fetch_query(stmt):
	try:
		r = ibm_db.fetch_assoc(stmt)
		while r != False:
			print(r)
			r = ibm_db.fetch_assoc(stmt)
	except Exception as e:
		print('Error occured in fetch_query!\n\t', str(e), 
			  ibm_db.stmt_error(), ibm_db.stmt_errormsg())
			
def main():
	con = connecto_db()
	stmt = query(con, "select currency_id, currency_name, cdate, bid, ask, \
				 rate from crypto.stock")
	fetch_query(stmt)
	ibm_db.free_stmt(stmt)
	ibm_db.close(con)

if __name__ == '__main__':
	main()

