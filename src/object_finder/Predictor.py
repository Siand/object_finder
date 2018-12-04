from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import ImageTaker
import numpy as np
import time
import cv2
class Predictor(object):
    def __init__(self):
        self.image_taker = ImageTaker.ImageTaker()
        self.use_file = False 
        self.model = load_model("ir_cnn_2.hdf5")
         
    def predict(self, sample_num=1, sample_delay=30):
        img_array = []
        return_array = [0,0,0,0]
        if self.use_file:
            img = load_img("./balls/ball101.jpg")
            img = img[...,::-1].astype(np.float32)
            img_array.append()
        else:
            for i in range(0,sample_num):
                img_array.append(self.image_taker.capture())
                # cv2.imwrite("asd.jpg",img_array[i])
                time.sleep(sample_delay/1000)   
        for img in img_array:
            rimg = img.copy()
            #rimg = rimg.resize((150,150))
            #x = np.array(rimg)
            #x = x.reshape((1,) + x.shape)
            #print(x.shape)
            rimg.resize((150,150,3))
            rimg = img_to_array(rimg)
            x = rimg.reshape((1,) + rimg.shape)

            cl = self.model.predict_classes(x)
            print(cl)

            return_array[cl[0][0]]+=1
        m = max(return_array)
        return [i for i, j in enumerate(return_array) if j == m]

