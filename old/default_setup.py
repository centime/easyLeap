
GLOBALS = {

    'MAIN_HAND' : 'left',
    
    'ENABLE_HANDS': True ,
    'ENABLE_GESTURE_SWIPE' : True,
    'ENABLE_GESTURE_CIRCLE' : True,
    'ENABLE_GESTURE_SCREEN_TAP' : True,
    'ENABLE_GESTURE_KEY_TAP' : True,

    'WATCHED_PARAMS_IN_HAND' : {
        'hand/fingers':'fingers.__len__()',
        'hand/max_dist_fingers':'max_dist_fingers',
        'hand/max_angle_fingers':'max_angle_fingers',
        'hand/position/x':'palm_position.x',
        'hand/position/y':'palm_position.y',
        'hand/position/z':'palm_position.z',
        'hand/position/name':'position_name',
        'hand/velocity/x':'palm_velocity.x',
        'hand/velocity/y':'palm_velocity.y',
        'hand/velocity/z':'palm_velocity.z',
        'hand/openess_api':'sphere_radius',
        'hand/openess':'openess',
        'hand/upside_down':'upside_down',
        'hand/roll':'roll',
        'hand/pitch':'pitch',
        'hand/palm_normal':'palm_normal',
    },
    'WATCHED_PARAMS_IN_SWIPE' : {
        'swipe/duration':'duration_seconds',
        'swipe/start_position/x':'start_position.x',
        'swipe/start_position/y':'start_position.y',
        'swipe/start_position/z':'start_position.z',
        'swipe/start_position/name':'start_position_name',
        'swipe/current_position/name':'current_position_name',
        'swipe/direction/vector':'direction',
        'swipe/direction/name':'direction_name',
        'swipe/speed':'speed',
        'swipe/state':'state' # 1 : just started, 2 : running, 3 : just finished

    },
    'WATCHED_PARAMS_IN_CIRCLE' : {
        'circle/center/x':'center.x',
        'circle/center/y':'center.y',
        'circle/center/z':'center.z',
        'circle/center/name':'position_name',
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


    'DIRECTION_THRSLD': 0.5,
    'POSITION_THRSLD': 40,
    'CENTER_X':0,
    'CENTER_Y':200,
    'CENTER_Z':0,


    'GESTURE_SWIPE_MIN_LEN' : 70.0,
    'GESTURE_SWIPE_MIN_VEL' : 750.0,
    'GESTURE_CIRCLE_MIN_RADIUS' : 7.0,
    'GESTURE_KEY_TAP_MIN_VEL' : 40.0,
    'GESTURE_KEY_TAP_MIN_LEN' : 1.0,
    'GESTURE_SCREEN_TAP_MIN_VEL' : 5.0,
    'GESTURE_SCREEN_TAP_MIN_LEN' : 0.3,

}