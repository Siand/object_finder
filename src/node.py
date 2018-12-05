#!/usr/bin/python

import object_finder.Predictor as pred
import object_finder.PositionEstimator as posest
import rospy
from actionlib_msgs.msg import GoalStatusArray



class OFClassifier(object):
    def __init__(self):
        items = {'ball':0 ,'hat': 1}
        self.ball_predictor = pred.Predictor("ir_cnn_balls_2.hdf5",0)
        self.pos_estimator = posest.PositionEstimator(items,verbose = False)
        self.command_taker = rospy.Subscriber("/move_base/status", GoalStatusArray, self.image_callback, queue_size=1)
        # run test
        print self.ball_predictor.predict()
        self.locked = False
        self.timeout = 10
        self.prints = 0

    def image_callback(self, status):
        if not self.locked:
            #print self.timeout
            if( (status.status_list and status.status_list[0].status == 3) or self.timeout == 0):
                self.timeout = 10
                self.locked = True
                (b_pred, b_pos) = self.ball_predictor.predict()   
                hp = 0
                print str(self.prints) + 'Image taken: ' + str(b_pred) + ', ' + str(b_pos)
                self.prints+=1
                if  b_pred != 1:
                    print str(self.prints) + ' ' + str(self.pos_estimator.place(0, b_pos))
                    self.prints += 1
                self.locked = False
            if self.timeout > 0:
                self.timeout -= 1
            
    def success_callback(self):
        # destroy class
        return 0
    
if __name__ == '__main__':
    #ball_predictor = pred.Predictor("ir_cnn_balls_2.hdf5",0)
    #print(ball_predictor.predict())
    classifier = OFClassifier()
    rospy.init_node("CLASSIFIER")
    rospy.spin()
