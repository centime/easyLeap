from OSC import OSCClient, OSCMessage

class OscSender():
    def __init__(self, osc_setup):
        self.host, self.port, self.root = osc_setup
        self.client = OSCClient()
        self.client.connect( (self.host, self.port) )
        print "Connected to the OSC server %s:%s%s" %osc_setup
        self.send_parameter('osd_initialized','Done')

    def send_parameters(self, hand_params):
        for path, value in hand_params.items():
            self.send_parameter(path, value)

    def send_parameter(self, rel_path, data):
        full_path = self.root+rel_path
        #self.client.send( OSCMessage( full_path, data ) )
        print "[osc]\t%s\t\t\t%s" %(full_path, data)

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
    full_path = root+rel_path
    #client.send( OSCMessage( full_path, data ) )
    print "[osc]\t%s\t\t\t%s" %(full_path, data)
