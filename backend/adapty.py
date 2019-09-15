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

  all_assigns.sort()

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

def adaptYModel3(assigns_trim_target):
  array_target = []

  all_assigns = ['FBTCE03','FBTMM00','FBTHU01','FBTIE02','BPTQI21','BPTMI04','FBPIN01'
  ,'BPTPI07','FBPLI02','FBTIN04','FGE0000','FBPCE04','FBPMM02','FBTIN05'
  ,'FBPIN03','FBPIN02','FBPLI01','FBPCE03','FBPMM01','FBTHU02','FBTSP03'
  ,'BPTFI02','BPTMI11','BPTSP05','BPTMI01','FBTCE04','FBTMM01','FGS0000'
  ,'FBTIE03','BPTFI03','BPTMI20','BPTFI01','BPTQI22','BPTMI05','BPTMI30'
  ,'BPTSP06','BPTMI02','BPTMI03','FPTCS16','FPTSP15','BPTEN12','BPTMI31'
  ,'FPTEN23','BPTSP03','BPTFI04','FPTSP14','FBTIE01','FPTSP20'
  ,'FPTMI21','BPTSP04','FPTSP01','FPTSP18','FPTSP17','FPTPI09'
  ,'FPTSP11','FPTSP04','FPTSP02','FPTSP23','FPTSP19','FPTSP07'
  ,'FPTSP25','FPTSP21']

  all_assigns.sort()
  print("sorted", all_assigns)

  print('LEEEEEEEEEENGTH', all_assigns.__len__())

  only_assigns = {}
  for assign_zero in all_assigns:
    only_assigns[assign_zero] = 0
    
  for assign in assigns_trim_target:
    print(assign)
    only_assigns[assign] = 1 
    
  array_target.append(np.array( tuple(only_assigns.values()) ))
  print('SHAAAAAAAPE', np.asarray(array_target).shape)
  print(np.asarray(array_target))
  return np.asarray(array_target)

def adaptYModel4(assigns_trim_target):
  array_target = []
  max_number_assigns = 10

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

  all_assigns.sort()
  
  # Rellenar todos los espacios de materias target en 0 
  row_assigns = []
  output_assigns = []
  
  for num_empty in range(max_number_assigns):
    row_assigns.append(np.zeros((66), dtype=int))
    output_assigns.append(0)

  # Determinar la cantidad de materias target elegidas
  print('CANTIDAD: ', len(assigns_trim_target))
  cant_assigns = len(assigns_trim_target)

  # Variable para determinar donde empiezan a llenarse con materias target
  start_assign = max_number_assigns - cant_assigns

  # Verificación de que el array de materias target esté ordenado alfabéticamente
  print('Y original:', assigns_trim_target)
  assigns_trim_target.sort()
  print('Y ordenado:', assigns_trim_target)

  for idx, assign in enumerate(assigns_trim_target):
    # Arma el array_target
    only_assigns = {}

    # Establece en 0 todas las posiciones de las materias
    for assign_zero in all_assigns:
      only_assigns[assign_zero] = 0
    
    # Establece 1 en los códigos de las materias que el estudiante verá en el trim_target
    only_assigns[assign.split('_')[0]] = 1
    row_assigns[start_assign + idx] = np.array(tuple(only_assigns.values()))

  # Anexa filas con el one hot de cada materia elegida en el array_target
  array_target.append(np.asarray(row_assigns))
    
  print('SHAPE TARGET:', np.asarray(array_target).shape)
  return np.asarray(array_target)