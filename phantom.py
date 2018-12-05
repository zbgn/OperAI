import sys
from os import environ
from random import choice, randrange


#passages = [{1,4},{0,2},{1,3},{2,7},{0,5,8},{4,6},{5,7},{3,6,9},{4,9},{7,8}]
salles = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
color = ['rose', 'rouge', 'gris', 'bleu', 'marron', 'noir', 'blanc', 'violet']

#Debug
debug = False #if not environ.get('DEBUG') else True
def dprint(*args, sep=' ', **kwargs):
    if debug:
        print(sep.join(map(str, args)), **kwargs)

# Mapping
character = None
direction = -1

#Passages entre salles
passages = [[1,4],[0,2],[1,3],[2,7],[0,5,8],[4,6],[5,7],[3,6,9],[4,9],[7,8]]
pass_ext = [{1,4},{0,2,5,7},{1,3,6},{2,7},{0,5,8,9},{4,6,1,8},{5,7,2,9},{3,6,9,1},{4,9,5},{7,8,4,6}]


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
        for score_room in scores_perso:
            if score_room[1] > bestscore[1]:
                bestscore = score_room
                result = post_list[index].split('-')
                result[1] = str(bestscore[0])
    dprint(result)
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


def find_all_rooms(moves, rooms):
    moves = moves - 1
    list_rooms = []
    list_rooms.extend(rooms)
    for room in list_rooms:
        rooms.extend(passages[room])
    if moves < 1:
        if len(rooms) > 0:
            rooms = set(rooms)
            return rooms
    find_all_rooms(moves, rooms)
    rooms = set(rooms)
    return rooms


#
# Groupe suspect par groupe de deux minimum
#

def update_status(status, character):
    dprint(salles, direction, character)
    for key, value in salles.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                value[i]['status'] = status

def update_room(direction, character):
    c = None
    dprint(salles, direction, character)
    for key, value in salles.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                c = v
                del value[i]
    if c is not None:
        salles[direction].append(c)
    dprint(salles, direction, character)

def update_room_other(new_lines):
    global character
    global direction
    try:
        for line in new_lines:
            if 'tuiles' in line.lower():
                character = new_lines[-1].split(':')[1].strip().split('-')[0]
            if 'position' in line.lower():
                direction = int(new_lines[-1].split(':')[1].strip())
        if character and direction != -1:
            update_room(direction, character, )
            character = None
            direction = -1
    except (ValueError, IndexError) as e:
        dprint('Error:', e, file=sys.stderr)
        pass
                

def send_response(rf, msg):
    msg = str(msg)
    dprint (msg)
    rf.write(msg)

def lancer():
    fini = False
    first = True
    old_question = ''
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
            #while not done:
            if 'REPONSE INTERPRETEE' in lines[-1]:
                update_room_other(lines[-4:])
        first = False
        # dprint(phantom_color)
        # dprint(phantom_power)
        qf = open('./1/questions.txt', 'r')
        question = qf.read()
        qf.close()

        if question != old_question and question != '':
            dprint(question)

            rf = open('./1/reponses.txt', 'w')

            # Choix des positions (salles)
            if ('{' in question.lower()):
                pos_list = question.split('{')[1].strip().split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                
                direction = choice(pos_list)
                update_room(direction, choosen_char)
                send_response(rf, direction)

            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                # indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]

                result = who_is_the_best(pos_list)
                dprint(result)
                choosen_room = 0
                choosen_char = pos_list[choosen_room].split('-')[0] #get color of choose
                
                send_response(rf, choosen_room)
                
            # Parsing pouvoir
            elif ('(' in question.lower()):
                color_choice = None
                pos_list = question.split('(')[1].strip().split(')')[0].strip()
                dprint (pos_list)
                if ('-' in pos_list):
                    pos_list = pos_list.split('-') #Choix des salles pour les pouvoirs
                elif ('/' in pos_list):
                    pos_list = pos_list.split('/') #Activation du pouvoir
                elif ('pas violet!' in question.lower()):
                    color_choice = choice(color[:-1])
                else:
                    dprint('error parsing: \x1B[3m{:}\x1B[23m ; token not found.'.format(question.lower()), file=sys.stderr)
                    pos_list = [0, 1]

                dprint("pouvoir")
                #send_response(rf, "1")
                send_response(rf, int(pos_list[1])) if not color_choice else send_response(rf, color_choice)
                #send_response(rf, randrange(int(pos_list[0]), int(pos_list[1]))) if not color_choice else send_response(rf, color_choice)
            else:
                send_response(rf, randrange(6))
            rf.close()
            old_question = question
