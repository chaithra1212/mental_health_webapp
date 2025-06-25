# 🧠 Mental Health WebApp

A full-stack web application that uses a machine learning model to predict a user's mental health state based on input data. This project is designed as part of a learning journey in Flask, machine learning, and user authentication systems.

---

## 🚀 Features

- 🧠 **Predicts mental health states**:
  - Normal
  - Mildly Stressed
  - Stressed
  - Depressed
- 🔐 User Signup & Login system
- 🕒 User history stored in CSV (session tracking)
- 🧾 Clean dashboard interface with emotion-specific images
- 💾 Machine Learning model integration (`predictor.pkl`)
- 🌐 Built with Flask, HTML/CSS, and Jinja2 templates

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Jinja2
- **ML Model:** Trained using scikit-learn
- **Storage:** Flat files (CSV for history, TXT for users)

---

## 📁 Project Structure

mental_health_webapp/
│
├── app.py # Main Flask app
├── users.txt # User credentials
├── data/
│ └── history.csv # Stores user prediction history
├── model/
│ └── predictor.pkl # Trained ML model
├── static/
│ ├── images/ # Images for each prediction class
│ └── style.css # Optional styling
├── templates/
│ ├── index.html # Homepage
│ ├── login.html
│ ├── signup.html
│ ├── predict.html
│ └── dashboard.html
├── screenshots/
│ ├── login_page.png
│ ├── predict_page.png
│ └── dashboard.png
