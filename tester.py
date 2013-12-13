import easyLeap
import sys
import subprocess
from sys import argv
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
        'lm_fing_tip_rel_pos_x':'lm_fing_tip_rel_pos_x',
        'lm_fing_tip_rel_pos_y':'lm_fing_tip_rel_pos_y',
        'lm_fing_tip_rel_pos_z':'lm_fing_tip_rel_pos_z',
        'rm_fing_tip_rel_pos_x':'rm_fing_tip_rel_pos_x',
        'rm_fing_tip_rel_pos_y':'rm_fing_tip_rel_pos_y',
        'rm_fing_tip_rel_pos_z':'rm_fing_tip_rel_pos_z',
    },
}

def on_hand(p):
    d={ k:int(v*100) for k,v in p.items()}
    try :
        p=actor.tree.predict(d)
        print "%s\t%s" %(p.best, p.best_prob)
        #'best', 'best_prob', 'clear', 'copy', 'count', 'counts', 'keys', 'probs', 'total',
        #print dir(p)
    except:
        print '??'

tree = pickle.load(open(argv[1]+'.pkl', 'rb'))

actor = easyLeap.Actor()
actor.tree = tree
actor.on_hand = on_hand


easyLeap.init(app_parameters)
listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
controller = easyLeap.Leap.Controller()  #Get a Leap controller
controller.add_listener(listener)  #Attach the listener

sys.stdin.readline()

#Remove the sample listener when done
controller.remove_listener(listener)