from typing import Dict, Tuple, List
import re
from zipfile import ZipFile
from collections import defaultdict
import numpy as np

from bbutil import BB, BBCollections

import SimpleITK as sitk


def load_label_files(f: str) -> BBCollections:
    is_gt = True
    z = ZipFile(f)
    bb = {}
    filepattern = re.compile(r'(\d+)_slice(\d+).txt')
    print(f'filepattern = {filepattern}')
    for filename in z.namelist():
        m = filepattern.match(filename)
        patient, slice = m.group(1), m.group(2)
        if not patient in bb:
            roi = bb[patient] = defaultdict(list)
        else:
            roi = bb[patient]
        for line in z.read(filename).decode('ascii').splitlines():
            if is_gt:
                try:
                    conf = 1.0
                    klass, cx, cy, w, h = [float(x) for x in line.split()]
                except:
                    is_gt = False
            if not is_gt:
                klass, cx, cy, w, h, conf = [float(x) for x in line.split()]
            roi[slice].append(BB(patient, slice, cx, cy, w, h, klass, conf))
            # print(f'roi[slice] = {roi[slice]}')

    return bb

confidence_min = 0.2
iou_min = 0.1

def iou(a: BB, b: BB) -> float:
    left = max(a.x - a.w/2, b.x - b.w/2)
    right = min(a.x + a.w/2, b.x + b.w/2)
    top = max(a.y - a.h/2, b.y - b.h/2)
    bottom = min(a.y + a.h/2, b.y + b.h/2)
    if left >= right or bottom <= top:
        return 0
    cross_area = (right - left) * (bottom - top)
    a_area = a.w * a.h
    b_area = b.w * b.h
    return cross_area / (a_area + b_area - cross_area)

class Stat:
    def __init__(self):
        self.false_positive_list: List[BB] = []
        self.false_negative_list: List[BB] = []
        self.num_gt_bb = 0
        self.num_pred_bb = 0
        self.num_wrong_klass = 0
        self.area_gt = 0.0
        self.area_pred = 0.0

    def compare_slice(self, gt_slice, pred_slice):
        self.num_gt_bb += len(gt_slice)
        for bb in gt_slice:
            self.area_gt += bb.w * bb.h
        for bb in pred_slice:
            if bb.confidence > confidence_min:
                self.area_pred += bb.w * bb.h
                self.num_pred_bb += 1

    def add_fp(self, bb: BB):
        self.false_positive_list.append(bb)

    def add_fn(self, bb: BB):
        self.false_negative_list.append(bb)

    def add_wrong_klass(self, gt: BB, pred: BB):
        self.num_wrong_klass += 1

    def fp_average_area(self) -> float:
        if not self.false_positive_list:
            return 0.0
        area = 0
        for bb in self.false_positive_list:
            area += bb.w * bb.h
        return area / len(self.false_positive_list)

    def fn_average_area(self) -> float:
        if not self.false_negative_list:
            return 0.0
        area = 0
        for bb in self.false_negative_list:
            area += bb.w * bb.h
        return area / len(self.false_negative_list)

    def gt_average_area(self):
        return self.area_gt / self.num_gt_bb

    def pred_average_area(self):
        return self.area_pred / self.num_pred_bb

stat = Stat()

def compare_slice(gt_slice: List[BB], pred_slice: List[BB]):
    stat.compare_slice(gt_slice, pred_slice)

    not_matched_gt = set(gt_slice)
    for pred in pred_slice:
        conf = pred.confidence
        if conf < confidence_min:
            continue
        for gt in gt_slice:
            if pred.klass != gt.klass:
                continue
            if iou(gt, pred) > iou_min:
                # got the matching gt data
                try:
                    not_matched_gt.remove(gt)
                except:
                    print('double match ', gt)
                    pass
                break
        else:
            # no such gt. bogus prediction. false positive
            stat.add_fp(pred)
            for gt in gt_slice:
                if pred.klass != gt.klass and iou(pred, gt) > iou_min:
                    stat.add_wrong_klass(gt, pred)
                    break
    for gt in not_matched_gt:
        stat.add_fn(gt)


def get_suv_mean(bbox_list: List[BB]):
    suv_slice_mean = 0
    bbox_area = 0

    for b in bbox_list:
        # img_path = f'E:/HSE/LungCancerDetect/data/images/test/{patient}/{patient}_slice{slice}.jpg'
        pet_file = f'E:/HSE/LungCancerDetect/data/images/test/{b.patient}/PET_cut.nii.gz'
        img_pet = sitk.ReadImage(pet_file)
        img_pet_arr = sitk.GetArrayFromImage(img_pet)
        img_pet_arr = img_pet_arr[:, ::-1, :]
        x_dim, y_dim = 160, 128
        w = b.w * x_dim
        h = b.h * y_dim
        x1 = (b.x - b.w * 0.5) * x_dim
        x2 = (b.x + b.w * 0.5) * x_dim
        y1 = (b.y - b.h * 0.5) * y_dim
        y2 = (b.y + b.h * 0.5) * y_dim

        bbox_pet = img_pet_arr[int(b.slice), round(y1):round(y2)+1, round(x1):round(x2)+1]
        if bbox_pet.size == 0:
            print(f'bbox_pet empty: x1 = {x1}, x2 = {x2}, y1 = {y1}, y2 = {y2}, w = {w}, h = {h}')
            continue

        suv_slice_mean += np.sum(bbox_pet)
        bbox_area += w * h

    suv_mean_area = suv_slice_mean / bbox_area
        # suv_mean_sum += suv_slice_mean
    print(f'suv_slice_mean = {suv_slice_mean}')
    print(f'len(patient_list) = {len(bbox_list)}')
    # suv_total_mean = suv_slice_mean / len(patient_list)
    # return suv_slice_mean / len(bbox_list)

    return suv_mean_area


def get_suv_mean_dict(gt_bb: BBCollections):
    suv_slice_mean = 0
    bbox_count = 0
    bbox_area = 0
    for patient in gt_bb:
        pet_file = f'E:/HSE/LungCancerDetect/data/images/test/{patient}/PET_cut.nii.gz'
        img_pet = sitk.ReadImage(pet_file)
        img_pet_arr = sitk.GetArrayFromImage(img_pet)
        img_pet_arr = img_pet_arr[:, ::-1, :]
        for slice in gt_bb[patient]:
            for b in gt_bb[patient][slice]:
                x_dim, y_dim = 160, 128
                w = b.w * x_dim
                h = b.h * y_dim
                x1 = (b.x - b.w * 0.5) * x_dim
                x2 = (b.x + b.w * 0.5) * x_dim
                y1 = (b.y - b.h * 0.5) * y_dim
                y2 = (b.y + b.h * 0.5) * y_dim

                bbox_pet = img_pet_arr[int(b.slice), round(y1):round(y2) + 1, round(x1):round(x2) + 1]
                if bbox_pet.size == 0:
                    print(f'bbox_pet empty: x1 = {x1}, x2 = {x2}, y1 = {y1}, y2 = {y2}, w = {w}, h = {h}')
                    continue
                bbox_count += 1
                suv_slice_mean += np.sum(bbox_pet)
                bbox_area += w * h
    # return suv_slice_mean / bbox_count
    return suv_slice_mean / bbox_area


def analysis(gt_file: str, pred_file: str):
    gt_bb = load_label_files(gt_file)
    num_gt_slice = sum(len(p) for p in gt_bb)
    pred_bb = load_label_files(pred_file)
    num_pred_slice = sum(len(p) for p in pred_bb)
    for patient in gt_bb:
        for slice in gt_bb[patient]:
            compare_slice(gt_bb[patient][slice], pred_bb[patient][slice])

    fp_suv_mean = get_suv_mean(stat.false_positive_list)
    fn_suv_mean = get_suv_mean(stat.false_negative_list)
    gt_suv_mean = get_suv_mean_dict(gt_bb)
    pred_suv_mean = get_suv_mean_dict(pred_bb)
    print(f'fp suv mean = {fp_suv_mean}')
    print(f'fn_suv_mean = {fn_suv_mean}')
    print(f'gt_suv_mean = {gt_suv_mean}')
    print(f'pred_suv_mean = {pred_suv_mean}')

    print(f'gt num patient = {len(gt_bb)} total slice num = {num_gt_slice}')
    print(f'pred num patient = {len(pred_bb)} total slice num = {num_pred_slice}')
    print(f'fp mean area = {stat.fp_average_area()} num = {len(stat.false_positive_list)}')
    print(f'false_negative_list = {stat.false_negative_list}')
    print(f'list type = {type(stat.false_negative_list)}')
    # for fn in stat.false_negative_list:
    #     print(f'fn type = {type(fn)}')

    print(f'fn mean area = {stat.fn_average_area()} num = {len(stat.false_negative_list)}')
    print(f'gt mean area = {stat.gt_average_area()} num = {stat.num_gt_bb}')

    print(f'pred mean area = {stat.pred_average_area()} num = {stat.num_pred_bb}')
    print(f'wrong klass pred = {stat.num_wrong_klass}')
    return gt_bb, pred_bb, stat


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--confidence', type=float, default=0.3, help='minimum confidence from predictions')
    parser.add_argument('--iou', type=float, default=0.2, help='minimum iou for matching')
    parser.add_argument('--gt', type=str, default='test_gt.zip', help='gt label zip file')
    parser.add_argument('--pred', type=str, default='test_pred.zip', help='prediction label zip file')
    parser.add_argument('--gui', type=bool, default=True, help='show viewer for bounding box')
    opt = parser.parse_args()

    confidence_min = opt.confidence
    iou_min = opt.iou
    bb_gt, bb_pred, stat = analysis(opt.gt, opt.pred)
    # if opt.gui:
    #     from bbplot import plot
    #     plot(bb_gt, bb_pred)