from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import ImageTaker

class Predictor(object):
    def __init__(self):
        self.image_taker = ImageTaker.ImageTaker()
        self.use_file = False 
         
    def predict(self):
        model = load_model("ir_cnn_1.hdf5")
        
        if self.use_file:
            img = load_img("./balls/ball134.jpg")
        else:
            img = self.image_taker.capture()   
        img = img.resize((150,150))
        x = img_to_array(img)
        print(x.shape)
        x = x.reshape((1,) + x.shape)
        print(x.shape)
        cl = model.predict_classes(x)

        print(cl)

