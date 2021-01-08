"""
Application download current stock prices of 5 top crypto currency.
Data are inserted to db2 database.
"""
import json
import configparser
import logging
import sys
import requests
import ibm_db


coins = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'LTC': 'Litecoin',
         'XRP': 'Ripple', 'USDT': 'Tether'
         }

logging.basicConfig(format='%(asctime)s %(message)s',
                    filename='crypto.log', level=logging.INFO)

def get_apikey():
    #Load mandatory api key for alphavantage.com.
    try:
        with open('alphavantageapi.key', 'r') as f:
            return str(f.readline().strip())
    except OSError as e:
        print('Error occured!')
        logging.error(f'{e}')
        sys.exit(1)
    except Exception as e:
        print('Error occured!')
        logging.error(f'{e}')
        sys.exit(1)

def assemble_url(currency: str, wapi_key: str):
    #Prepare complete url to be called.
    try:
        wurl = \
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
        return "".join([wurl, "&from_currency=", currency,
                    "&to_currency=EUR&apikey=", wapi_key])
    except:
        print('Error occured!')
        logging.error(f'{e}')
        sys.exit(1)

def send_request(url: str):
    #Call url using request module. Return values as string.
    return requests.get(url).text


"""
 --------
|Not used|
 --------

def read_currencies():
    cur = pd.read_csv('digital_currency_list.csv', names=[
                      'id', 'desc'], skiprows=[0, 3]).to_dict(orient='list')
    # cur['id'][index], cur['desc'][index]
    d = dict()
    for key, value in zip(cur['id'], cur['desc']):
        d[key] = value
    return d
"""

def connect_to_db():
    #Read db2 parameters from config file and connect to db2.
    #Return a connection object.
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
        print('Error occured!')
        logging.error(f'{e} {ibm_db.conn_errormsg()}')
        sys.exit(1)
    else:
        return con


def insert_data(sql, params):
    #Insert crypto currencies data to database.
    try:
        con = connect_to_db()
        logging.info('Connected to database.')
        stmt = ibm_db.prepare(con, sql)
        o = ibm_db.execute_many(stmt, tuple(params))
        logging.info(f'{o} records inserted into database.')
        ibm_db.free_stmt(stmt)
        ibm_db.close(con)
        logging.info('Close connection.')
    except Exception as e:
        print('Error occured!')
        logging
        logging.error(f'{e} {ibm_db.stmt_error()} {ibm_db.stmt_errormsg()}')
        sys.exit(1)


def query_from_crypto(sql, params):
    try:
        con = connect_to_db()
    except Exception as e:
        logging
        logging.error(f'{e} {ibm_db.stmt_error()} {ibm_db.stmt_errormsg()}')
        sys.exit(1)

def main():
    """
    Main function calls functions in the proper order.
    1. Get api key. 2. Handle requests sent in json format.
    3. Put entities first to a tuple then a list.
    4. Insert the formatted values into db2.
    """
    params = []
    wapi_key = get_apikey()
    for i in coins.keys():
        obj = json.loads(send_request(assemble_url(i, wapi_key)))
        if obj.get('Error Message') is None and obj.get('Information') is None:
            currency_id = obj.get('Realtime Currency Exchange Rate')[
                '1. From_Currency Code']
            currency_desc = obj.get('Realtime Currency Exchange Rate')[
                '2. From_Currency Name']
            date = obj.get('Realtime Currency Exchange Rate')[
                '6. Last Refreshed']
            bid_price = obj.get('Realtime Currency Exchange Rate')[
                '8. Bid Price']
            ask_price = obj.get('Realtime Currency Exchange Rate')[
                '9. Ask Price']
            rate = obj.get('Realtime Currency Exchange Rate')[
                '5. Exchange Rate']
            params.append((currency_id, currency_desc, date, bid_price, \
                                ask_price, rate))
        else:
            print('Error occured!')
            logging.error(f"{obj.get('Error Message') if obj.get('Error Message') else ''}"
                          f"{obj.get('Information') if obj.get('Information') else ''}")
            sys.exit(1)
    sql = "insert into crypto.stock (currency_id, currency_name, cdate, bid, \
                ask, rate) values(?, ?, ?, ?, ?, ?)"
    insert_data(sql, params)
    sys.exit(0)


if __name__ == '__main__':
    main()
