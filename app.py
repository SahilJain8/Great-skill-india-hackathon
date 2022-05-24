from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import pickle
import numpy as np


with open('gojo.pkl', 'rb') as f:
    x = pickle.load(f)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'earthquake'

mysql = MySQL(app)

with open('gojo.pkl', 'rb') as f:
    x = pickle.load(f)
print(x)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index.html')
def homes():
    return render_template('index.html')


@app.route('/tables.html')
def tables():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM datasourc ")
    data = cur.fetchall()
    cur.close()
    return render_template('tables.html', table=data)


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    type = request.form['type']
    depthError = request.form['depthError']
    status = request.form['status']
    locationSource = request.form['locationSource']
    magSource = request.form['magSource']
    shortplace = request.form['short place']
    input_data = (latitude,
                  longitude,
                  type,
                  depthError,
                  status,
                  locationSource,
                  magSource,
                  shortplace)
    input_data_as_numpy_array = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = x.predict(input_data_reshaped)

    return render_template('model.html', prediction_text='Mag is {}'.format(prediction[0][0]))
   


@app.route('/model.html')
def model():
    return render_template('model.html')


if __name__ == "__main__":
    app.run(debug=True)
