import os
import glob


file_path1 = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
file_path2 = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
file_path3 = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')

patient_list = []
for i in file_path1:
    patient_num = i.split('\\')[-2]
    print(f'patient num = {patient_num}')
    patient_list.append(patient_num)

for i in file_path2:
    patient_num = i.split('\\')[-2]
    print(f'patient num = {patient_num}')
    patient_list.append(patient_num)

for i in file_path3:
    patient_num = i.split('\\')[-2]
    print(f'patient num = {patient_num}')
    patient_list.append(patient_num)

print(f'patient list len = {len(patient_list)}')
print(f'patient list set = {len(set(patient_list))}')