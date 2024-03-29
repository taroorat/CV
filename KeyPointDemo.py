import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import os
# import some common libraries
import numpy as np
import cv2
import random

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

cfg = get_cfg()
cfg.merge_from_file("./detectron2_repo/configs/COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can either use the https://dl.fbaipublicfiles.... url, or use the following shorthand
cfg.MODEL.WEIGHTS = "detectron2://COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x/139686956/model_final_5ad38f.pkl"
# print(cfg)
predictor = DefaultPredictor(cfg)

def draw_new_image():
    for path in os.listdir(srcDir):
        print(path)
        im = cv2.imread(srcDir+path)
        outputs = predictor(im)
        # print(outputs)

        new_img=np.zeros((im.shape[0],im.shape[1],3), np.uint8)
        v = Visualizer(new_img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        v = v.draw_instance_predictions(outputs['instances'].to('cpu'))
        # print(v.get_image()[:, :, ::-1])
        cv2.imwrite(dstDir+path,v.get_image()[:, :, ::-1])

def draw_image():
    for path in os.listdir(srcDir):
        print(path)
        im = cv2.imread(srcDir + path)
        outputs = predictor(im)
        # print(outputs)

        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        v = v.draw_instance_predictions(outputs['instances'].to('cpu'))
        # print(v.get_image()[:, :, ::-1])
        cv2.imwrite(dstDir + path, v.get_image()[:, :, ::-1])

if __name__ == '__main__':
    srcDir = 'images/dajiwu/'
    dstDir = 'images/keypoint/dajiwu/'
    # draw_new_image()
    draw_image()



