import sys
from random import choice, randrange
from time import sleep


def lancer():
    fini = False
    old_question = ""
    first = True
    while not fini:
        infof = open('./1/infos.txt', 'r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            phantom_color = lines[0].split(':')[-1].strip()
            fini = "Score final" in lines[-1] and not first
        first = False
        # print(phantom_color)
        qf = open('./1/questions.txt', 'r')
        question = qf.read()
        qf.close()
        if question != old_question:
            rf = open('./1/reponses.txt', 'w')
            # Choix des positions (salles)
            if ('{' in question.lower()):
                pos_list = question.split('{')[1].strip().split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                rf.write(str(choice(pos_list)))
            # Choix de la tuile (personnage)
            elif('[' in question.lower()):
                pos_list = question.split('[')[1].strip().split(']')[0].strip()
                pos_list = pos_list.split(',')
                indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]
                rf.write(str(indices[0]) if len(indices) > 0 else str(randrange(len(pos_list))))
            # Parsing pouvoir
            elif ('(' in question.lower()):
                pos_list = question.split('(')[1].strip().split(')')[0].strip()
                if ('-' in pos_list):
                    pos_list = pos_list.split('-') # Choix des salles pour les pouvoirs
                elif ('/' in pos_list):
                    pos_list = pos_list.split('/') # Activation du pouvoir
                else:
                    print('error parsing: \x1B[3m{:}\x1B[23m ; token not found.'.format(question.lower()), file=sys.stderr)
                    pos_list = [0, 1]
                rf.write(str(randrange(int(pos_list[0]), int(pos_list[1]))))
            else:
                rf.write(str(randrange(6)))
            rf.close()
            old_question = question
