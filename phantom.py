from random import randrange, choice
from time import sleep
from ast import literal_eval

def lancer():
    sleep(3)
    fini = False
    old_question = ""
    while not fini:
        infof = open('./1/infos.txt','r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            phantom_color = lines[0].split(':')[-1].strip()
            fini = "Score final" in lines[-1]
        # print(phantom_color)
        qf = open('./1/questions.txt','r')
        question = qf.read()
        qf.close()
        if question != old_question :
            rf = open('./1/reponses.txt','w')
            if ('position' in question.lower()):
                pos_list = question.split(':')[1].strip()[1:].split('}')[0].strip()
                pos_list = [int(i) for i in pos_list.split(',')]
                rf.write(str(choice(pos_list)))
            elif('tuiles' in question.lower()):
                pos_list = question.split(':')[1].strip()[1:].split(']')[0].strip()
                pos_list = pos_list.split(',')
                indices = [i for i, s in enumerate(pos_list) if phantom_color in s.lower()]
                print(indices)
                rf.write(str(indices[0]) if len(indices) > 0 else str(randrange(len(pos_list))))
            else:
                rf.write(str(randrange(6)))
            rf.close()
            old_question = question
