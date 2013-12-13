import easyLeap
import sys
import subprocess

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

def move1(p):
    p['diff_fingers'] = p['fingers']-actor.last_time_fingers
    p['diff_dist_fingers_lr'] = p['dist_fingers_lr']-actor.last_time_dist_fingers_lr
    p['diff_angle_fingers_lr'] = p['angle_fingers_lr']-actor.last_time_angle_fingers_lr
    p['diff_lm_fing_tip_rel_pos_x'] = p['lm_fing_tip_rel_pos_x']-actor.last_time_lm_fing_tip_rel_pos_x
    p['diff_lm_fing_tip_rel_pos_y'] = p['lm_fing_tip_rel_pos_y']-actor.last_time_lm_fing_tip_rel_pos_y
    p['diff_lm_fing_tip_rel_pos_z'] = p['lm_fing_tip_rel_pos_z']-actor.last_time_lm_fing_tip_rel_pos_z
    p['diff_rm_fing_tip_rel_pos_x'] = p['rm_fing_tip_rel_pos_x']-actor.last_time_rm_fing_tip_rel_pos_x
    p['diff_rm_fing_tip_rel_pos_y'] = p['rm_fing_tip_rel_pos_y']-actor.last_time_rm_fing_tip_rel_pos_y
    p['diff_rm_fing_tip_rel_pos_z'] = p['rm_fing_tip_rel_pos_z']-actor.last_time_rm_fing_tip_rel_pos_z

    actor.last_time_fingers = p['fingers']
    actor.last_time_dist_fingers_lr = p['dist_fingers_lr']
    actor.last_time_angle_fingers_lr = p['angle_fingers_lr']
    actor.last_time_lm_fing_tip_rel_pos_x = p['lm_fing_tip_rel_pos_x']
    actor.last_time_lm_fing_tip_rel_pos_y = p['lm_fing_tip_rel_pos_y']
    actor.last_time_lm_fing_tip_rel_pos_z = p['lm_fing_tip_rel_pos_z']
    actor.last_time_rm_fing_tip_rel_pos_x = p['rm_fing_tip_rel_pos_x']
    actor.last_time_rm_fing_tip_rel_pos_y = p['rm_fing_tip_rel_pos_y']
    actor.last_time_rm_fing_tip_rel_pos_z = p['rm_fing_tip_rel_pos_z']
    
    actor.file.write(','.join([ str(int(p[k]*100)) for k in sorted(p.iterkeys())]))
    actor.file.write(',move1\n')

def move2(p):
    p['diff_fingers'] = p['fingers']-actor.last_time_fingers
    p['diff_dist_fingers_lr'] = p['dist_fingers_lr']-actor.last_time_dist_fingers_lr
    p['diff_angle_fingers_lr'] = p['angle_fingers_lr']-actor.last_time_angle_fingers_lr
    p['diff_lm_fing_tip_rel_pos_x'] = p['lm_fing_tip_rel_pos_x']-actor.last_time_lm_fing_tip_rel_pos_x
    p['diff_lm_fing_tip_rel_pos_y'] = p['lm_fing_tip_rel_pos_y']-actor.last_time_lm_fing_tip_rel_pos_y
    p['diff_lm_fing_tip_rel_pos_z'] = p['lm_fing_tip_rel_pos_z']-actor.last_time_lm_fing_tip_rel_pos_z
    p['diff_rm_fing_tip_rel_pos_x'] = p['rm_fing_tip_rel_pos_x']-actor.last_time_rm_fing_tip_rel_pos_x
    p['diff_rm_fing_tip_rel_pos_y'] = p['rm_fing_tip_rel_pos_y']-actor.last_time_rm_fing_tip_rel_pos_y
    p['diff_rm_fing_tip_rel_pos_z'] = p['rm_fing_tip_rel_pos_z']-actor.last_time_rm_fing_tip_rel_pos_z

    actor.last_time_fingers = p['fingers']
    actor.last_time_dist_fingers_lr = p['dist_fingers_lr']
    actor.last_time_angle_fingers_lr = p['angle_fingers_lr']
    actor.last_time_lm_fing_tip_rel_pos_x = p['lm_fing_tip_rel_pos_x']
    actor.last_time_lm_fing_tip_rel_pos_y = p['lm_fing_tip_rel_pos_y']
    actor.last_time_lm_fing_tip_rel_pos_z = p['lm_fing_tip_rel_pos_z']
    actor.last_time_rm_fing_tip_rel_pos_x = p['rm_fing_tip_rel_pos_x']
    actor.last_time_rm_fing_tip_rel_pos_y = p['rm_fing_tip_rel_pos_y']
    actor.last_time_rm_fing_tip_rel_pos_z = p['rm_fing_tip_rel_pos_z']
    actor.file.write(','.join([ str(int(p[k]*100)) for k in sorted(p.iterkeys())]))
    actor.file.write(',move2\n')
def none(p):
    p['diff_fingers'] = p['fingers']-actor.last_time_fingers
    p['diff_dist_fingers_lr'] = p['dist_fingers_lr']-actor.last_time_dist_fingers_lr
    p['diff_angle_fingers_lr'] = p['angle_fingers_lr']-actor.last_time_angle_fingers_lr
    p['diff_lm_fing_tip_rel_pos_x'] = p['lm_fing_tip_rel_pos_x']-actor.last_time_lm_fing_tip_rel_pos_x
    p['diff_lm_fing_tip_rel_pos_y'] = p['lm_fing_tip_rel_pos_y']-actor.last_time_lm_fing_tip_rel_pos_y
    p['diff_lm_fing_tip_rel_pos_z'] = p['lm_fing_tip_rel_pos_z']-actor.last_time_lm_fing_tip_rel_pos_z
    p['diff_rm_fing_tip_rel_pos_x'] = p['rm_fing_tip_rel_pos_x']-actor.last_time_rm_fing_tip_rel_pos_x
    p['diff_rm_fing_tip_rel_pos_y'] = p['rm_fing_tip_rel_pos_y']-actor.last_time_rm_fing_tip_rel_pos_y
    p['diff_rm_fing_tip_rel_pos_z'] = p['rm_fing_tip_rel_pos_z']-actor.last_time_rm_fing_tip_rel_pos_z

    actor.last_time_fingers = p['fingers']
    actor.last_time_dist_fingers_lr = p['dist_fingers_lr']
    actor.last_time_angle_fingers_lr = p['angle_fingers_lr']
    actor.last_time_lm_fing_tip_rel_pos_x = p['lm_fing_tip_rel_pos_x']
    actor.last_time_lm_fing_tip_rel_pos_y = p['lm_fing_tip_rel_pos_y']
    actor.last_time_lm_fing_tip_rel_pos_z = p['lm_fing_tip_rel_pos_z']
    actor.last_time_rm_fing_tip_rel_pos_x = p['rm_fing_tip_rel_pos_x']
    actor.last_time_rm_fing_tip_rel_pos_y = p['rm_fing_tip_rel_pos_y']
    actor.last_time_rm_fing_tip_rel_pos_z = p['rm_fing_tip_rel_pos_z']
    actor.file.write(','.join([ str(int(p[k]*100)) for k in sorted(p.iterkeys())]))
    actor.file.write(',none\n')



f = open("test.csv", 'w')

keys = [ k for k,v in app_parameters['WATCHED_PARAMS_IN_HAND'].items() ]
keys.append('diff_fingers')
keys.append('diff_dist_fingers_lr')
keys.append('diff_angle_fingers_lr')
keys.append('diff_lm_fing_tip_rel_pos_x')
keys.append('diff_lm_fing_tip_rel_pos_y')
keys.append('diff_lm_fing_tip_rel_pos_z')
keys.append('diff_rm_fing_tip_rel_pos_x')
keys.append('diff_rm_fing_tip_rel_pos_y')
keys.append('diff_rm_fing_tip_rel_pos_z')

f.write(','.join([ k+':discrete' for k in sorted(keys)]))
f.write(',cls:nominal:class\n')

    
actor = easyLeap.Actor()
actor.file = f
actor.last_time_fingers = 0
actor.last_time_dist_fingers_lr = 0
actor.last_time_angle_fingers_lr = 0
actor.last_time_lm_fing_tip_rel_pos_x = 0
actor.last_time_lm_fing_tip_rel_pos_y = 0
actor.last_time_lm_fing_tip_rel_pos_z = 0
actor.last_time_rm_fing_tip_rel_pos_x = 0
actor.last_time_rm_fing_tip_rel_pos_y = 0
actor.last_time_rm_fing_tip_rel_pos_z = 0
actor.on_hand = move1


easyLeap.init(app_parameters)
listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
controller = easyLeap.Leap.Controller()  #Get a Leap controller
controller.add_listener(listener)  #Attach the listener

sys.stdin.readline()
actor.on_hand = move2

sys.stdin.readline()

actor.on_hand = none

sys.stdin.readline()

#Remove the sample listener when done
controller.remove_listener(listener)