#%%
## Imports
import pandas as pd
import numpy as np
import os 
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dropout, Dense, Flatten, Activation, LSTM, Bidirectional, Concatenate
from keras.models import Model

import matplotlib.pyplot as plt

# Para almacenar y obtener el modelo para predicciones futuras de un archivo .pkl.
from sklearn.externals import joblib

from IPython.display import HTML, display
import time

#%%
"""## Cargar el One Hot"""
#%%
import os.path
fullpath = os.path.abspath('..\\recomendation-system\\backend\one_hot.csv')
df = pd.read_csv(fullpath, encoding='latin-1')

#%%
"""## Agrupar estudiantes y ordenar por trimestres"""
#%%
grouped = df.sort_values('trimestre').groupby(['estudiante'])
print('grouped', grouped.get_group(10024705))

#%%
"""## Separando el data set
Se separa el dataset en train y test. Luego, se crean las variables X y Y con las que se van a entrenar al modelo."""

#%%
"""**Auxiliar para mostrar el avance**
"""
#%%
def progress(value, max=100):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))

#%%
"""**Estableciendo la y de cada x**"""
#%%
# Contains all codes for asignatures in pensum of System Engineer
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

#%%
## Formateando la data

array_data = [] # Contains the history of trimestres
array_target=[] # The target trimestres
array_target_output=[] # Output that specifies if the target is posible (all passed) or not

# Máximos de numero de trimestre y número de asignaturas
max_number_trim = grouped.count()['trimestre'].max()
max_number_assigns = 10

# Variables para el loader
out_estudiante = display(progress(0, len(grouped)), display_id=True)
i_estudiante = 0
out_trim = display(progress(0, len(grouped)), display_id=True)

# For para recorrer cada grupo de estudiantes
for est, est_group in grouped:
  i_estudiante += 1 # variable para el loader
  out_estudiante.update(progress(i_estudiante, len(grouped))) # progreso del loader
  count = 0 # contador loader
  
  for cant_trim in range(est_group.shape[0]):
    count += 1 # contador loader
    out_trim.update(progress(count, est_group.shape[0])) # progreso loader
    
    # Inicialización de row
    row = {}
    row_trim = []
    
    # Validador si la cantidad de trimestres (proveniente del for) es 0
    if cant_trim == 0:
      continue
    
    # Rellenar todos los espacios de trimestres con "asignaturas con notas" en 0 
    for num_empty in range(max_number_trim - 1):
      row_trim.append(np.zeros((264), dtype=int))
    
    # Variable para determinar donde empiezan a llenarse con trimestres vistos 
    start_trim = max_number_trim - cant_trim
    
    # For para establecer valores de trimestres
    for num in range(cant_trim): 
      if num == cant_trim:
        continue
      row_trim[start_trim + num - 1] = est_group.iloc[ num , 3:].values
    
    
#     row['trim_data'] = np.asarray(row_trim)
    # Anexa filas con los trimestres vistos en cada una a array_data
    array_data.append(np.asarray(row_trim))
    
    # Obtiene las materias que el estudiante verá en el trimestre target
    assigns_trim_target = est_group.iloc[num+1, 3:].index[est_group.iloc[num+1, 3:] == 1].values # Obtain only assginatures with grades that the student have 
    
    # Arma el array_target
    only_assigns = {}
    
    # Establece en 0 todas las posiciones de las materias
    for assign_zero in all_assigns:
      only_assigns[assign_zero] = 0
    
    # Establece 1 en los códigos de las materias donde el estudiante verá materias en el trim_target
    for assign in assigns_trim_target:
      only_assigns[assign.split('_')[0]] = 1
#     row['trim_target'] = np.array(only_assigns)

    # Arma el array_target
    array_target.append(np.array( tuple(only_assigns.values()) ))  
  
    # Arma el array_target_output
    array_target_output.append(est_group.iloc[ num+1 , 3:].values)

#%%
"""**Estableciendo el target para cada entrada**

Se crea un array de targets, en el que para cada row del array de trimestres objetivo (target): 

*   Se asigna 1 si se obtuvo una calificación buena/mala en todas las materias. 
*   Se asigna 0 si reprobó/retiró alguna materia.
"""

#%%
# Se crea el array de targets que tiene 0 si el estudiante reprobo o retiro alguna materia en el trimestre target, y 1 en caso contrario

arr_target = np.asarray(array_target_output)

print(arr_target.shape, arr_target.shape[0])
sigm_target = np.zeros((arr_target.shape[0], 1), dtype=int)

for idx,item in enumerate(arr_target):
  columns = 4
  aux, mal, bien, reprobo, retiro = 0, 0, 0, 0, 0
  for one in range(int(item.shape[0]/4)):
    for col in range(columns):
      if item[col+columns*aux] == 1:
        if col == 0:
          mal += 1
        elif col == 1:
          bien += 1
        elif col == 2:
          reprobo += 1
        elif col == 3:
          retiro += 1
    aux += 1
  
  # Si no hay alguna materia reprobada o retirada, se asigna 1
  if reprobo == 0 and retiro == 0:
    sigm_target[idx] = 1

#%%
print(sigm_target.shape)
print(sigm_target)

#%%
"""**Adaptando el y de cada x**"""
#%%
print(array_data)

#%%
"""**Separando el conjunto de datos en los conjuntos de train, dev y test**"""
#%%
# Se separa el dataset en la proporción 80-20-20 para train, dev y test respectivamente
array_data = np.asarray(array_data)
array_target = np.asarray(array_target)

X_train, X_test, Y_train, Y_test, O_train, O_test = train_test_split(array_data,array_target,sigm_target, test_size=0.2, random_state=27014)
X_train, X_dev, Y_train, Y_dev, O_train, O_dev = train_test_split(X_train, Y_train, O_train, test_size=0.25, random_state=27014)  # Sería el equivalente al 20% de toda la data
print(X_train.shape)
print(Y_train.shape)
print(O_train.shape)

print(X_dev.shape)
print(Y_dev.shape)
print(O_dev.shape)

print(X_test.shape)
print(Y_test.shape)
print(O_test.shape)
print(array_data.shape)

#%%
"""## Definición del modelo

Se construye un modelo que recibe dos entradas, un array de los trimestres del estudiante, y otro del trimestre objetivo o target, y un output tipo sigmoide que indica 1 si el estudiante pasará todas las materias, y 0 en caso contrario.
"""

#%%
def model_opc1():
  # Se definen dos inputs
  main_input = Input(shape=(29,264), name='main_input')
  second_input = Input(shape=(66,), name='second_input')
  
  # Se utiliza el main_input para la LSTM
  X = LSTM(32, return_sequences=False, dropout=0.1, recurrent_dropout=0.1)(main_input)
  X = Dense(264, activation='relu')(X)
  X = Dropout(0.2)(X)
  lstm_out = Dense(264, activation='sigmoid')(X)
  
  # Se concatena el output de la LSTM con el segundo input
  X = Concatenate()([lstm_out, second_input])
  X = Dense(64, activation='relu')(X)
  
  
  main_output = Dense(1, activation='sigmoid', name='main_output')(X)
  model = Model(inputs=[main_input, second_input], outputs=[main_output])
  
  # Compile the model
  model.compile(
      optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy'])

#   history = model.fit([X_train, Y_train],  O_train, 
#                       batch_size=16, epochs=5,
#                       validation_data=([X_dev, Y_dev], O_dev))
  
  history = model.fit({'main_input': X_train, 'second_input': Y_train},
                      {'main_output': O_train}, batch_size=16, epochs=5, 
                      validation_data=([X_dev, Y_dev], O_dev))

  print(model.summary())

  # Persistencia del modelo: almacenarlo para las predicciones 
  joblib.dump(model, '../datos/modelos/model1.pkl')
  
  return (model, history)

#%%
def model_opc2():
  # Se definen dos inputs
  main_input = Input(shape=(29,264), name='main_input')
  second_input = Input(shape=(66,), name='second_input')
  
  # La primera rama utiliza el main_input para la LSTM
  X = LSTM(32, return_sequences=False, dropout=0.1, recurrent_dropout=0.1)(main_input)
  X = Dense(264, activation='relu')(X)
  X = Dropout(0.2)(X)
  X = Dense(264, activation='sigmoid')(X)
  X = Model(inputs=main_input, outputs=X)
  
  # La segunda rama utiliza el second_input
  Y = Dense(264, activation='relu')(second_input)
  Y = Model(inputs=second_input, outputs=Y)

  # Se combinan los outputs de las dos ramas
  combined = Concatenate()([X.output, Y.output])
  main_output = Dense(1, activation='sigmoid', name='main_output')(combined)
  
  model = Model(inputs=[X.input, Y.input], outputs=[main_output])
  
  # Compile the model
  model.compile(
      optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy'])

  history = model.fit([X_train, Y_train],  O_train, 
                      batch_size=16, epochs=5,
                      validation_data=([X_dev, Y_dev], O_dev))
  
#   history = model.fit({'main_input': X_train, 'second_input': Y_train},
#                       {'main_output': O_train}, batch_size=16, epochs=5, 
#                       validation_data=([X_dev, Y_dev], O_dev))

  print(model.summary())

  # Persistencia del modelo 2: almacenarlo para las predicciones 
  joblib.dump(model, '../datos/modelos/model2.pkl')

  return (model, history)

#%%
model_1, history_m1 = model_opc1()

#%%
model_2, history_m2 = model_opc2()

#%%
"""## Graficar modelo"""

#%%
def graf_model(train_history):
    f = plt.figure(figsize=(15,10))
    ax = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    # summarize history for accuracy
    ax.plot(train_history.history['binary_accuracy'])
    ax.plot(train_history.history['val_binary_accuracy'])
    ax.set_title('model accuracy')
    ax.set_ylabel('accuracy')
    ax.set_xlabel('epoch')
    ax.legend(['train', 'test'], loc='upper left')
    # summarize history for loss
    ax2.plot(train_history.history['loss'])
    ax2.plot(train_history.history['val_loss'])
    ax2.set_title('model loss')
    ax2.set_ylabel('loss')
    ax2.set_xlabel('epoch')
    ax2.legend(['train', 'test'], loc='upper left')
    plt.show()

#%%
graf_model(history_m1)

#%%
graf_model(history_m2)

#%%
"""## Test del modelo"""
#%%
print(Y_test.shape)

# # x_test_df = pd.DataFrame(X_test)
# y_test_df = pd.DataFrame(Y_test)

# # x_test_df.to_csv('x_test_def.csv', index=False)
# y_test_df.to_csv('y_test_def.csv')
# # !cp x_test_def.csv drive/Shared\ drives/Tesis/Proyecto\ de\ investigación/Modelo\ 2/Datos
# !cp y_test_def.csv drive/Shared\ drives/Tesis/Proyecto\ de\ investigación/Modelo\ 2/Datos

#%%
"""*Cargar archivos para probar de forma manual*"""
#%%
# np_load_test = np.load
# np.load = lambda *a,**k: np_load_test(*a, allow_pickle=True, **k)

# # np.load = np_load_test

#%%
# array_data_test = np.load('drive/Shared drives/Tesis/Proyecto de investigación/Modelo 2/Datos/array_data_df.npy')
# array_target_test = np.load('drive/Shared drives/Tesis/Proyecto de investigación/Modelo 2/Datos/array_target_df.npy')
#%%
# print(array_data_test)
# print(array_target_test)

#%%
"""*Respuesta*"""
#%%
# Y_hat = model_2.predict([array_data_test, array_target_test])

# print(Y_hat)
# # print(O_test)

#%%
"""*Subir un excel con el resultado a drive*"""
#%%
# mercy_hat_df = pd.DataFrame(Y_hat)
# y_df = pd.DataFrame(O_test)

# filepath = 'y_hat_df_model_2_opc_2.xlsx'
# y_hat_df.to_excel(filepath, index=False)
# y_df.to_excel('y_df_model_2_opc_2.xlsx')
# !cp y_hat_df_model_2_opc_2.xlsx drive/Shared\ drives/Tesis/Proyecto\ de\ investigación/Modelo\ 2/Datos
# !cp y_df_model_2_opc_2.xlsx drive/Shared\ drives/Tesis/Proyecto\ de\ investigación/Modelo\ 2/Datos

#%%
"""## Referencias

https://www.pyimagesearch.com/2019/02/04/keras-multiple-inputs-and-mixed-data/

https://keras.io/getting-started/functional-api-guide/

https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tolist.html
"""

