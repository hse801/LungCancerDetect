import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
from utils.plots import color_list
import math
from PIL import Image


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def plot_prediction(img_path, label_path, patient_num, pred_thres, file_name=None, batch_size=9, max_subplots=16):
    img = cv2.imread(img_path)

    img = cv2.resize(img, (3*img.shape[0], 3*img.shape[1]))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_height = img.shape[0]
    img_width = img.shape[1]
    max_size = 640
    batch_size = min(batch_size, max_subplots)  # limit plot images
    ns = np.ceil(batch_size ** 0.5)  # number of subplots (square)

    # Check if we should resize
    scale_factor = max_size / max(img_height, img_width)
    if scale_factor < 1:
        h = math.ceil(scale_factor * img_height)
        w = math.ceil(scale_factor * img_width)

    mosaic = np.full((int(ns * img_height), int(ns * img_width), 3), 255, dtype=np.uint8)  # init

    print(f'img size = {img.shape}')
    print(f'img bgr size = {img_bgr.shape}')
    # xy1 = top left , xy2 = bottom right
    labels = open(label_path, 'r')
    label_list = labels.readlines()
    for l in label_list:
        obj_class, x, y, w, h, conf = map(float, l.rstrip().split(' '))

        x, y, w, h = x * img_width, y * img_height, w * img_width, h * img_height
        x1 = int(x - h * 0.5)
        y1 = int(y + h * 0.5)
        x2 = int(x + w * 0.5)
        y2 = int(y - h * 0.5)
        if obj_class == 0:
            label = 'cancer'
            color = color_list()[0]
            print(f'type of color = {type(color)}')
        else:
            label = 'lymph'
            color = color_list()[1]
        print(f'obj class = {obj_class}, x = {x}, y = {y}, w = {w}, h = {h}, conf = {conf}')
        if float(conf) >= pred_thres: # plot boxes if confidence is higher than confidence threshold
            print('confidence higher than pred_thres')
            cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color=color, thickness=2)

            text = "{}: {:.1f}".format(label, conf)
            # cv2.rectangle(img, int(x), c2, color, -1, cv2.LINE_AA)  # filled
            # cv2.putText(img, label, (int(x) - 7, int(y) - 7), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
            cv2.putText(img_bgr, text, (int(x) - 7, int(y) - 7), 0, 1, color, 3)
            # cv2.rectangle(img_bgr, (10, 10), (50, 50), color=(0, 0, 255),
            #               thickness=3)

    # # Draw image filename labels
    # if paths:
    #     label = Path(paths[i]).name[:40]  # trim to 40 char
    #     t_size = cv2.getTextSize(label, 0, fontScale=tl / 1.5, thickness=tf)[0]
    #     cv2.putText(mosaic, label, (block_x + 15, block_y + t_size[1] + 15), 0, tl / 1.5, [320, 320, 320], thickness=tf,
    #                 lineType=cv2.LINE_AA)

    # if file_name:
    #     r = min(1280. / max(h, w) / ns, 1.0)  # ratio to limit image size
    #     # mosaic = cv2.resize(mosaic, (int(ns * w * r), int(ns * h * r)), interpolation=cv2.INTER_AREA)
    #     cv2.imwrite(file_name, cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))  # cv2 save
    #     # Image.fromarray(mosaic).save(file_name)  # PIL save

    os.chdir('E:/HSE/LungCancerDetect/runs/test/exp37/')
    cv2.putText(img_bgr, patient_num, (2, 15), 0, 0.5,
                [320, 320, 320], thickness=1, lineType=cv2.LINE_AA)
    im_arr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # cv2.imwrite(patient_num + '.jpg', im_arr)
    Image.fromarray(im_arr).save(patient_num + '.jpg')
    print(f'label list = {label_list}')
    print(f'type of img = {type(img)}')


# def draw_prediction():
os.chdir('E:/HSE/LungCancerDetect/data/images/')
img = open('patient_num_test_img.txt', 'r')
img_list = img.readlines()
count = 0
patient_idx = 0
patient_list = []

# get patient list
for i in img_list:
    img_path = i.rstrip()
    patient_num = img_path.split('\\')[-2]
    patient_list.append(patient_num)

for i in img_list:
    img_path = i.rstrip()
    patient_num = img_path.split('\\')[-2]
    img_name = img_path.split('\\')[-1]
    label_path = 'E:/HSE/LungCancerDetect/runs/test/exp37/labels/' + img_name.replace('jpg', 'txt')
    if os.path.isfile(label_path):
        # if count % 9 == 0 or patient_list[patient_idx] != patient_list[patient_idx - 1]:
        #     file_name = str(patient_num) + '_' + str(count) + '.jpg'

        # count = 0
        print(f'i = {i}')
        print(f'image path = {img_path}')
        print(f'patient num = {patient_num}, file name = {img_name}')
        print(f'label name = {label_path}')
        plot_prediction(img_path, label_path, patient_num, 0.25)
        count += 1
        patient_idx += 1
        # break

