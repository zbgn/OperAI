import sys
from random import choice, randrange


#passages = [{1,4},{0,2},{1,3},{2,7},{0,5,8},{4,6},{5,7},{3,6,9},{4,9},{7,8}]
salles = {0: [{'color': 'bleu', 'status': 'suspect'}, {'color': 'marron', 'status': 'clean'}], 1: [{'color': 'violet', 'status': 'suspect'}, {'color': 'noir', 'status': 'suspect'}], 2: [{'color': 'rose', 'status': 'suspect'}, {'color': 'rouge', 'status': 'clean'}], 3: [{'color': 'gris', 'status': 'clean'}], 4: [{'color': 'blanc', 'status': 'clean'}], 5: [], 6: [], 7: [], 8: [], 9: []}

color = ['rose', 'rouge', 'gris', 'bleu', 'marron', 'noir', 'blanc', 'violet']

#Debug
debug = False  #if not environ.get('DEBUG') else True
def dprint(*args, sep=' ', **kwargs):
    if debug:
        print(sep.join(map(str, args)), *print*kwargs)

# Mapping
character = None
direction = -1

#Passages entre salles
passages = [[1,4],[0,2],[1,3],[2,7],[0,5,8],[4,6],[5,7],[3,6,9],[4,9],[7,8]]
pass_ext = [{1,4},{0,2,5,7},{1,3,6},{2,7},{0,5,8,9},{4,6,1,8},{5,7,2,9},{3,6,9,1},{4,9,5},{7,8,4,6}]

def who_is_the_best(post_list):
    scores = []
    dprint(salles)
    for pos in post_list:
        perso = pos.split('-')
        rooms = get_all_rooms_can_go(perso)
        scores.append(get_score_per_room(perso,rooms))
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

def if_phantom_manifest(salles_tmp):
    try:
        for key, value in salles_tmp.items():
            for i, v in enumerate(value):
                if v['color'] == fantome:
                    room = key
        if len(salles_tmp[room]) > 1 and int(room) != ombre:
            return False
        else:
            return True
    except:
        return False

def how_many_suspect(salles_tmp):
    suspects = 0
    manifest = if_phantom_manifest(salles_tmp)
    if manifest:
        suspects = suspects + 1
        for key, value in salles_tmp.items():
            room = key
            if len(value) == 1 or key == ombre:
                for i, v in enumerate(value):
                    if v['status'] == 'suspect':
                        suspects = suspects + 1
    else:
        for key, value in salles_tmp.items():
            room = key
            if len(value) < 1 or key != ombre:
                for i, v in enumerate(value):
                    if v['status'] == 'suspect':
                        suspects = suspects + 1
    return suspects




def get_all_rooms_can_go(perso):
    moves = 1
    rooms = []
    rooms.extend(passages[int(perso[1])])
    if 'rose' in perso[0]:
        rooms.extend(pass_ext[int(perso[1])])
    rooms = set(rooms)
    try:
        if int(perso[1]) == bloquer[0]:
            rooms = [x for x in rooms if x != bloquer[1]]
        if int(perso[1]) == bloquer[1]:
            rooms = [x for x in rooms if x != bloquer[0]]
    except:
        dprint('error')
    return rooms


def get_score_per_room(perso ,rooms):
    result = []
    score = 0

    try:
        if perso[0] == fantome and subtour < 4:
             score = score + 2
    except:
        print('error')
    if perso[2] == 'clean':
        score = score - 10

    for room in rooms:
        salles_tmp = get_salles_tmp(room,perso[0].replace(' ', ''))

        result.append([room, (how_many_suspect(salles_tmp) + score)])
    return result


def find_all_rooms(moves, rooms):
    moves = moves - 1
    list_rooms = []
    list_rooms.extend(rooms)
    for room in list_rooms:
        rooms.extend(passages[room])
    if moves > 0:
            rooms = find_all_rooms(moves, rooms)
    rooms = set(rooms)
    return rooms


#
# Groupe suspect par groupe de deux minimum
#

def update_status(status, character):
    for key, value in salles.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                value[i]['status'] = status

def update_room(direction, character):
    c = None
    for key, value in salles.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                c = v
                del value[i]
    if c is not None:
        salles[direction].append(c)

def get_salles_tmp(direction, character):
    c = None
    salles_tmpp = salles
    for key, value in salles_tmpp.items():
        _ = key
        for i, v in enumerate(value):
            if v['color'] == character:
                c = v
                del value[i]
    if c is not None:
        salles_tmpp[direction].append(c)
    return salles_tmpp


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
    global iline
    global bloquer
    global ombre
    global tour
    global subtour
    global fantome

    tour = 0
    ombre = 0
    subtour = 0
    bloquer = []
    old_len_lines = 0
    best =''
    fini = False
    first = True
    old_question = ''
    choosen_char = ''
    iline = 0
    while not fini:
        infof = open('./1/infos.txt', 'r')
        lines = infof.readlines()
        infof.close()

        # get new lines #########################
        iline = len(lines)
        if old_len_lines != iline:
            for x in range(old_len_lines,iline):
                if '!! Le fantôme est :' in lines[x]:
                    fantome = lines[x].split(' : ')[1].replace('\n','')
                if 'Tour de' in lines[x]:
                    subtour = subtour + 1
                if 'Tour:' in lines[x]:
                    tour = tour + 1
                    subtour = 0
                    bloquer = []
                    bloquer_s = lines[x].split(' Bloque:')[1].replace('{','').replace('}','').replace('\n','').split(",")
                    ombre  =int(lines[x].split(',')[2].split(':')[1])
                    for item in bloquer_s:
                        bloquer.append(int(item))

                    init = lines[x + 1].split('  ')
                    for item in init:
                        perso = item.split('-')
                        character = perso[0].replace(' ', '')
                        direction = int(perso[1])
                        status = perso[2].replace('\n','')
                        update_room(direction,character)
                        update_status(status,character)
                if 'NOUVEAU PLACEMENT ' in lines[x]:
                    perso = lines[x].split(':')[1].strip().split('-')
                    character = perso[0].replace(' ','')
                    direction = int(perso[1])
                    update_room(direction,character)
            old_len_lines = len(lines)
         ########################################

        if len(lines) > 0:
            #Parsing des personnages
            if first:
                for personnage in [item.strip() for item in lines[3].split()]:
                    pos_col, pos_salle, pos_status = personnage.split('-')
                    salles[int(pos_salle)].append({'color':pos_col, 'status':pos_status})
                # phantom_color = lines[0].split(':')[-1].strip()
            fini = "Score final" in lines[-1] and not first
            #while not done::
            #if 'REPONSE INTERPRETEE' in lines[-1]:
                #update_room_other(lines[-4:])
        first = False
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
                if len(best.split('-')) > 2 and int(best.split('-')[1]) in pos_list:
                    direction = int(best.split('-')[1])
                else:
                    direction = choice(pos_list)
                send_response(rf, direction)
            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                # indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]
                best = who_is_the_best(pos_list)
                choosen_room = 0
                a = 0
                choosen_char = pos_list[choosen_room].split('-')[0] #get color of choose
                for item in pos_list:
                    if best.split('-')[0] in item:
                        a = pos_list.index(item)
                send_response(rf, a)
                
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
                send_response(rf, "0")
            else:
                send_response(rf, randrange(6))
            rf.close()
            old_question = question
    f = open('./1/infos.txt', 'w').close()

