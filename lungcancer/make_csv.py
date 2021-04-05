# create csv file for patients that only has lymph node

import csv
import os

lymph_only_patient = ['PTID','18153556', '18682799', '18838996',
    '23525317', '23779703', '23920587', '25827660', '26158932', '26975214', '27231760', '28389826',
 '28483658', '28719922', '30282687', '30797134', '31294816', '32107061', '33287193', '33910671', '35130231',
 '36521917', '37366384', '37494708', '37650926', '38770614', '38867734', '39141644', '39342447', '40412308',
 '40467687', '40733740', '42072364', '42101659', '42110569', '42153845', '42575539', '42870227', '43082915',
 '43759936', '44208563', '44252135', '44506128', '44760528', '46198794', '46392318']

print(f'patient = {lymph_only_patient}')
print(f'type = {type(lymph_only_patient)}, length = {len(lymph_only_patient)}')

os.chdir('E:/HSE/')
with open('only_lymph_patient.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for p in lymph_only_patient:
        writer.writerow([p])