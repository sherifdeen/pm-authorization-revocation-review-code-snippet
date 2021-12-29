
import itertools

ua_1 = ['grpHead', 'regHead']
ua_2 = [] #'TransSup', 'ATMCus'
ua_3 = ['Backup']
ua_4 = ['OpOff']
source = ['Cathy']


#attMap = {'ua_1': ua_1, 'ua_2': ua_2, 'ua_3': ua_3, 'ua_4': ua_4, 'source': source}
#pdtMap = {'sourceByua_1': sourceByua_1, }


sourceByua_1 = []
for pdt in itertools.product(source, ua_1):
    sourceByua_1.append(pdt)
print('sourceByua_1 = ' + str(sourceByua_1))

ua_2Byua_1 = []
for pdt in itertools.product(ua_2, ua_1):
    ua_2Byua_1.append(pdt)
print('ua_2Byua_1 = {}'.format(ua_2Byua_1))
    
sourceByua_3 = []
for pdt in itertools.product(source, ua_3):
    sourceByua_3.append(pdt)
print('sourceByua_3 = {}'.format(sourceByua_3))
    
ua_3Byua_1 = []
for pdt in itertools.product(ua_3, ua_1):
    ua_3Byua_1.append(pdt)
print('ua_3Byua_1 = {}'.format(ua_3Byua_1))

ua_2Byua_4 =[]
for pdt in itertools.product(ua_2, ua_4):
    ua_2Byua_4.append(pdt)
print('ua_2Byua_4 = {}'.format(ua_2Byua_4))
    
ua_3Byua_4 = []
for pdt in itertools.product(ua_3, ua_4):
    ua_3Byua_4.append(pdt)
print('ua_3Byua_4 = {}'.format(ua_3Byua_4))
    
ua_2Byua_3 = []
for pdt in itertools.product(ua_2, ua_3):
    ua_2Byua_3.append(pdt)
print('ua_2Byua_3 = {}'.format(ua_2Byua_3))
    
ua_1Byua_3 = []
for pdt in itertools.product(ua_1, ua_3):
    ua_1Byua_3.append(pdt)
print('ua_1Byua_3 = {}'.format(ua_1Byua_3))


