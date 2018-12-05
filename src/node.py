#!/usr/bin/python

import object_finder.Predictor as pred
import object_finder.PositionEstimator as posest
import rospy
from actionlib_msgs.msg import GoalStatusArray



class OFClassifier(object):
    def __init__(self):
        items = {'ball':0 ,'hat': 1}
        self.ball_predictor = pred.Predictor("ir_cnn_balls_2.hdf5",0)
        self.pos_estimator = posest.PositionEstimator(items,verbose = True)
        self.command_taker = rospy.Subscriber("/move_base/status", GoalStatusArray, self.image_callback, queue_size=1)

    def image_callback(self, status):
        if(status.status_list[0].status == 3):
            ball_predictions = self.ball_predictor.predict()    
            (b_pred, b_pos) = ball_predictions
            hp = 0
            if  b_pred != 1:
                self.pos_estimator.place(0, b_pos)

if __name__ == '__main__':
    #ball_predictor = pred.Predictor("ir_cnn_balls_2.hdf5",0 )
    #print(ball_predictor.predict())
    classifier = OFClassifier()
    rospy.init_node("CLASSIFIER")
    rospy.spin()
