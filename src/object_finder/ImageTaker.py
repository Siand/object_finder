import cv2 


class ImageTaker(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        cv2.destroyAllWindows()

    def capture(self):
        ret,frame = self.cap.read()
        return frame
        
