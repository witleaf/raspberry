from flask import Flask, render_template
from flask_socketio import SocketIO
from car import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ilovepi'
socketio = SocketIO(app)

mode="BOARD"
leftPwm=33
rightPwm=12
leftGPIO1=29
leftGPIO2=31
rightGPIO1=35
rightGPIO2=37

motor = L298NMotor(mode, leftPwm,leftGPIO1,leftGPIO2,rightPwm,rightGPIO1,rightGPIO2)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('action')
def handle_message(msg):
    print('received message: ' + str(msg))
    action =msg['action']
    print(action) 
    if action == 'start':
        motor.start()

    if action == 'forward':
        motor.forward()
        motor.setSpeed(100)

    if action == 'reverse':
        motor.reverse()
        motor.setSpeed(100)

    if action == 'left':
        motor.turnLeft()
        motor.reverse(50)

    if action == 'right':
        motor.turnRight()
        motor.setSpeed(50)

    if action == 'stop':
        motor.stop()

    if action == 'exit':
        motor.exit()

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0')
