import sys
from random import choice, randrange
from time import sleep
from collections import namedtuple

color = ['rose','rouge','gris','bleu','marron','noir','blanc','violet']

#Pouvoir suivant la couleur
color_power = {
    'rose' : 'permanents',
    'rouge' : 'deux',
    'gris' : 'deux',
    'bleu' : 'deux',
    'violet': 'avant',
    'marron' : 'avant',
    'noir' : 'apres',
    'blanc' : 'apres'
}

status = {
    'suspect' : 0,
    'clean' : 1
}

#Passages entre salles
debug = True
salles = [[],[],[],[],[],[],[],[],[],[]]

#passages = [{1,4},{0,2},{1,3},{2,7},{0,5,8},{4,6},{5,7},{3,6,9},{4,9},{7,8}]
passages = [[1,4],[0,2],[1,3],[2,7],[0,5],[0,8],[5,8],[3,6],[6,9],[3,9],[4,6],[5,7],[4,9],[7,8]]
pass_ext = [{1,4},{0,2,5,7},{1,3,6},{2,7},{0,5,8,9},{4,6,1,8},{5,7,2,9},{3,6,9,1},{4,9,5},{7,8,4,6}]

Personnage = namedtuple("personnage", "color power salle status indice")

#
# Groupe suspect par groupe de deux minimum
#
def get_fullest(rooms):
    fullest = 0
    current = 0
    for room in rooms:
        size = len(room)
        if size > fullest:
            fullest = current
        current += 1
    return rooms[fullest][0].indice

def get_closest(rooms):
    # check si on peux faire un groupe de deux suspects
    positions = []
    indices = []
    for room in rooms:
        #check si personnage est tout seul et suspect
        if len(room) == 1 and room[0].status == 'suspect':
            positions.append(room[0].salle)
            indices.append(room[0].indice)
    #check si on a des personnages tout seul et supect
    if len(positions) > 1:
        print(positions)
        #pour chaque passage
        for passage in passages:
            #check si on peux faire communiquer deux de ces personnes
            if passage[0] in positions and passage[1] in positions:
                return 0
    return 0
    #Sinon pour chaque personne dans la piece si il y a encore des suspects
    for personnage in room:
        if personnage.status == 'suspect':
            print ("suspect")
    return 0

def get_emptiest(rooms):
    emptiest = sys.maxsize
    current = 0
    for room in rooms:
        size = len(room)
        if 0 < size < emptiest:
            emptiest = current
        current += 1
    return rooms[emptiest][0].indice

def send_response(rf, msg):
    msg = str(msg)
    if debug:
        print (msg)
    rf.write(msg)

def lancer():
    fini = False
    old_question = ""
    first = True
    while not fini:
        infof = open('./1/infos.txt', 'r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            #Parsing des personnages
            if first:
                personnages = [item.strip() for item in lines[3].split('  ')]
                for personnage in personnages:
                    pos_col, pos_salle, pos_status = personnage.split('-')
                    pos_salle = int(pos_salle)
                    pos_power = color_power[pos_col]
                    perso = Personnage(color=pos_col, power=pos_power, salle=pos_salle, status=pos_status, indice=0)
                    salles[pos_salle].append(personnage)
                phantom_color = lines[0].split(':')[-1].strip()
                #error here
                phantom_power = color_power[phantom_color]
            fini = "Score final" in lines[-1] and not first
        first = False
        #print(phantom_color)
        #pintt(phantom_power)
        qf = open('./1/questions.txt', 'r')
        question = qf.read()
        qf.close()

        if question != old_question and question != "":
            if debug:
                print (question)

            rf = open('./1/reponses.txt', 'w')

            # Choix des positions (salles)
            if ('{' in question.lower()):
                #on choisit une possiton               
                pos_list = question.split('{')[1].strip().split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                
                send_response(rf, choice(pos_list))

            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                # on rempli les salles
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]
                
                indice = 0
                new_salles = [[],[],[],[],[],[],[],[],[],[]]
                for pos in pos_list:
                    pos_col, pos_salle, pos_status = pos.strip().split('-')
                    pos_salle = int(pos_salle)
                    pos_power = color_power[pos_col]
                    personnage = Personnage(color=pos_col, power=pos_power, salle=pos_salle, status=pos_status, indice=indice)
                    new_salles[pos_salle].append(personnage)
                    indice += 1
                
                chosen_room = 0
                #chosen_room = get_fullest(salles)
                #chosen_room = get_emptiest(salles)
                #chosen_room = get_closest(salles)
                send_response(rf, chosen_room)
                
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
                    print('error parsing: \x1B[3m{:}\x1B[23m ; token not found.'.format(question.lower()), file=sys.stderr)
                    pos_list = [0, 1]
                
                #print("pouvoir")
                send_response(rf, randrange(int(pos_list[0]), int(pos_list[1]))) if not color_choice else send_response(rf, color_choice)
            else:
                send_response(rf, randrange(6))
            rf.close()
            old_question = question
