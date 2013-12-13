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
        'max_dist_fingers':'max_dist_fingers',
        'max_angle_fingers':'max_angle_fingers',
        'fingers_avg_angle':'fingers_avg_angle',
        'fingers_avg_dist':'fingers_avg_dist',
    },
    'WATCHED_PARAMS_IN_CIRCLE' : {
        'center_name':'position_name',
        'clockwiseness':'clockwiseness',
        'state':'state' # 1 : just started, 2 : running, 3 : just finished
    },
    'GESTURE_CIRCLE_MIN_RADIUS' : 15.0,

    'WATCHED_PARAMS_IN_SWIPE' : {
        'direction_name':'direction_name',
        'start_position_name':'start_position_name',
        'current_position_name':'current_position_name',
        'state':'state' # 1 : just started, 2 : running, 3 : just finished
    }
}


def sendKey(key):
    command = 'xvkbd -text "%s"' % key
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print key

def on_hand2(p):
    md = p['max_dist_fingers']
    ma = p['max_angle_fingers']
    f = p['fingers']
    upd = p['upside_down']
    n = p['position_name']
    l='left' in n
    r='right' in n
    t='top' in n
    b='bottom' in n

    keys=['q','s','d','f','g','h','j','k']
    select = -1
    
    if md > 60 and ma < 0.40 and f == 2 :
        if l :
            if b : select = 0
            if t : select = 1
        if r :
            if b : select = 2
            if t : select = 3

    if f==0 and upd :
        if l :
            if b : select = 4
            if t : select = 5
        if r :
            if b : select = 6
            if t : select = 7
        
    if select > -1 and actor.current_cursor != select :
        sendKey(keys[select])
        actor.current_cursor = select

def on_circle2(p):
    s=p['state']
    n=p['center_name']
    c=p['clockwiseness']
    l='left' in n
    r='right' in n
    t='top' in n
    b='bottom' in n

    keys = ['w','x','c','v']
    select = -1
    if s == 3 :
        if c == 'clockwise':
            if l : select = 0
            if r : select = 1
        else :
            if l : select = 2
            if r : select = 3
    if select > -1 :
        sendKey(keys[select])

def on_hand(p):
    md = p['max_dist_fingers']
    ma = p['max_angle_fingers']
    f = p['fingers']
    n = p['position_name']
    h = not 'top' in n and not 'bottom' in n
    v = not 'left' in n and not 'right' in n
    l = 'left' in n and h
    r = 'right' in n and h
    t = 'top' in n and v
    b = 'bottom' in n and v

    keys=['q','s','d','f','g','h','j','k']
    select = -1
    if f == 2 and ma < 0.40 and md > 60 :
        if l : select = 0
        if r : select = 1
        if t : select = 2
        if b : select = 3
        
    if select > -1 and actor.current_cursor != select :
        sendKey(keys[select])
        actor.current_cursor = select
    
actor = easyLeap.Actor()
#actor.on_hand = on_hand
actor.current_cursor = 0
#actor.on_circle = on_circle
#actor.on_swipe = on_swipe


easyLeap.init(app_parameters)
listener = easyLeap.Listener(actor) #Get listener which herits from Leap.Listener
controller = easyLeap.Leap.Controller()  #Get a Leap controller
controller.add_listener(listener)  #Attach the listener

sys.stdin.readline()

#Remove the sample listener when done
controller.remove_listener(listener)