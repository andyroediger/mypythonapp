from flask import Flask, render_template, redirect, url_for, request, make_response
import yfinance as yf
import pandas as pd
import datetime as dt
import os
from gunicorn import util


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

@app.route('/ai/model')
def stock_info(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        info = stock_data.info['dayLow']
        return render_template('stock_info.html', info=info)
    except Exception as e:
       
        return f"Error: {str(e)}"

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

