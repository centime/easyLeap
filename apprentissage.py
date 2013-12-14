import easyLeap
import sys
import subprocess
from sys import argv
from dtree import Tree, Data
import pickle

app_parameters = {

    #'ENABLE_HANDS': False ,
    'ENABLE_GESTURE_SWIPE' : False,
    'ENABLE_GESTURE_CIRCLE' : False,
    'ENABLE_GESTURE_SCREEN_TAP' : False,
    'ENABLE_GESTURE_KEY_TAP' : False,

    'WATCHED_PARAMS_IN_HAND' : {

        'fingers':'fingers.__len__()',
        'angle_fingers_lr':'angle_fingers_lr',
        'fingers_avg_angle':'fingers_avg_angle',
        'lm_fing_tip_rel_pos_y':'lm_fing_tip_rel_pos_y',
        'lm_fing_tip_rel_pos_z':'lm_fing_tip_rel_pos_z',
        'rm_fing_tip_rel_pos_z':'rm_fing_tip_rel_pos_z',
    },
}
def new_csv(fname):
    f = open(fname, 'w')
    keys = [ k for k,v in app_parameters['WATCHED_PARAMS_IN_HAND'].items() ]

    f.write(','.join([ k+':discrete' for k in sorted(keys)]))
    f.write(',cls:nominal:class\n')
    return f

def save_class(p,cname):
    if not actor.training_done :
        nb_sambles = actor.training_set_size
        if actor.is_current_none :
            nb_sambles = actor.none_set_size
        f = actor.training_csv
    else :
        nb_sambles = actor.test_set_size
        f = actor.test_csv
    if actor.collected_samples < nb_sambles :
        data = ','.join([ str(actor.normalize(k,p[k])) for k in sorted(p.iterkeys())])
        f.write(data)
        f.write(',%s\n'%cname)
    elif actor.current_class < (len(actor.classes)-1) : 
        print 'Sampling for '+actor.classes[actor.current_class]+' : done.'
        print 'Next : '+actor.classes[actor.current_class+1]
        print 'press enter to continue..'
        actor.collected_samples = 0
        actor.current_class += 1
        actor.is_current_none = actor.classes[actor.current_class] == 'none'
            
        actor.on_hand = actor.ignore
    else :
        if not actor.training_done :
            actor.collected_samples = 0
            actor.current_class = 0
            actor.training_done = True
            actor.on_hand = ignore
            print 'Starting tests'
            print 'press enter to start with %s' %actor.classes[0]
        else :
            actor.on_hand = actor.done
    actor.collected_samples += 1


def normalize(k,v):
    m = min_max[k]['min']
    M = min_max[k]['max']
    i_range = M-m
    aligned_value = v - m
    norm_value = int(aligned_value * 100 / i_range)
    return norm_value

def done(p):
    print 'Sampling done.'
    print 'press enter..'
    actor.on_hand = ignore

def ignore(p):
    pass

def watch(p):
    d={ k:normalize(k,v) for k,v in p.items()}    
    p=actor.tree.predict(d)
    if not p.best == 'none':
        if not p.best_prob == 1.0 :
            print '\t\t\t\t\t\t\trefused : %s, %s' %(p.best,p.probs)
    if p.best == 'move1':
        print "\t%s" %p.best
    if p.best == 'move2':
        print "\t\t%s" %p.best
    if p.best == 'move3':
        print "\t\t\t%s" %p.best
    if p.best == 'move4':
        print "\t\t\t\t%s" %p.best
    if p.best == 'move5':
        print "\t\t\t\t\t%s" %p.best

def record(p):
    for k,v in p.items():
        if v < actor.min_max[k]['min'] : actor.min_max[k]['min'] = v
        if v > actor.min_max[k]['max'] : actor.min_max[k]['max'] = v

def fuu(p):
    print p

if argv[1] == 'collect':

    with open('setup.csv', 'r') as i:
        mm = i.read()
        min_max = eval(mm)

    classes = ['move1','move2', 'move3', 'move4', 'move5', 'none']
        
    actor = easyLeap.Actor()
    actor.current_class = 0
    actor.min_max = min_max
    actor.normalize = normalize
    actor.classes = classes
    actor.training_csv = new_csv(argv[2]+'.csv')
    actor.test_csv = new_csv(argv[2]+'-test.csv')
    actor.training_set_size = int(argv[3])
    actor.none_set_size = int(argv[3])*2
    actor.test_set_size = 200 #int(int(argv[3])*1/4)
    actor.collected_samples = 0
    actor.done = done
    actor.ignore = ignore
    actor.training_done = False
    actor.is_current_none = False

    actor.on_hand = ignore


    easyLeap.init(app_parameters)
    listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
    controller = easyLeap.Leap.Controller()  #Get a Leap controller
    controller.add_listener(listener)  #Attach the listener

    print
    print 'We will learn %s' %repr(actor.classes)
    print 'press enter to start with %s' %actor.classes[0]
    for i in range(len(actor.classes)*2) : 
        sys.stdin.readline()
        actor.on_hand = lambda p: save_class(p,actor.classes[actor.current_class])

    sys.stdin.readline()

    print 'building the decision tree..'
    actor.training_csv.close()
    actor.test_csv.close()
    tree = Tree.build(Data(argv[2]+'.csv'))
    tree.set_missing_value_policy('use_nearest')

    tree.watched_params = app_parameters['WATCHED_PARAMS_IN_HAND']

    with open(argv[2]+'.pkl', 'w') as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)

    print 'calculating accuracy...'
    print tree.test(Data(argv[2]+'-test.csv')).mean
    controller.remove_listener(listener)

elif argv[1] == 'build':

    f = open(argv[2]+'.pkl', 'rb')
    tree = pickle.load(f)
    f.close()
    app_parameters['WATCHED_PARAMS_IN_HAND'] = tree.watched_params
    tree = Tree.build(Data(argv[2]+'.csv'))

    tree.set_missing_value_policy('use_nearest')
    tree.watched_params = app_parameters['WATCHED_PARAMS_IN_HAND']
    with open(argv[2]+'.pkl', 'w') as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)

    print tree.test(Data(argv[2]+'-test.csv')).mean

elif argv[1] == 'setup':
    actor = easyLeap.Actor()
    actor.min_max = {k:{'min':0,'max':0} for k in app_parameters['WATCHED_PARAMS_IN_HAND'].iterkeys()}
    actor.on_hand = record

    easyLeap.init(app_parameters)
    listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
    controller = easyLeap.Leap.Controller()  #Get a Leap controller
    controller.add_listener(listener)  #Attach the listener
    sys.stdin.readline()

    with open('setup.csv', 'w') as output:
        output.write(repr(actor.min_max))

    controller.remove_listener(listener)    


elif argv[1] == 'run':
    try :
        f = open(argv[2]+'.pkl', 'rb')
        tree = pickle.load(f)
        f.close()
        app_parameters['WATCHED_PARAMS_IN_HAND'] = tree.watched_params
        print 'watched parameters:'
        for k in sorted([j for j in tree.watched_params.iterkeys()]):
            print '\t'+k 
    except :
        tree = Tree.build(Data(argv[2]+'.csv'))

    with open('setup.csv', 'r') as i:
        mm = i.read()
        min_max = eval(mm)

    tree.set_missing_value_policy('use_nearest')

    actor = easyLeap.Actor()
    actor.tree = tree
    actor.min_max = min_max
    actor.normalize = normalize
    actor.on_hand = watch


    easyLeap.init(app_parameters)
    listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
    controller = easyLeap.Leap.Controller()  #Get a Leap controller
    controller.add_listener(listener)  #Attach the listener

    sys.stdin.readline()

    #Remove the sample listener when done
    controller.remove_listener(listener)

elif argv[1] == 'see':
    actor = easyLeap.Actor()
    actor.on_hand = fuu


    easyLeap.init(app_parameters)
    listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
    controller = easyLeap.Leap.Controller()  #Get a Leap controller
    controller.add_listener(listener)  #Attach the listener

    sys.stdin.readline()

    #Remove the sample listener when done
    controller.remove_listener(listener)

