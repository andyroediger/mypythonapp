from flask import Flask, render_template, redirect, url_for, request, make_response
import yfinance as yf
import pandas as pd
import datetime as dt
import os
from gunicorn import util
from config import *
import mysql.connector

db_config = {
    'host': hostname,
    'user': username,
    'password': password,
    'database': database,
}

# Function to connect to the MySQL database and fetch data from a specific column
def get_data_from_database(column_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Replace 'your_table_name' with the actual table name
    query = f"SELECT {column_name} FROM your_table_name"
    
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

app = Flask(__name__)
app.config['ENV'] = 'production'

@app.route('/stock_info/<symbol>')
def stock_info(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        info = stock_data.info
        return render_template('stock_info.html', info=info)
    except Exception as e:
       
        return f"Error: {str(e)}"
    
@app.route('/test/<symbol>')
def test(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        info = {
            'longName': stock_data.info.get('longName'),
            'symbol': stock_data.info.get('symbol'),
            'longBusinessSummary': stock_data.info.get('longBusinessSummary'),
            'sector': stock_data.info.get('sector'),
            'industry': stock_data.info.get('industry'),
            'currentPrice': stock_data.info.get('currentPrice'),
            'previousClose': stock_data.info.get('previousClose'),
            'open': stock_data.info.get('open'),
            'dayLow': stock_data.info.get('dayLow'),
            'fullTimeEmployees': stock_data.info.get('fullTimeEmployees'),
            'website': stock_data.info.get('website'),
            'fiftyDayAverage':stock_data.info.get('fiftyDayAverage'),
            'relto50': str(round((stock_data.info.get('currentPrice') / stock_data.info.get('fiftyDayAverage') - 1) * 100, 2)) + ' %',
            'twoHundredDayAverage':stock_data.info.get('twoHundredDayAverage',)       
        }

        return render_template('test.html', info=info)
    except Exception as e:
        return f"Error: {str(e)}"

# @app.route('/ai/model')
# def stock_info(symbol):
#     try:
#         stock_data = yf.Ticker(symbol)
#         info = stock_data.info['dayLow']
#         return render_template('stock_info.html', info=info)
#     except Exception as e:
       
#         return f"Error: {str(e)}"

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/')
def start():
    return "Hello Abdulla !!!"
       

@app.route('/register')
def register():
 return render_template('register.html')
 
 
@app.route('/registerV')
def registerV():
 return render_template('registerV.html')

@app.route('/csv/')
def download_csv():
   csv = 'foo,bar,baz\nhai,bai,crai\n'
   response = make_response(csv)
   cd = 'attachment; filename=mycsv.csv'
   response.headers['Content-Disposition'] = cd
   response.mimetype='text/csv'
   
   return response

@app.route('/model')
def newpage():
    return render_template('model.html')

# Flask route to display the data as an HTML table
@app.route('/hsai')
def hsai():
    # Replace 'your_column_name' with the actual column name you want to fetch
    column_name = 'ai'
    
    data = get_data_from_database(column_name)

    # Render the data in an HTML table
    return render_template('hsai.html', data=data)



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))

    bind_address = f'{host}:{port}'
    worker_class = 'gevent'  # You can choose another worker class based on your requirements

    cmd = [
        'gunicorn',
        '--bind', bind_address,
        '--worker-class', worker_class,
        'app:app',
    ]

    os.execvp(cmd[0], cmd)

