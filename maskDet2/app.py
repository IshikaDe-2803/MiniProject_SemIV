from flask import Flask, render_template, Response, request, redirect, url_for, flash, g
import cv2
from camera import VideoCam
import time
from datetime import datetime
from functools import wraps
from model import Users, Feedback, db
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dmishika2002@gmail.com'
app.config['MAIL_PASSWORD'] = 'unknownme~'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html', home_activity='active')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = request.form['Loginemail']
        password1 = request.form['Loginpassword']
        check_email = Users.query.filter_by(email=email_id).first()
        if check_email is not None and check_email.password == password1:
            success = 'Login SUCCESSFUL'
        # if email_id == "admin@gmail.com" and password1 == "admin1234*":
            success = 'Login SUCCESSFUL'
            return redirect(url_for('dialog'))
        else:
            flash("Invalid Login!!!")
            return render_template('login.html', Login_activity='active', registration=False)
    else:
        return render_template('login.html', Login_activity='active', registration=False)

# @app.route('/feedback')
# def feedback():
#     return render_template('feedback.html', Feedback_activity='active')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        feedbackMsg = request.form['feedmsg']
        new_feedback = Feedback(username=name, email=email, telephone=number, message=feedbackMsg)
        db.session.add(new_feedback)
        db.session.commit()
        msg = Message('Mask Detector Feedback', sender = 'dmishika2002@gmail.com', recipients = ['dmishika2002@gmail.com'])
        msg.body = "Feedback for Mask Detector\nName: " + name + "\n" + "Email: " + email + "\n" + "Contact: " + number + "\n" + "Feedback: " + feedbackMsg
        mail.send(msg)
        return render_template('home.html', feedback=True)    
    return render_template('feedback.html', Feedback_activity='active')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email_id = request.form['register_email']
        password1 = request.form['register_password']
        password_confirm = request.form['confirm_password']
        telephone_no = request.form['telephone']
        if password1 == password_confirm:
            new_user = Users(email=email_id, password=password1, telephone=telephone_no)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html', Login_activity='active', registration=True)
        else:
            flash("Invalid Registration!!!")
            return render_template('register.html', Register_activity='active')
    else:
        return render_template('register.html', Register_activity='active')
        

@app.route('/detect')
def detect():
    return render_template('detection.html', Detect_activity='active')

@app.route('/dialog', methods=['GET', 'POST'])
def dialog():
    return render_template('dialog.html')

def gen_frames(camera):  
    curr_time = time.time()
    while time.time() < curr_time + 5:
        frame, wearmask = camera.get_frame()
        global curr_datetime
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        global maskTF 
        maskTF = wearmask
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(VideoCam()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
