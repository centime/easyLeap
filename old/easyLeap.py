from leap import Leap
from math import atan
import default_setup

GLOBALS = default_setup.GLOBALS

def init(globals):
    for k,v in globals.items():
        GLOBALS[k]=v


class Listener(Leap.Listener):  #The Listener that we attach to the controller.
   
    def __init__(self, actor):
        super(Listener, self).__init__()
        self.actor = actor
        self.center = Leap.Vector(GLOBALS['CENTER_X'],GLOBALS['CENTER_Y'],GLOBALS['CENTER_Z'])
                       
    def on_init(self, controller):
        pass
        
    def on_connect(self, controller):
        self.setup_gestures(controller)
        self.actor.on_connect(controller)

    def setup_gestures(self,controller):
        if GLOBALS['ENABLE_GESTURE_SWIPE'] :
            controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        if GLOBALS['ENABLE_GESTURE_CIRCLE'] :
            controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        if GLOBALS['ENABLE_GESTURE_KEY_TAP'] :
            controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        if GLOBALS['ENABLE_GESTURE_SCREEN_TAP'] :
            controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

        if(controller.config.set("Gesture.Swipe.MinLength", GLOBALS['GESTURE_SWIPE_MIN_LEN'])
          and controller.config.set("Gesture.Swipe.MinVelocity", GLOBALS['GESTURE_SWIPE_MIN_VEL'])):
            controller.config().save()

        if controller.config.set("Gesture.Circle.MinRadius", GLOBALS['GESTURE_CIRCLE_MIN_RADIUS']):
            controller.config.save()

        if(controller.config.set("Gesture.KeyTap.MinDownVelocity", GLOBALS['GESTURE_KEY_TAP_MIN_VEL'])
           and controller.config.set("Gesture.KeyTap.MinDistance", GLOBALS['GESTURE_KEY_TAP_MIN_LEN'])):
            controller.config.save()

        if(controller.config.set("Gesture.ScreenTap.MinForwardVelocity", GLOBALS['GESTURE_SCREEN_TAP_MIN_VEL'])
            and controller.config.set("Gesture.ScreenTap.MinDistance", GLOBALS['GESTURE_SCREEN_TAP_MIN_LEN'])):
                controller.config.save()

    def on_disconnect(self, controller):
        self.actor.on_disconnect(controller)

    def on_exit(self, controller):
        self.actor.on_exit(controller)

    def on_frame(self, controller):
        frame = controller.frame()  # Get latest information from the leapmotion
        if not frame.hands.empty:  # Only process if hands present
            if GLOBALS['MAIN_HAND'] == 'right' :
                hand = frame.hands.rightmost
            if GLOBALS['MAIN_HAND'] == 'left' :
                hand = frame.hands.leftmost
            
            if GLOBALS['ENABLE_HANDS'] :
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

                gesture.direction_name = self.get_direction_name(gesture.direction)

                gesture.current_position_name=self.get_position_name(gesture.hands[0].palm_position)
                gesture.start_position_name=self.get_position_name(gesture.start_position)

               
                watched_params = GLOBALS['WATCHED_PARAMS_IN_SWIPE']
            if gesture.type == 4 :
                gesture= Leap.CircleGesture(gesture)
                if gesture.pointable.direction.angle_to(gesture.normal) <= Leap.PI/2:
                    gesture.clockwiseness = "clockwise"
                else:
                    gesture.clockwiseness = "counterclockwise"

                gesture.position_name=self.get_position_name(gesture.center)

                watched_params = GLOBALS['WATCHED_PARAMS_IN_CIRCLE']
            if gesture.type == 5 :
                gesture.activated = True
                watched_params = GLOBALS['WATCHED_PARAMS_IN_SCREEN_TAP']
            if gesture.type == 6 :
                gesture.activated = True
                watched_params = GLOBALS['WATCHED_PARAMS_IN_KEY_TAP']
            

            for path, api in watched_params.items():
                try :
                    gesture_params[path] = eval('gesture.'+api )
                except:
                    print "%s\t%s not found. Valid api ?" %(path,api)

            if gesture.type == 1 :
                self.actor.on_swipe(gesture_params)
            if gesture.type == 4 :
                self.actor.on_circle(gesture_params)
            if gesture.type == 5 :
                self.actor.on_screen_tap(gesture_params)
            if gesture.type == 6 :
                self.actor.on_key_tap(gesture_params)
        

    def watch_params_in_hand(self,hand): 
    # Watch after every parameter specified in WATCHED_PARAMS_IN_HAND
        hand_params = {}
        hand.openess = hand.palm_position.distance_to(hand.sphere_center)
        hand.upside_down = hand.palm_position.y-hand.sphere_center.y < 0

        hand.pitch = atan(1.0*hand.palm_normal.z/hand.palm_normal.y)
        hand.roll = atan(1.0*hand.palm_normal.x/hand.palm_normal.y)
        
        hand.max_dist_fingers = hand.fingers.leftmost.stabilized_tip_position.distance_to(hand.fingers.rightmost.stabilized_tip_position)
        hand.max_angle_fingers = hand.fingers.leftmost.direction.angle_to(hand.fingers.rightmost.direction)

        hand.position_name = self.get_position_name(hand.palm_position)
    
        for path, api in GLOBALS['WATCHED_PARAMS_IN_HAND'].items():
            try :
                hand_params[path] = eval('hand.'+api )
            except:
                print "%s\t%s not found. Valid api ?" %(path,api)
        self.actor.on_hand(hand_params)

    def get_position_name(self, position):
        position_name = ''
        if position.x-self.center.x > GLOBALS['POSITION_THRSLD'] : position_name += ' right'
        if position.x-self.center.x <= -GLOBALS['POSITION_THRSLD'] : position_name += ' left'
        if position.y-self.center.y > GLOBALS['POSITION_THRSLD'] : position_name += ' top'
        if position.y-self.center.y <= -GLOBALS['POSITION_THRSLD'] : position_name += ' bottom'
        if position.z-self.center.z > GLOBALS['POSITION_THRSLD'] : position_name += ' back'
        if position.z-self.center.z <= -GLOBALS['POSITION_THRSLD'] : position_name += ' front'
        return position_name

    def get_direction_name(self, direction):
        direction_name = ''
        if direction.x > GLOBALS['DIRECTION_THRSLD'] : direction_name += ' right'
        if direction.x <= -GLOBALS['DIRECTION_THRSLD'] : direction_name += ' left'
        if direction.y > GLOBALS['DIRECTION_THRSLD'] : direction_name += ' top'
        if direction.y <= -GLOBALS['DIRECTION_THRSLD'] : direction_name += ' bottom'
        if direction.z > GLOBALS['DIRECTION_THRSLD'] : direction_name += ' back'
        if direction.z <= -GLOBALS['DIRECTION_THRSLD'] : direction_name += ' front'
        return direction_name


class Actor():
    def on_connect(self, leap_controller):
        print 'Leap connected'
        print
    def on_disconnect(self, leap_controller):
        print 'Leap disconnected'
        print
    def on_swipe(self, swipe_params):
        for k,v in swipe_params.items():
            print '%s\t\t\t%s' %(k,v)
        print
    def on_circle(self, circle_params):
        print 'o'
        for k,v in circle_params.items():
            print '%s\t\t\t%s' %(k,v)
        print
    def on_screen_tap(self, screen_tap_params):
        for k,v in screen_tap_params.items():
            print '%s\t\t\t%s' %(k,v)
        print
    def on_key_tap(self, key_tap_params):
        for k,v in key_tap_params.items():
            print '%s\t\t\t%s' %(k,v)
        print
    def on_hand(self, hand_params):
        for k,v in hand_params.items():
            print '%s\t\t\t%s' %(k,v)
        print
    def on_exit(self, leap_controller):
        print 'Exit.'
        print
           