from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import ImageTaker
import numpy as np
import time
import cv2
class Predictor(object):
    def __init__(self, model_name, object_num):
        self.image_taker = ImageTaker.ImageTaker()
        self.use_file = False 
        self.obj_num = object_num
        self.model = load_model(model_name)
    

    def locate_ball(pic):
        # split data into segments - current dimensions are (150, 150, 3)
        data = img_to_array(pic)
        segments = []
        for x in range(0,4):
            for y in range(0,4):
                # needs to change depending on HEIGHT and WIDTH, currently based on 150x150
                seg = data[x*35:(x+1)*35+10,y*35:(y+1)*35+10][:]
                p = array_to_img(seg)
                # resize to model input size
                p = p.resize((150,150))
                seg = img_to_array(p)
                seg = seg.reshape((1,) + seg.shape)
                segments.append(seg)

        classes = []
        for seg in segments:
            classes.append(self.model.predict_classes(seg)[0].tolist()[0])
        return classes
        # analyze each segment
        # find location of ball



        def choose_tile(self, tile_arrays):
            ts = []
            for tile_array in tile_arrays:
                t = [int(i==self.obj_num) for i in tile_array]
                if sum(t):
                    ts.append(t)
            if ts == []:
                return 6 # attempt at finding a middle point
            # sum up lists
            # take average x and y
            num_arrs = len(ts)
            sums = [sum(x) for x in zip(*ts)]
            xs = 0
            ys = 0
            for i in range(len(sums)):
                xs += (i % 4) * sums[i]
                ys += (i // 4) * sums[i]
            x = (xs + 0.5) // num_arrs
            y = (ys + 0.5) // num_arrs
            return x + 4 * y




    def predict(self, sample_num=1):
        sample_delay = 30
        tile_array = []
        img_array = []
        return_array = [0] * 2
        tile = 16
        if self.use_file:
            img = load_img("./balls/ball101.jpg")
            img = img[...,::-1].astype(np.float32)
            img_array.append(img)
        else:
            for i in range(0,sample_num):
                img_array.append(self.image_taker.capture())
                # cv2.imwrite("asd.jpg",img_array[i])
                time.sleep(sample_delay/1000)   
        for img in img_array:
            rimg = img.copy()
            rimg.resize((150,150,3))
            rimg = img_to_array(rimg)
            x = rimg.reshape((1,) + rimg.shape)        
            cl = self.model.predict_classes(x)
            if(cl[0][0] == self.obj_num):
                tile_array.append(self.locate_ball(img))
            return_array[cl[0][0]]+=1
        item_pos = choose_tile(tile_array)
        m = max(return_array)
        best_pred = [i for i, j in enumerate(return_array) if j == m] 
        return (best_pred[0],item_pos)

