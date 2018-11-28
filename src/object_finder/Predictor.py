from net.build import TFNet
import cv2
import ImageTaker

class Predictor(object):
    def __init__(self):
        self.image_taker = ImageTaker.ImageTaker()
        #self.tfnet = TFNet(<options_from_yolo>)
         
    def predict(self):
        frame = self.image_taker.capture()
        cv2.imshow("frame",frame)
        cv2.waitKey(0) 
        cv2.imwrite("image.jpg",frame)
        
        

