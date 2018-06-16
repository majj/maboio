

import time

from transitions import Machine





class MTSState(object):
    """"""
    
    def __init__(self):
        """"""
        
        self.p_state = None
        
        # The states
        self.states=['unknown', 'idle', 'running', 'stop', 'error']

        # And some transitions between states. We're lazy, so we'll leave out
        # the inverse phase transitions (freezing, condensation, etc.).
        self.transitions = [
            { 'trigger': 'Error', 'source': '*', 'dest': 'error' },
            { 'trigger': 'error', 'source': '*', 'dest': 'error'  },
            { 'trigger': 'Sys', 'source': '*', 'dest': 'error'  },
            
            { 'trigger': 'Running', 'source': '*', 'dest': 'running' },
            
            { 'trigger': 'Hold', 'source': '*', 'dest': 'stop'  },
            { 'trigger': 'Stopped', 'source': '*', 'dest': 'stop'  },            
            { 'trigger': 'Entering Stopped', 'source': '*', 'dest': 'stop'  },
            { 'trigger': 'End of test', 'source': '*', 'dest': 'stop'  },
            { 'trigger': 'Procedure Interlocked', 'source': '*', 'dest': 'stop'  },
            
             { 'trigger': 'Exiting Stopped', 'source': '*', 'dest': 'idle'  },
        ]

        #transitions3 = []

        # add common callback
        triggers = []
        for d in self.transitions:
            triggers.append((d['trigger']))
            d.update(before='check', after='show')
            
        v = '|'.join(triggers)
        self.trigger_pattern = '(?P<trigger>%s)' % v
        #print(v)
    
        #transitions3.append(d)
    
        #print(transitions)

        transitions2 = [
            ['Error', '*', 'error'],
            ['error', '*', 'error'],
            ['Sys', '*', 'error'],
            
            ['Running', '*', 'running'],    
            
            ['Hold', '*', 'stop'],
            ['Entering Stopped', '*', 'stop'],
            ['End of test', '*', 'stop'],
            
        ]        
        
        
        print('init...')
    
    def check(self, event):
        """"""
        
        if 't' in event.kwargs:
            print(event.kwargs['t'])
        #print(dir(event))
        #print('----------check-----------',self.state)
        #if self.p_state == None and self.state == 'unknown':
        self.p_state = self.state
    
    def show(self, event):
        """"""
        
        #print('----------show-----------', self.state)
        
    def on_enter_error(self, event): print(">>>Error!")
    def on_exit_error(self, event): print(">>>Stoped!")


def test():
    """"""
    
    mts = MTSState()


    # Initialize
    machine = Machine(mts, states=mts.states, send_event=True, transitions=mts.transitions, initial='unknown')



    # Now lump maintains state...
    print(mts.state)
    #print(dir(mts))

    time.sleep(1)
    print(mts.trigger('Running', t = time.time()))
    print(mts.p_state, '-->', mts.state)

    time.sleep(1)
    print(mts.trigger('Hold', t=1))
    print(mts.p_state, '-->', mts.state)

    time.sleep(1)
    print(mts.trigger('Stopped'))
    print(mts.p_state, '-->', mts.state)

    time.sleep(1)
    print(mts.trigger('Running'))
    print(mts.p_state, '-->', mts.state)
    
    
if __name__ == '__main__':
    test()