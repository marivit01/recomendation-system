import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.model_selection import train_test_split

def adapty(assigns_trim_target):
    array_target = []

    all_assigns = ['FBTCE03','FBTMM00','FBTHU01','FBTIE02','BPTQI21','BPTMI04','FBPIN01'
    ,'BPTPI07','FBPLI02','FBTIN04','FGE0000','FBPCE04','FBPMM02','FBTIN05'
    ,'FBPIN03','FBPIN02','FBPLI01','FBPCE03','FBPMM01','FBTHU02','FBTSP03'
    ,'BPTFI02','BPTMI11','BPTSP05','BPTMI01','FBTCE04','FBTMM01','FGS0000'
    ,'FBTIE03','BPTFI03','BPTMI20','BPTFI01','BPTQI22','BPTMI05','BPTMI30'
    ,'BPTSP06','BPTMI02','BPTMI03','FPTCS16','FPTSP15','BPTEN12','BPTMI31'
    ,'FPTEN23','BPTSP03','BPTFI04','FPTSP14','BPTDI01-1','FBTIE01','FPTSP20'
    ,'FPTMI21','BPTSP04','FPTSP01','FPTSP18','FPTSP22','FPTSP17','FPTPI09'
    ,'FPTSP11','FPTSP04','FPTSP02','BPTDI01-2','FPTSP23','FPTSP19','FPTSP07'
    ,'FPTSP25','FPTSP21','FPTIS01']

    print('LEEEEEEEEEENGTH', all_assigns.__len__())

    only_assigns = {}
    for assign_zero in all_assigns:
      only_assigns[assign_zero] = 0
      
    for assign in assigns_trim_target:
      print(assign)
      only_assigns[assign] = 1
      
    array_target.append(np.array( tuple(only_assigns.values()) ))
    print('SHAAAAAAAPE', np.asarray(array_target).shape)
    return np.asarray(array_target)