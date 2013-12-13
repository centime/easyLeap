import sys
from leap import Leap
from OSC import OSCClient, OSCMessage
from math import sqrt

OSC_SERVER = "localhost"
OSC_PORT = 2345
OSC_ROOT = "/" # Must start with /

WATCHED_PARAMS_IN_HAND = {
    'which':'which', #needed
    '<which>/id':'id',
    '<which>/fingers':'fingers.__len__() ',
    '<which>/position/x':'palm_position.x',
    '<which>/position/y':'palm_position.y',
    '<which>/position/z':'palm_position.z',
    '<which>/openess':'openess',
    '<which>/upside_down':'upside_down',
    '<which>/move1':'move1',
    '<which>/move2':'move2',
    }

'''
WATCHED_PARAMS_IN_HAND = {
    'which':'which',
    }
'''

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

MAGIC_DEBOUNCER = 5     # Increase it for stability over responsability for right/left recognization
MAGIC_TRSLD_ANGLE = 1.3     # Angle diff must be at least 1.3 times the average to consider it is the thumb


def main(osc_setup, watched_params_in_hand):

    print "----------------------------------Initializing ----------------------------------"
    print


    #print "Get an actor for sending OSC messages."
    actor = Sender(osc_setup)

    #print "Get a hands listener and bind it with the actor."
    listener = Hands_Listener(actor,watched_params_in_hand) #Get listener which herits from Leap.Listener

    #print "Get a Leap controller."
    controller = Leap.Controller()  #Get a Leap controller

    #print "Binding the Listener to the controller."

    controller.add_listener(listener)  #Attach the listener
    

    #Keep this process running until Enter is pressed
    
    
    print "Press Enter to quit..."
    print
    print "---------------------------------- Running ----------------------------------"
    
    sys.stdin.readline()
    
    #Remove the sample listener when done
    controller.remove_listener(listener)


class Sender():
    #Takes the short moves defined by the user, parse them and store them in a strucured hash table.
    #Process the gestures from the listener : find the associated command, ask for a confirmation, execute the command.
    def __init__(self, osc_setup):
        self.host, self.port, self.root = osc_setup
        self.client = OSCClient()
        self.client.connect( (self.host, self.port) )
        print "Connected to the OSC server %s:%s%s" %osc_setup
        self.send('init','leap_listener initialized')

    def send_hand(self, hand_params):
        print '********* HAND ***********'
        which = hand_params['which']
        for path, value in hand_params.items():
            path = path.replace('<which>',which)
            self.send(path, value)

    def send(self, rel_path, data):
        full_path = self.root+rel_path
        #self.client.send( OSCMessage( full_path, data ) )
        print "[osc]\t%s\t\t\t%s" %(full_path, data)


class Hands_Listener(Leap.Listener):  #The Listener that we attach to the controller.
   
    def __init__(self, sender, watched_params_in_hand):
        super(Hands_Listener, self).__init__()  #Initialize like a normal listener
        self.sender = sender
        self.watched_params_in_hand = watched_params_in_hand      
        self.hands_manager = Hands_Manager()                 

    def on_init(self, controller):
        pass
        #print "Listener initialized"

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        '''
            if(controller.config.set_float("Gesture.Swipe.MinLength", 200.0)
              and controller.config.set_float("Gesture.Swipe.MinVelocity", 750)):
                controller.config().save()
        '''
        print
        print "***************************"
        print "\tLeap connected"
        print "\t gesture recognition enabled"
        print "***************************"
        print

    def on_disconnect(self, controller):
        print
        print "***************************"
        print "\tLeap disconnected"
        print "***************************"
        print

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()  # Get latest information from the leapmotion
        print len(frame.hands)
        if False :
            if not frame.hands.empty:  # Only process if hands present
                hands_lr = self.hands_manager.recognize_hands(frame.hands) # tell left or right

                for hand in hands_lr:    # For each hand   
                    self.watch_params_in_hand(hand) # Watch after every parameter specified in WATCHED_PARAMS_IN_HAND
                '''
                gestures = frame.gestures()
                if not gestures.empty :
                    for gesture in gestures :
                        self.watch_params_in_gesture(gesture)
                '''
        
        
    def watch_params_in_gesture(self,gesture):
        if len(gesture.hands) > 0 :
            print '\t\t\t************ GESTURE *************'
            for hand in gesture.hands :
                print "\t\t\thand %s" % self.hands_manager.which(hand)
            print gesture.type
        

    def watch_params_in_hand(self,hand): 
    # Watch after every parameter specified in WATCHED_PARAMS_IN_HAND
        hand_params = {}
        hand.openess = hand.palm_position.distance_to(hand.sphere_center)
        hand.upside_down = hand.palm_position.y-hand.sphere_center.y < 0
        hand.move1 = MOVE1(hand)
        hand.move2 = MOVE2(hand)
        for path, api in self.watched_params_in_hand.items():
            try :
                hand_params[path] = eval('hand.'+api )
            except:
                print "%s\t%s not found. Valid api ?" %(path,api)
        self.sender.send_hand(hand_params)
        



class Hands_Manager(object):
    def __init__(self):
        self.hand_seen_as_right = {} # debouncers

    def which(self,hand):
        if (hand.id in self.hand_seen_as_right.keys()) :
            if self.hand_seen_as_right[hand.id].state :
                return 'right'
            else :
                return 'left'
        else :
            return 'unknown'

    def recognize_hands(self, hands):
        hands_lr = []

        for hand in hands:
            self.register_hand_if_new(hand)
            hands_lr.append(hand)

        if len(hands_lr) ==  2 :
            self.distinguish_hands(hands_lr, hands.leftmost, hands.rightmost)
        else : 
            self.update_bouncer_from_thumb(hands_lr[0])      
    
        for hand in hands_lr :
            if self.hand_seen_as_right[hand.id].state :
                hand.which = 'right'
            else :
                hand.which = 'left'
        return hands_lr

    def distinguish_hands(self, hands, leftmost, rightmost):
        for hand in hands :
            if hand == leftmost:
                self.set_bouncer_to_left(hand)
            elif hand == rightmost:
                self.set_bouncer_to_right(hand)

    def register_hand_if_new(self,hand):    
        if not (hand.id in self.hand_seen_as_right.keys()) :
            self.hand_seen_as_right[hand.id] = Debouncer(MAGIC_DEBOUNCER)


    def update_bouncer_to_right(self, hand):
        self.hand_seen_as_right[hand.id].signal(True)

    def update_bouncer_to_left(self, hand):
        self.hand_seen_as_right[hand.id].signal(False)

    def set_bouncer_to_right(self,hand):
        self.hand_seen_as_right[hand.id].opposite_counter = 0
        self.hand_seen_as_right[hand.id].state = True

    def set_bouncer_to_left(self,hand):
        self.hand_seen_as_right[hand.id].opposite_counter = 0
        self.hand_seen_as_right[hand.id].state = False


    def update_bouncer_from_thumb(self, hand):
        if len(hand.fingers)>0 :

            hand_updside_down = hand.palm_position.y-hand.sphere_center.y < 0 

            avg_angle = 0
            i=0
            for finger in hand.fingers :
                avg_angle += finger.direction.angle_to(hand.direction)
                i += 1
            avg_angle /= i

            angle_leftmost = hand.direction.angle_to(hand.fingers.leftmost.direction)
            angle_rightmost = hand.direction.angle_to(hand.fingers.rightmost.direction)

            if (abs(angle_rightmost/avg_angle) > MAGIC_TRSLD_ANGLE) or (abs(angle_leftmost/avg_angle) > MAGIC_TRSLD_ANGLE):
                if (angle_rightmost > angle_leftmost) :
                    if not hand_updside_down :
                        self.update_bouncer_to_left(hand)
                    else : 
                        self.update_bouncer_to_right(hand)
                else : 
                    if not hand_updside_down :
                        self.update_bouncer_to_right(hand)
                    else :
                        self.update_bouncer_to_left(hand)

class Debouncer(object):  #Takes a binary "signal" and debounces it.
    def __init__(self, debounce_time):  #Takes as an argument the number of opposite samples it needs to debounce.
        self.opposite_counter = 0  #Number of contrary samples vs agreeing samples.
        self.state = True  #Default state. True = Right hand
        self.debounce_time = debounce_time  #Number of samples to change states (debouncing threshold).

    def signal(self, value):  #Update the signal.
        if value != self.state:  #We are receiving a different signal than what we have been.
            self.opposite_counter += 1
        else:  #We are recieving the same signal that we have been
            self.opposite_counter -= 1

        if self.opposite_counter < 0: self.opposite_counter = 0
        if self.opposite_counter > self.debounce_time: self.opposite_counter = self.debounce_time
        #No sense building up negative or huge numbers of agreeing/contrary samples

        if self.opposite_counter >= self.debounce_time:  #We have seen a lot of evidence that our internal state is wrong
            self.state = not self.state  #Change internal state
            self.opposite_counter = 0  #We reset the number of contrary samples
        return self.state  #Return the debounced signal (may help keep code cleaner)

    def set(self, value): # set the signal to value, and opposite_counter to 0
        self.state = value
        self.opposite_counter = 0
           
if __name__ == '__main__' :
    osc_setup = (OSC_SERVER, OSC_PORT, OSC_ROOT)

    main(osc_setup, WATCHED_PARAMS_IN_HAND)

