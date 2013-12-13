import sys
from leap import Leap
from OSC import OSCClient, OSCMessage
from math import atan



OSC_SERVER = "localhost"
OSC_PORT = 2345
OSC_ROOT = "/" # Must start with /

MAIN_HAND = 'left'

GESTURE_SWIPE = True
GESTURE_CIRCLE = True
GESTURE_SCREEN_TAP = True
GESTURE_KEY_TAP = True

GESTURE_SWIPE_MIN_LEN = 70.0
GESTURE_SWIPE_MIN_VEL = 750.0
GESTURE_CIRCLE_MIN_RADIUS = 7.0
GESTURE_KEY_TAP_MIN_VEL = 40.0
GESTURE_KEY_TAP_MIN_LEN = 1.0
GESTURE_SCREEN_TAP_MIN_VEL = 5.0
GESTURE_SCREEN_TAP_MIN_LEN = 0.3

WATCHED_PARAMS_IN_HAND = {
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
    }

WATCHED_PARAMS_IN_SWIPE = {
    'swipe/duration':'duration_seconds',
    'swipe/start_position/x':'start_position.x',
    'swipe/start_position/y':'start_position.y',
    'swipe/start_position/z':'start_position.z',
    'swipe/direction/vector':'direction',
    'swipe/direction/name':'direction_name',
    'swipe/speed':'speed',
    'swipe/state':'state' # 1 = just started, 2 = running, 3 = just finished

}
WATCHED_PARAMS_IN_CIRCLE = {
    'circle/center/x':'center.x',
    'circle/center/y':'center.y',
    'circle/center/z':'center.z',
    'circle/progress':'progress',
    'circle/radius':'radius',
    'circle/clockwiseness':'clockwiseness',
    'circle/state':'state' # 1 = just started, 2 = running, 3 = just finished
    
}
WATCHED_PARAMS_IN_KEY_TAP = {
    'key_tap/activated':'activated',
}

WATCHED_PARAMS_IN_SCREEN_TAP = {
    'screen_tap/activated': 'activated',
}

def MOVE1(hand):
    # 2 fingres spread appart
    return (len(hand.fingers) == 2) and (hand.fingers[0].stabilized_tip_position.distance_to(hand.fingers[1].stabilized_tip_position) > 100)

def MOVE2(hand):
    # 3 fingers at ~90 degree one to another
    if len(hand.fingers) == 3 :
        directions = [ hand.fingers[0].direction, hand.fingers[1].direction, hand.fingers[2].direction ]
        for d in directions :
            dir2 = directions
            dir2.remove(d)
            for d2 in dir2:
                if d.angle_to(d2) < 0.50 :
                    return False
    else : 
        return False
    return True



def main(osc_setup):

    print "----------------------------------Initializing ----------------------------------"
    print


    actor = Sender(osc_setup)
    listener = Hands_Listener(actor) #Get listener which herits from Leap.Listener
    controller = Leap.Controller()  #Get a Leap controller

    print "Waiting for the Leap..."
    print

    controller.add_listener(listener)  #Attach the listener

    print "Press Enter to quit..."
    print
    print "---------------------------------- Running ----------------------------------"
    
    sys.stdin.readline()
    
    #Remove the sample listener when done
    controller.remove_listener(listener)


class Sender():
    def __init__(self, osc_setup):
        self.host, self.port, self.root = osc_setup
        self.client = OSCClient()
        self.client.connect( (self.host, self.port) )
        print "Connected to the OSC server %s:%s%s" %osc_setup
        self.send('init','leap listener program started')

    def send_hand(self, hand_params):
        print '********* HAND ***********'
        for path, value in hand_params.items():
            self.send(path, value)
    
    def send_gesture(self, gesture_params):
        print '********* GESTURE ***********'
        for path, value in gesture_params.items():
            self.send(path, value)

    def send(self, rel_path, data):
        full_path = self.root+rel_path
        #self.client.send( OSCMessage( full_path, data ) )
        print "[osc]\t%s\t\t\t%s" %(full_path, data)


class Hands_Listener(Leap.Listener):  #The Listener that we attach to the controller.
   
    def __init__(self, sender):
        super(Hands_Listener, self).__init__()  #Initialize like a normal listener
        self.sender = sender
                       

    def on_init(self, controller):
        pass
        
    def on_connect(self, controller):
        self.setup_gestures(controller)
        self.sender.send('init','Leap connected')

    def setup_gestures(self,controller):
        if GESTURE_SWIPE :
            controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        if GESTURE_CIRCLE :
            controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        if GESTURE_KEY_TAP :
            controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        if GESTURE_SCREEN_TAP :
            controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

        if(controller.config.set("Gesture.Swipe.MinLength", GESTURE_SWIPE_MIN_LEN)
          and controller.config.set("Gesture.Swipe.MinVelocity", GESTURE_SWIPE_MIN_VEL)):
            controller.config().save()

        if controller.config.set("Gesture.Circle.MinRadius", GESTURE_CIRCLE_MIN_RADIUS):
            controller.config.save()

        if(controller.config.set("Gesture.KeyTap.MinDownVelocity", GESTURE_KEY_TAP_MIN_VEL)
           and controller.config.set("Gesture.KeyTap.MinDistance", GESTURE_KEY_TAP_MIN_LEN)):
            controller.config.save()

        if(controller.config.set("Gesture.ScreenTap.MinForwardVelocity", GESTURE_SCREEN_TAP_MIN_VEL)
            and controller.config.set("Gesture.ScreenTap.MinDistance", GESTURE_SCREEN_TAP_MIN_LEN)):
                controller.config.save()

    def on_disconnect(self, controller):
        self.sender.send('error','Leap disconnected')

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()  # Get latest information from the leapmotion
        if not frame.hands.empty:  # Only process if hands present
            if MAIN_HAND == 'right' :
                hand = frame.hands.rightmost
            if MAIN_HAND == 'left' :
                hand = frame.hands.leftmost
            
            self.watch_params_in_hand(hand) # Watch after every parameter specified in WATCHED_PARAMS_IN_HAND
            gestures = frame.gestures()
            if not gestures.empty : #FIX hands ?
                for gesture in gestures :
                    self.watch_params_in_gesture(gesture)
            
        
    def watch_params_in_gesture(self,gesture):
        if len(gesture.hands) > 0 : #FIX hands ?
            gesture_params = {}
            if gesture.type == 1 :
                gesture= Leap.SwipeGesture(gesture)
                d = gesture.direction
                gesture.direction_name = 'not sure'
                if d.x > 0.7 : gesture.direction_name = 'right'
                if d.x <= -0.7 : gesture.direction_name = 'left'
                if d.y > 0.7 : gesture.direction_name = 'top'
                if d.y <= -0.7 : gesture.direction_name = 'bottom'
                if d.z > 0.7 : gesture.direction_name = 'back'
                if d.z <= -0.7 : gesture.direction_name = 'front'

                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    gesture.clockwiseness = "clockwise"
                else:
                    gesture.clockwiseness = "counterclockwise"
                
                watched_params = WATCHED_PARAMS_IN_SWIPE
            if gesture.type == 4 :
                gesture= Leap.CircleGesture(gesture)
                watched_params = WATCHED_PARAMS_IN_CIRCLE
            if gesture.type == 5 :
                gesture.activated = True
                watched_params = WATCHED_PARAMS_IN_SCREEN_TAP
            if gesture.type == 6 :
                gesture.activated = True
                watched_params = WATCHED_PARAMS_IN_KEY_TAP
            

            for path, api in watched_params.items():
                try :
                    gesture_params[path] = eval('gesture.'+api )
                except:
                    print "%s\t%s not found. Valid api ?" %(path,api)
            self.sender.send_gesture(gesture_params)
        

    def watch_params_in_hand(self,hand): 
    # Watch after every parameter specified in WATCHED_PARAMS_IN_HAND
        hand_params = {}
        hand.openess2 = hand.palm_position.distance_to(hand.sphere_center)
        hand.upside_down = hand.palm_position.y-hand.sphere_center.y < 0

        hand.pitch = atan(1.0*hand.palm_normal.z/hand.palm_normal.y)
        hand.roll = atan(1.0*hand.palm_normal.x/hand.palm_normal.y)
        
        hand.move1 = MOVE1(hand)
        hand.move2 = MOVE2(hand)

        for path, api in WATCHED_PARAMS_IN_HAND.items():
            try :
                hand_params[path] = eval('hand.'+api )
            except:
                print "%s\t%s not found. Valid api ?" %(path,api)
        #self.sender.send_hand(hand_params)
           
if __name__ == '__main__' :
    osc_setup = (OSC_SERVER, OSC_PORT, OSC_ROOT)

    main(osc_setup)

