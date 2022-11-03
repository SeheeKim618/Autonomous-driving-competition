import base64
from datetime import datetime
import os
import shutil
import numpy as np
from nav_msgs.msg import Odometry
from keras.models import load_model
#helper class
import utils
from mavros_msgs.msg import *
from mavros_msgs.srv import *
import rospy
from sensor_msgs.msg import Imu,Image
import cv2
import math
import ros_numpy
from xycar_msgs.msg import xycar_motor
class Road():
    def __init__(self):
        
        self.count = 0
        self.rgb_map = 0.1
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.depth_color_map = Image()
        self.sp = Odometry()
        
        self.model_pretrained = load_model('/home/seheekim/Desktop/autonomous/cloning/model.h5')
        
    
        self.vel_msg = xycar_motor()
        
        self.pub = rospy.Publisher('/xycar_motor', xycar_motor, queue_size=1,tcp_nodelay=True)
        rospy.init_node('setpoint_node', anonymous=True)
        

    
    
    def Drive(self):
        depth_image = None
        while depth_image is None:
            try:
                depth_image = rospy.wait_for_message("/usb_cam/image_raw", Image, timeout = 5)
            except:
                pass
        depth_image = ros_numpy.numpify(depth_image)
       
        image = utils.preprocess(depth_image) # apply the preprocessing
    
        inputt = np.array([image])
        infer = self.model_pretrained.predict(inputt, batch_size=1)
        self.vel_msg.speed = 35
        self.vel_msg.angle = int(infer[0])
        self.pub.publish(self.vel_msg)
        print('Im driving at speed of ',self.vel_msg.speed,'KPH' )
tensor = Road()
while(1):  
    tensor.Drive()
  
        
