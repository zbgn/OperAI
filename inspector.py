import sys
from random import choice, randrange
from time import sleep

color = ['rose','rouge','gris','bleu','marron','noir','blanc','violet']

def lancer():
    fini = False
    old_question = ""
    first = True
    old_question = ''
    while not fini:
        infof = open('./0/infos.txt', 'r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            # phantom_color = lines[0].split(':')[-1].strip()
            fini = "Score final" in lines[-1] and not first
        first = False
        # print(phantom_color)
        qf = open('./0/questions.txt', 'r')
        question = qf.read()
        qf.close()

        if question != old_question and question != '':
            rf = open('./0/reponses.txt', 'w')
            # Choix des positions (salles)
            if ('{' in question.lower()):
                pos_list = question.split('{')[1].strip().split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                direction = str(pos_list[0])
                rf.write(direction)
            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                # util pour le phantom uniquement
                # indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]
                # rf.write(str(indices[0]) if len(indices) > 0 else str(randrange(len(pos_list))))
                rf.write(str(randrange(len(pos_list))))
            # Parsing pouvoir
            elif ('(' in question.lower()):
                color_choice = None
                pos_list = question.split('(')[1].strip().split(')')[0].strip()
                if ('-' in pos_list):
                    pos_list = pos_list.split('-') # Choix des salles pour les pouvoirs
                elif ('/' in pos_list):
                    pos_list = pos_list.split('/') # Activation du pouvoir
                elif ('pas violet!' in question.lower()):
                    color_choice = str(color[0])
                else:
                    #print('error parsing: \x1B[3m{:}\x1B[23m ; token not found.'.format(question.lower()), file=sys.stderr)
                    pos_list = [0, 1]
                rf.write(str(randrange(int(pos_list[0]), int(pos_list[1])))) if not color_choice else rf.write(color_choice)
            else:
                rf.write(str(randrange(6)))
            rf.close()
            old_question = question

