from typing import Dict, Tuple, List
import re
from zipfile import ZipFile
from collections import defaultdict

from bbutil import BB, BBCollections

def load_label_files(f: str) -> BBCollections:
    is_gt = True
    z = ZipFile(f)
    bb = {}
    filepattern = re.compile(r'(\d+)_slice(\d+).txt')
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
            roi[slice].append(BB(cx, cy, w, h, klass, conf))
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

def analysis(gt_file: str, pred_file: str):
    gt_bb = load_label_files(gt_file)
    num_gt_slice = sum(len(p) for p in gt_bb)
    pred_bb = load_label_files(pred_file)
    num_pred_slice = sum(len(p) for p in pred_bb)
    for patient in gt_bb:
        for slice in gt_bb[patient]:
            compare_slice(gt_bb[patient][slice], pred_bb[patient][slice])

    print(f'gt num patient = {len(gt_bb)} total slice num = {num_gt_slice}')
    print(f'pred num patient = {len(pred_bb)} total slice num = {num_pred_slice}')
    print(f'fp mean area = {stat.fp_average_area()} num = {len(stat.false_positive_list)}')
    print(f'false_negative_list = {stat.false_negative_list}')
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
    # 점선이 림프
    # 실선이 primary
    # 빨간게 ground truth, 초록이 prediction