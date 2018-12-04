#!/usr/bin/python

import object_finder.Predictor as pred
import object_finder.PosFromGrid as pfg

if __name__ == '__main__':
    predictor = pred.Predictor()
    pfgo = pfg.PosFromGrid()
    print pfgo.get_rel_pos(0)
    #print(predictor.predict())
    
