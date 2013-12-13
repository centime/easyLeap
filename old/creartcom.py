import easyLeap
import sys
import OscSend

OSC_SERVER = "localhost"
OSC_PORT = 2345
OSC_ROOT = "/"

app_parameters = {

    'WATCHED_PARAMS_IN_HAND' : {
        'hand/fingers':'fingers.__len__() ',
        'hand/position/x':'palm_position.x',
        'hand/position/y':'palm_position.y',
        'hand/position/z':'palm_position.z',
        'hand/velocity/x':'palm_velocity.x',
        'hand/velocity/y':'palm_velocity.y',
        'hand/velocity/z':'palm_velocity.z',
        'hand/openess':'sphere_radius',
        'hand/openess2':'openess2',
        'hand/upside_down':'upside_down',
        'hand/move1':'move1',
        'hand/move2':'move2',
        'hand/roll':'roll',
        'hand/pitch':'pitch',
        'hand/palm_normal':'palm_normal',
    },
    'WATCHED_PARAMS_IN_SWIPE' : {
        'swipe/duration':'duration_seconds',
        'swipe/start_position/x':'start_position.x',
        'swipe/start_position/y':'start_position.y',
        'swipe/start_position/z':'start_position.z',
        'swipe/direction/vector':'direction',
        'swipe/direction/name':'direction_name',
        'swipe/speed':'speed',
        'swipe/state':'state' # 1 : just started, 2 : running, 3 : just finished
    },
    'WATCHED_PARAMS_IN_CIRCLE' : {
        'circle/center/x':'center.x',
        'circle/center/y':'center.y',
        'circle/center/z':'center.z',
        'circle/progress':'progress',
        'circle/radius':'radius',
        'circle/clockwiseness':'clockwiseness',
        'circle/state':'state' # 1 : just started, 2 : running, 3 : just finished
        
    },
    'WATCHED_PARAMS_IN_KEY_TAP' : {
        'key_tap/activated':'activated',
    },
    'WATCHED_PARAMS_IN_SCREEN_TAP' : {
        'screen_tap/activated': 'activated',
    },
}

easyLeap.init(app_parameters)

osc_setup = (OSC_SERVER, OSC_PORT, OSC_ROOT)

from OSC import OSCClient, OSCMessage
def init(osc_setup):
    host, port, root = osc_setup
    client = OSCClient()
    client.connect( (host, port) )
    print "Connected to the OSC server %s:%s%s" %osc_setup
    send_parameter('osd_initialized','Done')
    return client

def send_parameters( hand_params):
    for path, value in hand_params.items():
        send_parameter(path, value)

def send_parameter( rel_path, data):
    full_path = OSC_ROOT+rel_path
    #client.send( OSCMessage( full_path, data ) )
    print "[osc]\t%s\t\t\t%s" %(full_path, data)

init(osc_setup)

def on_connect(leap_controller):
    print 'Leap connected'
def on_disconnect(leap_controller):
    print 'Leap disconnected'
def ignore(params):
    pass
def on_exit(leap_controller):
    print 'thx bybye'

events_response = {
    'on_connect':on_connect,
    'on_disconnect':on_disconnect,
    'on_hand':ignore,
    'on_circle':on_exit,
    'on_exit':on_exit,
}

listener = easyLeap.Listener(events_response) #Get listener which herits from Leap.Listener
controller = easyLeap.Leap.Controller()  #Get a Leap controller
controller.add_listener(listener)  #Attach the listener

sys.stdin.readline()

#Remove the sample listener when done
controller.remove_listener(listener)