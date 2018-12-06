from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import ImageTaker
from PIL import Image
import numpy as np
import time
import cv2
import random
class Predictor(object):
    def __init__(self, model_name, object_num):
        self.image_taker = ImageTaker.ImageTaker()
        self.use_file = False 
        self.obj_num = object_num
        self.model = load_model(model_name)
        self.counter = 0
        #cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    

    def locate_ball(self,pic):
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
        sums = [sum(x) for x in zip(*ts)]
        sum_arrs = sum(sums)
        xs = 0
        ys = 0
        for i in range(len(sums)):
            xs += (i % 4) * sums[i]
            ys += (i // 4) * sums[i]
        x = (xs + 0.5) // sum_arrs
        y = (ys + 0.5) // sum_arrs
        if x > 3:
            x = 3
        if y > 3:
            y = 3
        return x + 4 * y




    def predict(self, sample_num=1, use_file=False):
        sample_delay = 30
        tile_array = []
        img_array = []
        return_array = [0] * 2
        tile = 16
        if use_file:
            img = load_img("./balls/ball101.jpg")
            img = img[...,::-1].astype(np.float32)#/255.0
            img_array.append(img)
        else:
            for i in range(0,sample_num):
                img_array.append(self.image_taker.capture())
                #cv2.imshow("frame", img_array[i])
                cv2.imwrite("empty/newEmpty{0}.jpg".format(self.counter),img_array[i])
                self.counter +=1
                #cv2.waitKey(30)
                time.sleep(sample_delay/1000)   
        for img in img_array:
            rimg = img.copy()
            cv2im = rimg
            cv2im = cv2.cvtColor(cv2im, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2im)
            #pil_im.show()
            pil_im = pil_im.resize((150,150))
            pil_im.show()
            rimg = np.array(pil_im) 
            x = rimg.reshape((1,) + rimg.shape) 
            cl = self.model.predict_classes(x)
            if(cl[0][0] == self.obj_num):
                tile_array.append(self.locate_ball(img))
            return_array[cl[0][0]]+=1
        if tile_array == []:
            return (1-self.obj_num,None)
        item_pos = self.choose_tile(tile_array)
        m = max(return_array)
        best_pred = [i for i, j in enumerate(return_array) if j == m]
        random.shuffle(best_pred)
        return (best_pred[0],item_pos)

