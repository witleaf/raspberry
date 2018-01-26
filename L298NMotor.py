import logging
import sys
import time
import socket
import subprocess
import RPi.GPIO as GPIO
import time



reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["QIDONG"]
SLUG = "L298N"

def handle(text, mic, profile, wxbot=None):
    """
    Responds to user-input, typically speech text
    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    logger = logging.getLogger(__name__)

    kwargs = {}
    kwargs['mic'] = mic
    kwargs['profile'] = profile

    persona = 'DINGDANG'
    if 'robot_name' in profile:
        persona = profile['robot_name']

    robot_name_cn = u'叮当'
    if 'robot_name_cn' in profile:
        robot_name_cn = profile['robot_name_cn']



    if SLUG not in profile:
       'gpio' not in profile[SLUG]:
        mic.say(u'L298N配置有误，插件使用失败', cache=True)
        return
    if 'gpio' in profile[SLUG]:
        leftPwm = int(profile[SLUG]['gpio_left_pwm'])
        leftGPIO1 = int(profile[SLUG]['gpio_left_gpio_1'])
        leftGPIO2 = int(profile[SLUG]['gpio_left_gpio_2'])

        rightPwm = int(profile[SLUG]['gpio_right_pwm'])
        rightGPIO1 = int(profile[SLUG]['gpio_right_gpio_1'])
        rightGPIO2 = int(profile[SLUG]['gpio_right_gpio_2'])
    else:
        mic.say(u'主人，开车要先接好引脚线', cache=True)
    try:
        logger.debug(word)
        motor=L298NMotor(leftPwm,leftGPIO1,leftGPIO2,rightPwm,rightGPIO1,rightGPIO2)
        i:=50
        if (any(word in text for word in [u"启动"])):
            motor.start()
            mic.say(u"小车已经启动,你现在可以说前进或者后退来控制")
        else if (any(word in text for word in [u"前进"])):
            while i<100:
                i=i+5
                motor.SetSpeed(i)
                motor.forward()
                time.speed(1)
            pass
        else if (any(word in text for word in [u"停车",u"停止"])):
            while i>0:
                i=i-5
                motor.SetSpeed(i)
                motor.forward()
                time.speed(1)
            pass
            motor.stop()
        else if (any(word in text for word in [u"退出行驶",u"退出"])):
            motor.exit()
        else {
            mic.say(u'主人，请说，前进，后退，向左转，向后转，后退，倒来控制小车')
        }
    except Exception, e:
        print u"配置异常"
        logger.error(e)
        mic.say(u'主人，启动电机失败了', cache=True)

def isValid(text):
    return any(word in text for word in [u"启动",u"自动驾驶","开车","手动驾驶", u"前进",u"加速",u"快点",u"停车",u"左转",u"向左转",u"向右转",u"后退",u"后倒",u"退出行驶"])



Class L298NMotor:
     '电机驱动类'
     GPIO.setmode(GPIO.BOARD)
     GPIO.setwarnings(False)

     def __int__(mode,leftPwm,leftGPIO1,leftGPIO2,rightPwm,rightGPIO1,rightGPIO2):
         if (mode=='BCM'):
            GPIO.setmode(GPIO.BCM)
         else
            GPIO.setmode(GPIO.BOARD)
         GPIO.setwarnings(False)
         self.leftPwm=leftPwm
         self.leftGPIO1=leftGPIO1
         self.leftGPIO2=leftGPIO2
         self.leftPwm=leftPwm
         self.rightGPIO1=rightGPIO1
         self.rightGPIO2=rightGPIO2

     def start():
         GPIO.setup(self.leftGPIO1, GPIO.OUT)
         GPIO.setup(self.leftGPIO2, GPIO.OUT)
         GPIO.setup(self.rightGPIO1, GPIO.OUT)
         GPIO.setup(self.rightGPIO2, GPIO.OUT)

         GPIO.setup(self.leftPwm, GPIO.OUT)
         GPIO.setup(self.rightPwm, GPIO.OUT)

         self.leftPwm = GPIO.PWM(PWM1,100)
         self.rightPwm = GPIO.PWM(PWM2,100)

         self.leftPwm.start(0)
         self.rightPwm.start(0)

    def Reverse():
         GPIO.output(self.leftGPIO1, GPIO.HIGH)
         GPIO.output(self.leftGPIO2, GPIO.LOW)
         GPIO.output(self.rightGPIO1, GPIO.HIGH)
         GPIO.output(self.rightGPIO2, GPIO.LOW)


   def Foward():
        GPIO.output(self.leftGPIO1, GPIO.LOW)
        GPIO.output(self.leftGPIO2, GPIO.HIGH)
        GPIO.output(self.rightGPIO1, GPIO.LOW)
        GPIO.output(self.rightGPIO2, GPIO.HIGH)

    def TurnLeft():
         GPIO.output(self.leftGPIO1, GPIO.LOW)
         GPIO.output(self.leftGPIO2, GPIO.HIGH)
         GPIO.output(self.rightGPIO1, GPIO.HIGH)
         GPIO.output(self.rightGPIO2, GPIO.LOW)

    def TurnRight():
         GPIO.output(self.leftGPIO1, GPIO.HIGH)
         GPIO.output(self.leftGPIO2, GPIO.LOW)
         GPIO.output(self.rightGPIO1, GPIO.LOW)
         GPIO.output(self.rightGPIO2, GPIO.HIGH)

    def SetSpeed(speed):
         if (speed<0):
               speed=0
         if (speed>100):
               speed=100
          self.leftPwm.ChangeDutyCycle(speed)
          self.rightPwm.ChangeDutyCycle(speed)

    def Stop():
         GPIO.output(self.gpio_left_gpio_1,GPIO.LOW)
         GPIO.output(self.gpio_left_gpio_2,GPIO.LOW)
         GPIO.output(self.gpio_right_gpio_1,GPIO.LOW)
         GPIO.output(self.gpio_right_gpio_2,GPIO.LOW)
         self.leftPwm.stop()
         self.rightPwm.stop()

    def exit():
         GPIO.cleanup()
