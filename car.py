class L298NMotor:
    GPIO.setwarnings(False)

    def __init__(self, mode, leftPwm, leftGPIO1, leftGPIO2, rightPwm, rightGPIO1, rightGPIO2):

        if (mode=='BCM'):
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.leftPwm=leftPwm
        self.leftGPIO1=leftGPIO1
        self.leftGPIO2=leftGPIO2
        self.rightPwm=rightPwm
        self.rightGPIO1=rightGPIO1
        self.rightGPIO2=rightGPIO2

        self.pwm1=None
        self.pwm2=None

    def start(self):
         GPIO.setup(self.leftGPIO1, GPIO.OUT)
         GPIO.setup(self.leftGPIO2, GPIO.OUT)
         GPIO.setup(self.rightGPIO1, GPIO.OUT)
         GPIO.setup(self.rightGPIO2, GPIO.OUT)

         GPIO.setup(self.leftPwm, GPIO.OUT)
         GPIO.setup(self.rightPwm, GPIO.OUT)

         self.pwm1 = GPIO.PWM(self.leftPwm,100)
         self.pwm2 = GPIO.PWM(self.rightPwm,100)
         self.pwm1.start(0)
         self.pwm2.start(0)


    def reverse(self):
         GPIO.output(self.leftGPIO1, GPIO.HIGH)
         GPIO.output(self.leftGPIO2, GPIO.LOW)
         GPIO.output(self.rightGPIO1, GPIO.HIGH)
         GPIO.output(self.rightGPIO2, GPIO.LOW)

    def forward(self):
         self.start()
         GPIO.output(self.leftGPIO1, GPIO.LOW)
         GPIO.output(self.leftGPIO2, GPIO.HIGH)
         GPIO.output(self.rightGPIO1, GPIO.LOW)
         GPIO.output(self.rightGPIO2, GPIO.HIGH)

    def turnLeft(self):
         GPIO.output(self.leftGPIO1, GPIO.LOW)
         GPIO.output(self.leftGPIO2, GPIO.HIGH)
         GPIO.output(self.rightGPIO1, GPIO.HIGH)
         GPIO.output(self.rightGPIO2, GPIO.LOW)

    def turnRight(self):
         GPIO.output(self.leftGPIO1, GPIO.HIGH)
         GPIO.output(self.leftGPIO2, GPIO.LOW)
         GPIO.output(self.rightGPIO1, GPIO.LOW)
         GPIO.output(self.rightGPIO2, GPIO.HIGH)

    def setSpeed(self,speed):
        if (speed<0):
            speed=0
        if (speed>100):
            speed=100
        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(speed)

    def stop(self):
         GPIO.output(self.gpio_left_gpio_1,GPIO.LOW)
         GPIO.output(self.gpio_left_gpio_2,GPIO.LOW)
         GPIO.output(self.gpio_right_gpio_1,GPIO.LOW)
         GPIO.output(self.gpio_right_gpio_2,GPIO.LOW)
         self.pwm1.stop()
         self.pwm2.stop()

    def exit():
         GPIO.cleanup()
