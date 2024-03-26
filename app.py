import pdfplumber
from collections import Counter
import spacy
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

import pdf2image
import layoutparser as lp

# import re
# import os
# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# check a file if it is a pdf
def is_pdf(file_path):
    """
    Check if a file is a pdf
    """
    with open(file_path, 'rb') as f:
        return f.read(4) == b'%PDF'

SAMPLE_DATA_PATH='./sampleData/2021-09-22_Paper_12.pdf'

isPdfType = is_pdf(SAMPLE_DATA_PATH)

if(isPdfType):
    img = np.asarray(pdf2image.convert_from_path(SAMPLE_DATA_PATH)[0])

    model1 = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
                                    label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    # model2 = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_R_50_FPN_3x/config',
    #                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    #                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    # model3 = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
    #                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    #                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    # model4 = lp.Detectron2LayoutModel('lp://PrimaLayout/mask_rcnn_R_50_FPN_3x/config',
    #                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    #                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    layout_result1 = model1.detect(img)
    # layout_result2 = model2.detect(img)
    # layout_result3 = model3.detect(img)
    # layout_result4 = model4.detect(img)

    lp.draw_box(img, layout_result1,  box_width=5, box_alpha=0.2, show_element_type=True)

    # lp.draw_box(img, layout_result2,  box_width=5, box_alpha=0.2, show_element_type=True)

    # lp.draw_box(img, layout_result3,  box_width=5, box_alpha=0.2, show_element_type=True)

    # lp.draw_box(img, layout_result4,  box_width=5, box_alpha=0.2, show_element_type=True)
