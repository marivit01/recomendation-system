import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.model_selection import train_test_split
import itertools

def getAvailableSubjects(studentId):
    studentId = int(studentId)
    # one_hot_path = os.path.abspath('..\\datos\\ordenados\\one_hot.csv')
    one_hot_path = os.path.abspath("../datos/modelos/model-5/one_hot_new_classes.csv")
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    assigns_trim_target = []
    for est, est_group in grouped:
        for num in range(est_group.shape[0]):
            assigns_trim_target = np.append(assigns_trim_target, est_group.iloc[num, 2:].index[est_group.iloc[num, 2:] == 1].values.tolist(), axis=None)

    assigns_trim_target_aux = []
    for assign in assigns_trim_target:
        # print(assign.split('_')[0])
        # Validacion para no incluir la materia en el array de materias vistas si el estudiante no la ha pasado (reprobado o retirado)
        if (assign.split('_')[1] == "Reprobo" or assign.split('_')[1] == "R"):
            # print("aqui paso algo",assign.split('_')[1])
            continue
        # Validacion para no incluir como vista la materia Electiva, para que el estudiante pueda elegirla siempre como opcion
        if (assign.split('_')[0] == "FGE0000"):
            continue
        assigns_trim_target_aux = np.append(assigns_trim_target_aux, assign.split('_')[0], axis=None)
    print("materias que vio", np.asarray(assigns_trim_target_aux).tolist())

    #NUEVO
    seenSubjects = np.asarray(assigns_trim_target_aux)
    path = os.path.abspath('../datos/subjectNames.csv')
    subjectNames = pd.read_csv(path).sort_values('asignatura')

    # Se obtienen las materias que el estudiante no ha visto
    mask = subjectNames['asignatura'].isin(seenSubjects)
    availableSubjects = subjectNames[~mask]

    # Se llama a la función para transformar las materias disponibles en un array con {code, name}
    total_credits, bp_credits = getCredits(seenSubjects)
    availableSubjectsFormatted = getSubjectsNames(availableSubjects, total_credits, bp_credits)
    return availableSubjectsFormatted

def getAvailableSubjects_test(studentId):
    studentId = int(studentId)
    # one_hot_path = os.path.abspath('..\\datos\\ordenados\\one_hot.csv')
    one_hot_path = os.path.abspath("../datos/modelos/model-5/one_hot_new_classes.csv")
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    assigns_trim_target = []
    for est, est_group in grouped:
        for num in range(est_group.shape[0] - 1):
            assigns_trim_target = np.append(assigns_trim_target, est_group.iloc[num, 2:].index[est_group.iloc[num, 2:] == 1].values.tolist(), axis=None)

    assigns_trim_target_aux = []
    for assign in assigns_trim_target:
        # print(assign.split('_')[0])
        # Validacion para no incluir la materia en el array de materias vistas si el estudiante no la ha pasado (reprobado o retirado)
        if (assign.split('_')[1] == "Reprobo" or assign.split('_')[1] == "R"):
            # print("aqui paso algo",assign.split('_')[1])
            continue
        # Validacion para no incluir como vista la materia Electiva, para que el estudiante pueda elegirla siempre como opcion
        if (assign.split('_')[0] == "FGE0000"):
            continue
        assigns_trim_target_aux = np.append(assigns_trim_target_aux, assign.split('_')[0], axis=None)
    print("materias que vio", np.asarray(assigns_trim_target_aux).tolist())

    #NUEVO
    seenSubjects = np.asarray(assigns_trim_target_aux)
    path = os.path.abspath('../datos/subjectNames.csv')
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
        # print("valores", subject.values, subject.values[5], subject.values[6])
        subject_disabled = False

        if (isinstance(subject.values[8], str)):
            ## CASO ESPECIAL LISTA 5 -> ORDEN: [materia lista siguiente, materia de lista 1]
            print("LENGTH: ", len(subject.values[8].split(' ')))
            if (len(subject.values[8].split(' ')) > 1):
                print("disponibles: ", availablesArray)
                print("materias que siguen:", subject.values[8].split(' '))
                print("m1:", list(subject.values[8].split(' ')[0]))
                print("m2:", list(subject.values[8].split(' ')[1]))

                print("SI O QUE: ", availablesArray['asignatura'].isin(list(subject.values[8].split(' ')[1])).any())

                # Asignaturas que no vio porque empezó en una lista que no las requiere o no hacen falta ver
                if (availablesArray['asignatura'].isin(list(subject.values[8].split(' ')[1])).any() == False): 
                    # Ya vio la materia que le seguia en la lista 1
                    subject_disabled = True
                elif (availablesArray['asignatura'].isin(list(subject.values[8].split(' ')[0])).any() == False): 
                    # Ya vio la materia que le seguir en la siguiente lista
                    subject_disabled = True
            else:
                if (availablesArray['asignatura'].isin(subject.values[8].split(' ')).any() == False): 
                    subject_disabled = True              

        if (isinstance(subject.values[3], str)):
            # print("disponibles: ", availablesArray)
            # print("materias que prelan:", subject.values[3].split(' '))
            # print("SI O QUE: ", availablesArray['asignatura'].isin(subject.values[3].split(' ')).any())

            if (np.isnan(subject.values[6]) == False):
                # Determina si el estudiante no ha visto la materia ni ha cumplido con los creditos bp si aplica
                if (availablesArray['asignatura'].isin(subject.values[3].split(' ')).any() and subject.values[6] > bp_credits):
                    # print("no cumple con los creditos BP ni las asignaturas")
                    subject_disabled = True
            else:
            	# Determina si no ha visto alguna de las materias preladas para ponerle el disable true
                if (availablesArray['asignatura'].isin(subject.values[3].split(' ')).any()): 
                    # print("no ha visto las prelatorias")
                    subject_disabled = True

        # Determina si el estudiante cumple con los requisitos de creditos si los tiene
        if (np.isnan(subject.values[5]) == False):
            if (np.isnan(subject.values[6]) == False):
                if (subject.values[5] > total_credits and subject.values[6] > bp_credits):
                    # print("no cumple con los creditos ni bp ni normales")
                    subject_disabled = True
            else:
                if (subject.values[5] > total_credits):
                    # print("no cumple con los creditos")
                    subject_disabled = True

        tmp = {'code':subject.values[1], 'name':subject.values[2], 'disabled': subject_disabled}
        subjectsArray.append(tmp)
    return subjectsArray

def getCredits(seenSubjects):
    total_credits = 0
    bp_credits = 0
    # print("seen subjects", seenSubjects)
    for subject in seenSubjects:
        # print("subject seen", subject)
        total_credits += 1
        if (subject.find('BP') == 0):
            bp_credits += 1

    total_credits *= 3 
    bp_credits *= 3
    # print("credits", total_credits, bp_credits)
    return (total_credits, bp_credits)

def createCombinations(availablesArray, preselectedArray, assignsNumber):
    combinations = []
    final_combinations = pd.DataFrame()
    availables = []

#  COMENTADO PORQUE AHORA DESDE EL FRONT SE OBTIENEN DIRECTAMENTE LOS CODIGOS
    # for subject in availablesArray:
    #     print('ITEM', subject['code'])
    #     availables.append(subject['code'])
    # print('availables:', availables)



    # if (assignsNumber != 'all'):
    #     assignsNumber = int(assignsNumber)

    #     # Obtener todas las combinaciones posibles de materias, de una longitud pasada por parametro
    #     combinations = list(itertools.combinations(availablesArray, assignsNumber))
    #     print('opc1: ', combinations)     


    if (assignsNumber != 'all'):
        print('length of presel', len(preselectedArray), preselectedArray)
        number = int(assignsNumber) - len(preselectedArray) # Establecer número de materias a evaluar incluyendo las preseleccionadas
        print('current number: ', number)
        combs = list(itertools.combinations(availablesArray, number))
        # Iterador para insertar las materias preseleccionadas
        if (preselectedArray and len(preselectedArray) > 0):
            new_combs = []
            for c in combs:
                for sel in preselectedArray:            
                    c = c + (sel,) # las combinaciones individuales son objeto 'tuple', así se concatenan
                    # print('SEEEEEL 2', sel, c)
                new_combs.append(c)
            combs = new_combs
        # print('COMBSSSSSS', new_combs)
        combs = pd.DataFrame(np.asarray(combs))
        # # print('comb: ',comb)
        # # print('comb array: ', np.asarray(comb))
        # # print('total comb: ',combinations)
        # print('shapes', combs.shape)
        # print('combs', combs)
        # # final_combinations = np.concatenate((final_combinations, combs), axis=None)
        final_combinations = pd.concat([final_combinations, combs])
        # final_combinations.append(combs)

        # final_combinations = final_combinations.replace(np.nan, '', regex=True)
        final_combinations = final_combinations.fillna(value='')
        # print('opc2: ', final_combinations)
    else:
        numbers = [2,3,4,5,6]

        # Obtener todas las combinaciones posibles de materias, de todas las longitudes posibles
        for number in numbers:
            number = number - len(preselectedArray)
            print('current number: ', number)
            combs = list(itertools.combinations(availablesArray, number))
            # Iterador para insertar las materias preseleccionadas
            if (preselectedArray and len(preselectedArray) > 0):
                new_combs = []
                for c in combs:
                    for sel in preselectedArray:            
                        c = c + (sel,) # las combinaciones individuales son objeto 'tuple', así se concatenan
                        # print('SEEEEEL 2', sel, c)
                    new_combs.append(c)
                combs = new_combs                
            combs = pd.DataFrame(np.asarray(combs))
            # # print('comb: ',comb)
            # # print('comb array: ', np.asarray(comb))
            # # print('total comb: ',combinations)
            # print('shapes', combs.shape)
            # print('combs', combs)
            # # final_combinations = np.concatenate((final_combinations, combs), axis=None)
            final_combinations = pd.concat([final_combinations, combs])
            # final_combinations.append(combs)

        # final_combinations = final_combinations.replace(np.nan, '', regex=True)
        final_combinations = final_combinations.fillna(value='')
        print('opc2: ', final_combinations)     
    
    # Print the obtained combinations 
    print('final combs: ', np.asarray(final_combinations))  
    return np.asarray(final_combinations)



    