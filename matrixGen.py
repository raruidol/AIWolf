import pandas as pd
import numpy as np
import re
from sklearn import preprocessing

def generate_matrix(file, name, test=False):
    dict={}
    dict['target'] = {}
    day = 0
    try:
        with open(file, 'r') as f:
            while True:
                line = f.readline().split(',')
                if line == ['']:
                    break
                #print(line)

                # Genero nuevas claves para un nuevo dia de la partida
                if day != int(line[0]):
                    day = int(line[0])
                    dict[day] = {}
                    dict[day]['talk'] = {}
                    dict [day]['vote'] = {}
                    dict [day]['dead'] = {}

                # Almaceno los roles de cada agente (id)
                if line[1] == 'status':
                    dict['target'][line[2]] = line[3]
                    if line[4] == 'DEAD':
                        dict[day]['dead'][int(line[2])] = True

                # Almaceno la sucesión de mensajes de cada agente para cada dia

                if line[1] == 'talk' and day!=0:
                    if int(line[4]) in dict[day]['talk']:
                        dict[day]['talk'][int(line[4])].append(line[5])

                    else:
                        dict[day]['talk'][int(line[4])] = []
                        dict[day]['talk'][int(line[4])].append(line[5])


                # Almaceno la votación realizada al finalizar cada dia
                elif line[1] == 'vote' and day != 0:

                    dict[day]['vote'][int(line[2])] = int(line[3])

            # accion[DEAD, VOTE, TALK]
            # detalle [ESTIMATE, COMINGOUT, DIVINATION, GUARD, VOTE, ATTACK, DIVINED, IDENTIFIED, GUARDED, VOTED, ATTACKED, SKIP/OVER]
            # msg_target [one_hot_player]
            # role [one_hot_roles]
            num_players = len(dict['target'].items())
            game = [[] for i in range(num_players)]
            mask = []
            #print(game)
            target = []
            in_dia = 0

            for k, v in dict['target'].items():
                target.append(v)
            tgt = []
            enc = preprocessing.OrdinalEncoder()
            X = np.array(target).reshape(-1, 1)
            enc.fit(X)
            for role in X:
                va = np.array([role])
                tgt.append(enc.transform(va))
            target = []
            for elem in tgt:
                target.append(int(elem[0][0]))
            num_roles = len(set(target))

            # clave-dia/target valor-tipo_accion{id}
            for key, value in dict.items():

                if key != 'target':

                    actions_day = 0
                    # clave-tipo_accion valor-id{sucesos}
                    for k, v in dict[key].items():
                        if k == 'talk':

                            day = []
                            # clave-id valor-[sucesos]
                            for k1, v1 in dict[key][k].items():
                                actions_day = len(v1)
                                acc_dia = []

                                # a -> mensaje
                                for a in v1:

                                    acc_dias = []
                                    accion = [0,0,0]
                                    detalle = [0]*12
                                    msg_target = [0]*num_players
                                    role = [0]*num_roles

                                    msg = re.split(' |\[|\]|\n', a)
                                    accion[2] = 1


                                    if msg[0] == 'ESTIMATE':
                                        detalle[0] = 1
                                        msg_target[int(msg[2]) - 1] = 1
                                        rol_cod = enc.transform([[msg[4]]])
                                        role[int(rol_cod[0][0])] = 1

                                    elif msg[0] == 'COMINGOUT':
                                        detalle[1] = 1
                                        msg_target[int(msg[2]) - 1] = 1
                                        rol_cod = enc.transform([[msg[4]]])
                                        role[int(rol_cod[0][0])] = 1

                                    elif msg[0] == 'DIVINATION':
                                        detalle[2] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'GUARD':
                                        detalle[3] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'VOTE':
                                        detalle[4] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'ATTACK':
                                        detalle[5] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'DIVINED':
                                        detalle[6] = 1
                                        msg_target[int(msg[2]) - 1] = 1
                                        ww = enc.transform([['WEREWOLF']])
                                        if msg[4] != 'HUMAN':
                                            role[int(ww[0][0])] = 1

                                        else:
                                            for i in range(len(role)):
                                                if i != int(ww[0][0]):
                                                    role[i] = 1

                                    elif msg[0] == 'IDENTIFIED':
                                        detalle[7] = 1
                                        msg_target[int(msg[2]) - 1] = 1
                                        ww = enc.transform([['WEREWOLF']])
                                        if msg[4] != 'HUMAN':
                                            role[int(ww[0][0])] = 1

                                        else:
                                            for i in range(len(role)):
                                                if i != int(ww[0][0]):
                                                    role[i] = 1

                                    elif msg[0] == 'GUARDED':
                                        detalle[8] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'VOTED':
                                        detalle[9] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    elif msg[0] == 'ATTACKED':
                                        detalle[10] = 1
                                        msg_target[int(msg[2]) - 1] = 1

                                    else:
                                        detalle[11] = 1

                                    acc_dias.extend(accion)
                                    acc_dias.extend(detalle)
                                    acc_dias.extend(msg_target)
                                    acc_dias.extend(role)
                                    acc_dia.append(acc_dias)
                                #print('Acciones del agente',k1,':', len(acc_dia))
                                day.append([acc_dia, k1])


                            flag = 0
                            for p in day:
                                #print(p[1])
                                game[p[1]-1].extend(p[0])
                                for action in p[0]:
                                    if flag == 0:
                                        mask.append(0)
                                flag = 1
                                #game[p[1]-1].extend(p[0])
                                #print(game[p[1]-1])


                        elif k == 'vote':

                            day = []

                            # clave-id valor-[sucesos]
                            for k1, v1 in dict[key][k].items():
                                vot_dia=[]
                                accion = [0, 0, 0]
                                detalle = [0] * 12
                                msg_target = [0] * num_players
                                role = [0]*num_roles

                                accion[1] = 1
                                msg_target[v1 - 1] = 1

                                vot_dia.extend(accion)
                                vot_dia.extend(detalle)
                                vot_dia.extend(msg_target)
                                vot_dia.extend(role)
                                day.append([vot_dia, k1])

                            #print('Votaciones del dia:', day)

                            flag = 0
                            for p in day:
                                #print(p[1])
                                game[p[1]-1].extend([p[0]])
                                if flag == 0:
                                    mask.append(1)
                                flag = 1
                                #print(game[p[1]-1])

                        elif k == 'dead' and key != len(dict.items())-1:
                            day = []
                            for k1, v1 in dict[key][k].items():
                                acc_dia = []
                                accion = [0, 0, 0]
                                detalle = [0] * 12
                                msg_target = [0] * num_players
                                role = [0]*num_roles
                                accion[0] = 1

                                acc_dia.extend(accion)
                                acc_dia.extend(detalle)
                                acc_dia.extend(msg_target)
                                acc_dia.extend(role)

                                day.append([acc_dia, k1])
                            for p in day:
                                real = []
                                for j in range(actions_day+1):
                                    real.append(p[0])


                                game[p[1]-1].extend(real)
                    in_dia += 1

            if test:

                print("Players:", len(game))
                print("Steps:", len(game[0]))


                print(np.array(target))
                print(np.array(game))
                print(np.array(mask))
                print(dict)

            else:
                dir = 'data/gat2017log15_data/'
                #print('Guardando en: ', dir)
                np.save(dir + name + '.x', np.array(game))
                np.save(dir + name + '.y', np.array(target))
                np.save(dir + name + '.valid', np.array(mask))


    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    test = False

    for i in range(1000):
        for j in range(100):

            if test:
                nombre = ''
                generate_matrix('000.log', nombre, test)
                break

            if len(str(i)) == 1:
                f = '00'+str(i)
            elif len(str(i)) == 2:
                f = '0' + str(i)
            else:
                f = str(i)

            if len(str(j)) == 1:
                g = '00'+str(j)
            elif len(str(j)) == 2:
                g = '0' + str(j)
            else:
                g = str(j)

            ubi_file = 'data/gat2017log15/'+f+'/'+g+'.log'

            #print("Obteniendo matriz a partir del fichero: ", ubi_file, ".....")
            nombre = str(f)+'_'+str(g)
            generate_matrix(ubi_file, nombre, test)

            #print("Matriz ", nombre, " guardada")

        if test:
            break
