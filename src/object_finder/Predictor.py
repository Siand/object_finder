from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import ImageTaker

class Predictor(object):
    def __init__(self):
        self.image_taker = ImageTaker.ImageTaker()
        self.use_file = True 
         
    def predict(self, sample_num=1, sample_delay=30):
        model = load_model("ir_cnn_2.hdf5")
        img_array = []
        if self.use_file:
            img_array.append(load_img("./balls/ball101.jpg"))
        else:
            for i in range(0,sample_num):
                img_array.append(self.image_taker.capture())
                time.sleep(sample_delay/1000)   
        for img in img_array:
            img = img.resize((150,150))
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)
            cl = model.predict_classes(x)
        return_array = [] 
        return return_array

