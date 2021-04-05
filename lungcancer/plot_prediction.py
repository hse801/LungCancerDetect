
import torch
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
from pathlib import Path
from utils.general import xywh2xyxy, xyxy2xywh
import random
import os
import glob

# plot images of bounding boxes
# 환자 별로 결과 이미지를 생성한다


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


def color_list():
    # Return first 10 plt colors as (r,g,b) https://stackoverflow.com/questions/51350872/python-from-color-name-to-rgb
    def hex2rgb(h):
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))

    return [hex2rgb(h) for h in plt.rcParams['axes.prop_cycle'].by_key()['color']]


def plot_images(infiles, fname, paths=None, names=None, max_size=640, max_subplots=16):
    # Plot image grid with labels
    images = []
    for infile in infiles:
        if not Path(infile).exists():
            print(infile, ' does not exist')
        img = cv2.cvtColor(cv2.imread(infile, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (3*img.shape[1], 3*img.shape[0]))
        print('img', img.shape)
        images.append(img)

    tl = 3  # line thickness
    tf = max(tl - 1, 1)  # font thickness
    h, w = images[0].shape[:2]  # batch size, _, height, width
    bs = 16
    bs = min(bs, max_subplots)  # limit plot images
    ns = np.ceil(bs ** 0.5)  # number of subplots (square)

    ns = 4
    # Check if we should resize
    scale_factor = max_size / max(h, w)
    if scale_factor < 1:
        h = math.ceil(scale_factor * h)
        w = math.ceil(scale_factor * w)

    colors = color_list()  # list of colors
    mosaic = np.full((int(ns * h), int(ns * w), 3), 255, dtype=np.uint8)  # init
    print('mosaic', mosaic.shape, 'scale_factor', scale_factor)
    for i in range(len(images) * 2):
        img = images[i // 2]
        block_x = int(w * (i % ns))
        block_y = int(h * (i // ns))

        # img = img.transpose(1, 2, 0)
        if scale_factor < 1:
            img = cv2.resize(img, (w, h))

        mosaic[block_y:block_y + h, block_x:block_x + w, :] = img
        targets = read_targets(infiles[i//2], ground_truth=i % 2 == 0)
        print(f'targets = {targets}')
        if len(targets) > 0:
            if False:
                image_targets = targets[targets[:, 0] == i]
                boxes = xywh2xyxy(image_targets[:, 2:6]).T
                classes = image_targets[:, 1].astype('int')
                labels = image_targets.shape[1] == 6  # labels if no conf column
                conf = None if labels else image_targets[:, 6]  # check for confidence presence (label vs pred)
            else:
                classes = targets[:, 0].astype('int')

                conf = None if i % 2 == 0 else targets[:, 5]
                # if i % 2 == 0:
                #     conf = 0
                # else:
                # conf = targets[:, 5]
                boxes = xywh2xyxy(targets[:, 1:5]).T
                # labels = None

            if boxes.shape[1]:
                if boxes.max() <= 1.01:  # if normalized with tolerance 0.01
                    boxes[[0, 2]] *= w  # scale to pixels
                    boxes[[1, 3]] *= h
                elif scale_factor < 1:  # absolute coords need scale if image scales
                    boxes *= scale_factor
            boxes[[0, 2]] += block_x
            boxes[[1, 3]] += block_y
            for j, box in enumerate(boxes.T):
                cls = int(classes[j])
                color = colors[cls % len(colors)]
                cls = names[cls] if names else cls
                if i % 2 == 0 or conf[j] > 0.25:  # 0.25 conf thresh
                    label = '%s' % cls if i % 2 == 0 else '%s %.1f' % (cls, conf[j])
                    plot_one_box(box, mosaic, label=label, color=color, line_thickness=tl)

        # Draw image filename labels
        if paths:
            # label = Path(paths[i]).name[:40]  # trim to 40 char
            if i % 2 == 0:
                label = paths[i//2].split('\\')[-1][:17] + '_label'
            else:
                label = paths[i//2].split('\\')[-1][:17] + '_predicted'
            print(f'label = {label}')
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            cv2.putText(mosaic, label, (block_x + 5, block_y + t_size[1] + 5), 0, tl / 3, [220, 220, 220], thickness=tf,
                        lineType=cv2.LINE_AA)

        # Image border
        cv2.rectangle(mosaic, (block_x, block_y), (block_x + w, block_y + h), (255, 255, 255), thickness=3)

    if fname:
        r = min(1280. / max(h, w) / ns, 1.0)  # ratio to limit image size
        mosaic = cv2.resize(mosaic, (int(ns * w * r), int(ns * h * r)), interpolation=cv2.INTER_AREA)
        # cv2.imwrite(fname, cv2.cvtColor(mosaic, cv2.COLOR_BGR2RGB))  # cv2 save
        print('PIL save to', fname, 'image shape', mosaic.shape)
        os.chdir('E:/HSE/LungCancerDetect/runs/test/exp37/')
        Image.fromarray(mosaic).save(fname)  # PIL save
        # cv2.imshow(fname, mosaic)
        # cv2.waitKey(0)
    return mosaic


def read_targets(img_path, ground_truth):
    img_file_name = img_path.split('\\')[-1]
    patient_name = img_path.split('\\')[-2]
    if ground_truth:
        # label path of ground truth
        label_path = 'E:/HSE/LungCancerDetect/data/testset/'+patient_name+'/' + img_file_name.replace('jpg', 'txt')
    else:
        # label path of prediction
        label_path = 'E:/HSE/LungCancerDetect/runs/test/exp37/labels/' + img_file_name.replace('jpg', 'txt')
    targets = []
    if os.path.isfile(label_path):
        labels = open(label_path, 'r')
        label_list = labels.readlines()
        for l in label_list:
            target = map(float, l.rstrip().split(' '))
            targets.append(list(target))
            # print(f'targets = {targets}')
            # print(f'type = {type(targets)}, len = {len(targets)}')
        # print(targets[1])
    return np.array(targets)


# read_targets(r'E:/HSE/LungCancerDetect/data/testset\12380088\12380088_slice047.jpg')


def split_by_patient(lines):
    def get_patient(line):
        return line.split('\\')[-2]
    lines_per_patient = {}
    patient = ''
    for line in lines:
        line = line.rstrip()
        new_patient = get_patient(line)
        if new_patient == patient:
            lines_per_patient[patient].append(line)
        else:
            lines_per_patient[new_patient] = [line]
            patient = new_patient
    return lines_per_patient


os.chdir('E:/HSE/LungCancerDetect/data/images/')
lines = split_by_patient(open('patient_num_test_img.txt', 'r').readlines())
names = {0: 'cancer', 1: 'lymph'}

for patient in lines:
    lines_per_patient = lines[patient]
    for i in range(0, len(lines_per_patient), 8):
        # patient_num = lines_per_patient[i:i+9].split('\\')[-1]
        file_name = lines_per_patient[0].split('\\')[-2] + '_' + str(i) + '.jpg'
        plot_images(lines_per_patient[i:i+8],names=names, paths=lines_per_patient[i:i+8], fname=file_name)
        # plot_images()
        # print(f'patient num = {patient_num}')
        # print(f'i = {i}')
        # print(f'for patient {patient}')
        # print(f'lines per patient = {lines_per_patient[i:i+9]}')
        # print(f'length = {len(lines_per_patient[i:i+9])}')


