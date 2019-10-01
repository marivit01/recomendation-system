import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.model_selection import train_test_split

def getAvailableSubjects(studentId):
    studentId = int(studentId)
    # one_hot_path = os.path.abspath('..\\datos\\ordenados\\one_hot.csv')
    one_hot_path = os.path.abspath('..\\datos\\modelos\\model-5\\one_hot_new_classes.csv')
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    assigns_trim_target = []
    for est, est_group in grouped:
        for num in range(est_group.shape[0]):
            assigns_trim_target = np.append(assigns_trim_target, est_group.iloc[num, 2:].index[est_group.iloc[num, 2:] == 1].values.tolist(), axis=None)

    assigns_trim_target_aux = []
    for assign in assigns_trim_target:
        print(assign.split('_')[0])
        # Validacion para no incluir la materia en el array de materias vistas si el estudiante no la ha pasado (reprobado o retirado)
        if (assign.split('_')[1] == "Reprobo" or assign.split('_')[1] == "R"):
            print("aqui paso algo",assign.split('_')[1])
            continue
        # Validacion para no incluir como vista la materia Electiva, para que el estudiante pueda elegirla siempre como opcion
        if (assign.split('_')[0] == "FGE0000"):
            continue
        assigns_trim_target_aux = np.append(assigns_trim_target_aux, assign.split('_')[0], axis=None)
    print(np.asarray(assigns_trim_target_aux).tolist())

    #NUEVO
    seenSubjects = np.asarray(assigns_trim_target_aux)
    path = os.path.abspath('..\\datos\\subjectNames.csv')
    subjectNames = pd.read_csv(path).sort_values('asignatura')

    # Se obtienen las materias que el estudiante no ha visto
    mask = subjectNames['asignatura'].isin(seenSubjects)
    availableSubjects = subjectNames[~mask]

    # Se llama a la función para transformar las materias disponibles en un array con {code, name}
    total_credits, bp_credits = getCredits(seenSubjects)
    availableSubjectsFormatted = getSubjectsNames(availableSubjects, total_credits, bp_credits)
    return availableSubjectsFormatted

# Función que recibe un array de las materias que un estudiante no ha visto, 
# y lo devuelve en formato code, name para pasarlo al manejador
def getSubjectsNames(availablesArray, total_credits, bp_credits):
    subjectsArray = []
    for idx, subject in availablesArray.iterrows():
        print("valores", subject.values, subject.values[5], subject.values[6])
        subject_disabled = False

        if (isinstance(subject.values[8], str)):
            print("las vio", availablesArray['asignatura'].isin(subject.values[8].split(' ')))
            if (availablesArray['asignatura'].isin(subject.values[8].split(' ')).any() == False): 
                    print("vio alguna de las siguientes de estas")
                    subject_disabled = True

        if (isinstance(subject.values[3], str)):
            # print("split", availablesArray, subject.values[3].split(' '),availablesArray['asignatura'].isin(subject.values[3].split(' ')).any())
            if (np.isnan(subject.values[6]) == False):
                print("creditos bp")
                # Determina si el estudiante no ha visto la materia ni ha cumplido con los creditos bp si aplica
                if (availablesArray['asignatura'].isin(subject.values[3].split(' ')).any() and subject.values[6] > bp_credits):
                    print("no cumple con los creditos BP ni las asignaturas")
                    subject_disabled = True
            else:
            	# Determina si no ha visto alguna de las materias preladas para ponerle el disable true
                if (availablesArray['asignatura'].isin(subject.values[3].split(' ')).any()): 
                    print("no ha visto las prelatorias")
                    subject_disabled = True

        # Determina si el estudiante cumple con los requisitos de creditos si los tiene
        if (np.isnan(subject.values[5]) == False):
            print("hay creditos")
            if (np.isnan(subject.values[6]) == False):
                if (subject.values[5] > total_credits and subject.values[6] > bp_credits):
                    print("no cumple con los creditos ni bp ni normales")
                    subject_disabled = True
            else:
                if (subject.values[5] > total_credits):
                    print("no cumple con los creditos")
                    subject_disabled = True

        tmp = {'code':subject.values[1], 'name':subject.values[2], 'disabled': subject_disabled}
        # print("tmp", tmp)
        subjectsArray.append(tmp)
    print(subjectsArray)
    return subjectsArray

def getCredits(seenSubjects):
    total_credits = 0
    bp_credits = 0
    print("seen subjects", seenSubjects)
    for subject in seenSubjects:
        print("subject seen", subject)
        total_credits += 1
        if (subject.find('BP') == 0):
            print("bp is here")
            bp_credits += 1

    total_credits *= 3 
    bp_credits *= 3
    print("credits", total_credits, bp_credits)
    return (total_credits, bp_credits)

# Función que recibe un array de las materias que un estudiante no ha visto, 
# y che
# def getPrelaciones(assignCode, availablesArray):
#     # Rama de ingles
#     if(assignCode == 'FBTIN04' AND availablesArray.):


# def removeUnnecessary(availablesArray):

# def getQuarters():
    