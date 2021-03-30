import matplotlib as mpl
import matplotlib.pylab as plt
import sys
import os
import numpy as np
import nibabel as nib
from nilearn import plotting
from nibabel.testing import data_path
from nilearn import image
import pydicom as dcm
from lungmask import mask
import SimpleITK as sitk

#example
input_image = sitk.ReadImage('F:/03. DataSet/Lung Cancer (PET-CT)/SNUH_lung/10918160/CT_20120912/1.3.12.2.1107.5.99.2.64000.30000012091101273093700005719.dcm')
segmentation = mask.apply(input_image)  # default model is U-net(R231)
print('type = ', type(segmentation))
model = mask.get_model('unet','LTRCLobes')
segmentation2 = mask.apply(input_image, model)
segmentation3 = mask.apply_fused(input_image)