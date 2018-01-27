# -*- coding: utf-8-*-
import logging
import sys
import time
import socket
import subprocess
import RPi.GPIO as GPIO
import time
import traceback

"""

"""

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["QIDONG"]
SLUG = "xiao_che"


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

    params = {}
    params['mic'] = mic
    params['profile'] = profile

    persona = 'DINGDANG'
    if 'robot_name' in profile:
        persona = profile['robot_name']

    robot_name_cn = u'叮当'
    if 'robot_name_cn' in profile:
        robot_name_cn = profile['robot_name_cn']


    print profile[SLUG]
    print SLUG
    if SLUG not in profile:
        mic.say(u'小画配置有误，无法启动,请正确配置小车', cache=True)
        return
    mode = profile[SLUG]['mode']
    leftPwm = int(profile[SLUG]['gpio_left_pwm'])
    leftGPIO1 = int(profile[SLUG]['gpio_left_1'])
    leftGPIO2 = int(profile[SLUG]['gpio_left_2'])

    rightPwm = int(profile[SLUG]['gpio_right_pwm'])
    rightGPIO1 = int(profile[SLUG]['gpio_right_1'])
    rightGPIO2 = int(profile[SLUG]['gpio_right_2'])
    try:
        logger.debug(text)
        xiaoche = Xiaoche(params,mic,profile)

        #小车，添加电机模块
        xiaoche.motor = L298NMotor(mode, leftPwm,leftGPIO1,leftGPIO2,rightPwm,rightGPIO1,rightGPIO2)
        xiaoche.start() #启动小车线程

        while True:
            try:
                threshold, transcribed = mic.passiveListen(persona)
            except Exception, e:
                logger.error(e)
                threshold, transcribed = (None, None)

            if not transcribed or not threshold:
                logger.info("Nothing has been said or transcribed.")
                continue

            input = mic.activeListen()

            if (any(word in input for word in [u"启动"])):
                 logger.info("小车进入驾驶模式")
                 xiaoche.start()
                 mic.say(u"小车进入驾驶模式,你现在可以说前进或者后退来控制")
                 return

            if (any(word in input for word in [u"前进"])):
                 mic.say(u"小车准备前进")
                 xiaoche.forward(100)
                 return

            if (any(word in input for word in [u"停车",u"停止"])):
                 mic.say(u"小车准备停车")
                 xiaoche.stop()
                 return

            if (any(word in input for word in [u"退出行驶",u"退出"])):
                 mic.say(u"退出行驶模式")
                 xiaoche.exit()
                 return

    except Exception, e:
        print u"配置异常"
        print e
        print traceback.print_exc()
        logger.error(e)
        mic.say(u'主人，动力系统有问题', cache=True)

def isValid(text):
    return any(word in text for word in [u"启动",u"自动驾驶","开车","手动驾驶", u"前进",u"加速",u"快点",u"停车",u"左转",u"向左转",u"向右转",u"后退",u"后倒",u"退出行驶"])



class Xiaoche(threading.Thread):

    def __init__(self, mic,profile):
        super(Xiaoche,self).__init__()
        self.event=threading.Event()

        self.logger = logging.getLogger(__name__)
        self.mic = mic
        self.profile = profile
        self.speed = 0     #当前小车的状态
        self.status = None #当前小车的状态
        self.is_exit = False
        self.is_stop = False
        self.motor = None

        def run(self):
            while True and not self.is_exit:
                if self.event.wait():
                    if self.is_stop== True:
                        self.setSpeed(0)
                    else :
                        self.setSpeed(100)


        def setSpeed(self,speed):
            time.sleep(1)
            print "设置",speed

        def forward(self):
            print "开始前行"
            self.event.set()
            self.motor.forward()


        def stop(self):
            try:
                print "中间停车,没有熄火"
                self.motor.stop()
                self.event.clear()
                self.is_stop =False
            except:
                pass

        def exit(self):
            print "停车熄火"
            self.motor.exit()
            self.is_exit=True
            self.stop()

        def resume(self):
             self.is_stop = False
             self.event.set()


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
         print 'start'
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
