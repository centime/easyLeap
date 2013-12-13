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
        'dist_fingers_lr':'dist_fingers_lr',
        'angle_fingers_lr':'angle_fingers_lr',
        'fingers_avg_angle':'fingers_avg_angle',
        'fingers_avg_dist':'fingers_avg_dist',
        'lm_fing_tip_rel_pos_x':'lm_fing_tip_rel_pos_x',
        'lm_fing_tip_rel_pos_y':'lm_fing_tip_rel_pos_y',
        'lm_fing_tip_rel_pos_z':'lm_fing_tip_rel_pos_z',
        'rm_fing_tip_rel_pos_x':'rm_fing_tip_rel_pos_x',
        'rm_fing_tip_rel_pos_y':'rm_fing_tip_rel_pos_y',
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
    if actor.collected_samples < actor.training_set_size :    
        actor.training_csv.write(','.join([ str(int(p[k]*100)) for k in sorted(p.iterkeys())]))
        actor.training_csv.write(',%s\n'%cname)
    elif actor.collected_samples < actor.training_set_size + actor.test_set_size:
        actor.test_csv.write(','.join([ str(int(p[k]*100)) for k in sorted(p.iterkeys())]))
        actor.test_csv.write(',%s\n'%cname)
    elif actor.current_class < (len(actor.classes)-1) : 
        print 'next : '+actor.classes[actor.current_class+1]
        actor.collected_samples = 0
        actor.current_class += 1
        if actor.current_class == 2 :
            actor.training_set_size = actor.training_none_size
            print actor.training_set_size
        actor.on_hand = lambda p: save_class(p,actor.classes[actor.current_class])
    else :
        actor.on_hand = actor.done
    actor.collected_samples += 1

def done(p):
    print 'done'
    actor.on_hand = ignore

def ignore(p):
    pass

if argv[1] == 'collect':
    classes = ['move1','move2', 'none']
        
    actor = easyLeap.Actor()
    actor.current_class = 0
    actor.classes = classes
    actor.training_csv = new_csv(argv[2]+'.csv')
    actor.test_csv = new_csv(argv[2]+'-test.csv')
    actor.training_set_size = int(int(argv[3])*2/3)
    actor.training_none_size = int(argv[3])*2
    actor.test_set_size = int(int(argv[3])*1/3)
    actor.collected_samples = 0
    actor.done = done
    actor.on_hand = lambda p: save_class(p,actor.classes[0])


    easyLeap.init(app_parameters)
    listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
    controller = easyLeap.Leap.Controller()  #Get a Leap controller
    controller.add_listener(listener)  #Attach the listener

    sys.stdin.readline()
    #Remove the sample listener when done
    actor.training_csv.close()
    actor.test_csv.close()
    print 'calculating accuracy...'
    tree = Tree.build(Data(argv[2]+'.csv'))
    tree.set_missing_value_policy('use_nearest')
    import pickle

    with open(argv[2]+'.pkl', 'wb') as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)

    print tree.test(Data(argv[2]+'-test.csv')).mean
    controller.remove_listener(listener)

elif argv[1] == 'test':
    try :
        tree = pickle.load(open(argv[2]+'.pkl', 'rb'))
    except :
        tree = Tree.build(Data(argv[2]+'.csv'))
    tree.set_missing_value_policy('use_nearest')
    print tree.test(Data(argv[2]+'-test.csv')).mean

