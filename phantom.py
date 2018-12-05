import sys
from random import choice, randrange
from time import sleep
from collections import namedtuple

color = ['rose','rouge','gris','bleu','marron','noir','blanc','violet']

status = {
    'suspect' : 0,
    'clean' : 1
}

#Passages entre salles
debug = False
salles = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}

#passages = [{1,4},{0,2},{1,3},{2,7},{0,5,8},{4,6},{5,7},{3,6,9},{4,9},{7,8}]
passages = [[1,4],[0,2],[1,3],[2,7],[0,5],[0,8],[5,8],[3,6],[6,9],[3,9],[4,6],[5,7],[4,9],[7,8]]
pass_ext = [{1,4},{0,2,5,7},{1,3,6},{2,7},{0,5,8,9},{4,6,1,8},{5,7,2,9},{3,6,9,1},{4,9,5},{7,8,4,6}]

passagesbis = [[1,4],[0,2],[1,3],[2,7],[0,5,8],[4,6],[5,7],[3,6,9],[4,9],[7,8]]


def who_is_the_best(post_list):
    scores = []
    for pos in post_list:
        perso = pos.split('-')
        rooms = get_all_rooms_can_go(perso)
        scores.append(get_score_per_room(rooms))
    bestscore = scores[0][0]
    result = post_list[0].split('-')
    result[1] = str(bestscore[0])
    for index, scores_perso in enumerate(scores):
        for score_room in scores_perso
            if score_room[1] > bestscore[1]:
                bestscore = score_room
                result = post_list[index].split('-')
                result[1] = str(bestscore[0])
    #print(result)
    return '-'.join(result)


def get_all_rooms_can_go(perso):
    moves = len(salles[int(perso[1])])
    rooms = [int(perso[1])]
    rooms = find_all_rooms(moves, rooms)
    return [x for x in rooms if x != int(perso[1])]


def get_score_per_room(rooms):
    result = []
    for room in rooms:
        result.append([room, len(salles[room])])
    return result


def find_all_rooms(moves,rooms):
    moves = moves -1
    list_rooms = []
    list_rooms.extend(rooms)
    for room in list_rooms:
        rooms.extend(passagesbis[room])
    if moves < 1:
        if len(rooms ) > 0:
         rooms = set(rooms)
        return rooms
    find_all_rooms(moves,rooms)
    rooms = set(rooms)
    return rooms


#
# Groupe suspect par groupe de deux minimum
#


def update_room(direction, character):
    c = None
    #print(salles, direction, character)
    for key, value in salles.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                c = v
                del value[i]
    if c is not None:
        salles[direction].append(c)
   # print(salles, direction, character)

def send_response(rf, msg):
    msg = str(msg)
    if debug:
        print (msg)
    rf.write(msg)

def lancer():
    fini = False
    old_question = ''
    first = True
    choosen_char = ''
    while not fini:
        infof = open('./1/infos.txt', 'r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            #Parsing des personnages
            if first:
                for personnage in [item.strip() for item in lines[3].split()]:
                    pos_col, pos_salle, pos_status = personnage.split('-')
                    salles[int(pos_salle)].append({'color':pos_col, 'status':pos_status})
                # phantom_color = lines[0].split(':')[-1].strip()
            fini = "Score final" in lines[-1] and not first
        first = False
        #print(phantom_color)
        #print(phantom_power)
        qf = open('./1/questions.txt', 'r')
        question = qf.read()
        qf.close()

        if question != old_question and question != '':
            if debug:
                print (question)

            rf = open('./1/reponses.txt', 'w')

            # Choix des positions (salles)
            if ('{' in question.lower()):
                #on choisit une positon               
                pos_list = question.split('{')[1].strip().split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                
                direction = choice(pos_list)
                update_room(direction, choosen_char)
                send_response(rf, direction)

            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                # on rempli les salles
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                # indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]

                result = who_is_the_best(pos_list)
                #print(result)
                choosen_room = 0
                choosen_char = pos_list[choosen_room].split('-')[0] #get color of choose

                send_response(rf, choosen_room)
                
            # Parsing pouvoir
            elif ('(' in question.lower()):
                color_choice=None
                pos_list = question.split('(')[1].strip().split(')')[0].strip()
                if ('-' in pos_list):
                    pos_list = pos_list.split('-') # Choix des salles pour les pouvoirs
                elif ('/' in pos_list):
                    pos_list = pos_list.split('/') # Activation du pouvoir
                elif ('pas violet!' in question.lower()):
                    color_choice=choice(color[:-1])
                else:
                    #print('error parsing: \x1B[3m{:}\x1B[23m ; token not found.'.format(question.lower()), file=sys.stderr)
                    pos_list = [0, 1]
                
                #print("pouvoir")
                send_response(rf, randrange(int(pos_list[0]), int(pos_list[1]))) if not color_choice else send_response(rf, color_choice)
            else:
                send_response(rf, randrange(6))
            rf.close()
            old_question = question
