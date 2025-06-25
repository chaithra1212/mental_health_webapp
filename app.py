from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import pickle
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load model
with open('model/predictor.pkl', 'rb') as f:
    model, label_encoder = pickle.load(f)

# Load users from users.txt
def load_users():
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            return dict(line.strip().split(',') for line in file)
    return {}

# Save new user
def save_user(username, password):
    with open('users.txt', 'a') as file:
        file.write(f"{username},{password}\n")

users = load_users()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global users
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('predict'))
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global users
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            return render_template('signup.html', error="Username already exists")
        users[uname] = pwd
        save_user(uname, pwd)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    prediction = None
    if request.method == 'POST':
        try:
            screen_time = float(request.form['screen_time'])
            unlock_count = float(request.form['unlock_count'])
            sleep_hours = float(request.form['sleep_hours'])
            app_usage = float(request.form['app_usage'])

            features = [[screen_time, unlock_count, sleep_hours, app_usage]]
            pred_encoded = model.predict(features)
            prediction = label_encoder.inverse_transform(pred_encoded)[0]

            # Save prediction to history
            log = {
                'username': session['username'],
                'screen_time': screen_time,
                'unlock_count': unlock_count,
                'sleep_hours': sleep_hours,
                'app_usage': app_usage,
                'prediction': prediction,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            os.makedirs('data', exist_ok=True)
            history_path = 'data/history.csv'
            df_log = pd.DataFrame([log])

            if os.path.exists(history_path):
                df_log.to_csv(history_path, mode='a', header=False, index=False)
            else:
                df_log.to_csv(history_path, index=False)

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template('predict.html', prediction=prediction)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        df = pd.read_csv('data/history.csv')
        total_predictions = len(df)
        latest_predictions = df.tail(5).to_dict(orient='records')
        mood_counts = df['prediction'].value_counts().to_dict()
    except Exception:
        total_predictions = 0
        latest_predictions = []
        mood_counts = {}

    return render_template('dashboard.html',
                           total_predictions=total_predictions,
                           latest_predictions=latest_predictions,
                           mood_counts=mood_counts)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
