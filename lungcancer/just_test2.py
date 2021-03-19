import PIL.Image as pilimg
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from sklearn import metrics

y = np.array([1, 1, 2, 2])
pred = np.array([0.1, 0.4, 0.35, 0.8])
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
print(metrics.auc(fpr, tpr))
#
# ct_img = pilimg.open( r'E:\HSE\PyTorch-YOLOv3\data\temp\images\test\46332866\CT-cut-slice000.jpg')
# # ct_img.show()
# ct_array  = np.array(ct_img)
# np.save(r'E:\HSE\PyTorch-YOLOv3\data\temp\images\test\46332866\justtest', ct_array)
# load_ct = np.load(r'E:\HSE\PyTorch-YOLOv3\data\temp\images\test\46332866\justtest.npy')
# # plt.imshow(ct_array)
# pil_pet = Image.fromarray(pet_trans.astype('float64'))
# pil_pet.show()
# print('load ct type = ', type(load_ct))
# print('ct array type = ', type(ct_array))
# print(np.all(load_ct == ct_array))
# print(load_ct == ct_array)
# pil_ct = Image.fromarray(ct_array)
# pil_ct.show()
# class Counter:
#     def __init__(self, stop):
#         self.stop = stop
#
#     def __getitem__(self, index):
#         if index < self.stop:
#             print('index = ', index)
#             return index*10
#         else:
#             raise IndexError
#
#
# print(Counter(3)[0], Counter(7)[5], Counter(3)[2])
# # print(Counter(5)[4])
# #
# for i in Counter(10):
#     print('i = ', i)