

import re

import time

from transitions import Machine

from t5 import MTSState

msg = '''(10/26/2017 16:39:26) Information [Stmgr] "HSM 5 -- Low Pressure."

(10/26/2017 16:39:26) Information [Stmgr] "HSM 8 -- Low Pressure."

(10/26/2017 16:39:29) Information [Stmgr] "HSM 5 -- No Pressure."

(10/26/2017 16:39:29) Information [Stmgr] "HSM 8 -- No Pressure."

(10/26/2017 16:39:32) Information [Stmgr] "HPU T9-J25 -- Low Pressure."

(10/26/2017 16:39:33) Information [Stmgr] "HPU T9-J25 -- No Pressure."

(10/27/2017 08:19:45) Information [Stmgr] "HPU T9-J25 -- High Pressure."

(10/27/2017 08:19:45) Information [Stmgr] "HSM 5 -- High Pressure."

(10/27/2017 08:19:45) Information [Stmgr] "HSM 8 -- High Pressure."

(10/27/2017 08:20:02) Information [MPT Runtime] "Exiting Stopped"

(10/27/2017 08:20:04) Information [MPT Runtime] "Running"

(10/27/2017 10:23:50) Information [MPT Runtime] "Entering Stopped"

(10/27/2017 10:23:52) Information [MPT Runtime] "Stopped
 Running Time:  02:05:03 
 Channel Counters:
    Fx -       7497  Cycles
    Fy -       7497  Cycles
 Sequence Counters:
    Group 1 -          1  
      Cyclic Command 1 -         47  Cycles
      Cyclic Command 2 - 
      Cyclic Command 3 - 
      Cyclic Command 4 - "

(10/28/2017 08:38:16) Information [MPT Runtime] "Exiting Stopped"

(10/28/2017 08:38:18) Information [MPT Runtime] "Running"

(10/29/2017 03:15:02) Information [MPT Runtime] "Procedure Done"

(10/29/2017 03:15:04) Information [MPT Runtime] "Stopped
 Running Time:  20:41:50 
 Channel Counters:
    Fx -      74500  Cycles
    Fy -      74500  Cycles
 Sequence Counters:
    Group 1 -         10  
      Cyclic Command 1 -       6500  Cycles
      Cyclic Command 2 -        200  Cycles
      Cyclic Command 3 -        450  Cycles
      Cyclic Command 4 -        300  Cycles"

(10/31/2017 09:52:02) Information [MPT Runtime] "Procedure Reset"

(10/31/2017 09:52:02) Information [MPT Runtime] "Procedure Beginning: control arm two axle 01.000"

(10/31/2017 09:52:02) Information [MPT Runtime] "Running"

(10/31/2017 10:22:21) Information [Stmgr] "HPU T9-J25 -- No Pressure."

(10/31/2017 10:22:21) Information [Stmgr] "HSM 5 -- No Pressure."

(10/31/2017 10:22:21) Information [Stmgr] "HSM 8 -- No Pressure."

(10/31/2017 10:22:21) Information [MPT Runtime] "Entering Stopped"

(10/31/2017 10:22:21) Error [MPT Runtime] "Procedure Interlocked: 'HSM 5' is 'Off'.
 Running Time:  00:30:19 
 Channel Counters:
    Fx -       1819  Cycles
    Fy -       1819  Cycles
 Sequence Counters:
    Group 1 -          0  
      Cyclic Command 1 -       1818  Cycles
      Cyclic Command 2 - 
      Cyclic Command 3 - 
      Cyclic Command 4 - "

(10/31/2017 10:22:21) Error [MPT Runtime] "Procedure Interlocked: 'HSM 5' is 'Off'.
 Running Time:  00:30:19 
 Channel Counters:
    Fx -       1819  Cycles
    Fy -       1819  Cycles
 Sequence Counters:
    Group 1 -          0  
      Cyclic Command 1 -       1818  Cycles
      Cyclic Command 2 - 
      Cyclic Command 3 - 
      Cyclic Command 4 - "

(10/31/2017 10:22:23) Information [MPT Runtime] "Stopped
 Running Time:  00:30:21 
 Channel Counters:
    Fx -       1819  Cycles
    Fy -       1819  Cycles
 Sequence Counters:
    Group 1 -          0  
      Cyclic Command 1 -       1819  Cycles
      Cyclic Command 2 - 
      Cyclic Command 3 - 
      Cyclic Command 4 - "

(10/31/2017 11:23:32) Information [Stmgr] "HPU T9-J25 -- Low Pressure."

(10/31/2017 11:23:32) Information [Stmgr] "HSM 5 -- Low Pressure."

(10/31/2017 11:23:32) Information [Stmgr] "HSM 8 -- Low Pressure."'''




status_d = {
    'Error':'error',
    'error':'error',
    'Sys':'error',
    'Running':'running',
    'Exiting Stopped':'???',
    'Hold':'stop',
    'Aborted':'stop',
    'End of test':'stop',
    'Entering Stopped':'stop'
}

def test():
    
    mts = MTSState()


    # Initialize
    machine = Machine(mts, states=mts.states, send_event=True, transitions=mts.transitions, initial='unknown')    
    
    pattern_mts_log = r"""\((.*)\) (\w+) \[(.*)\] (.*)"""
    
    compile_obj = re.compile(pattern_mts_log,  re.DOTALL | re.UNICODE)
    
    #v = test1()
    
    compile_obj2 = re.compile(mts.trigger_pattern,  re.DOTALL | re.UNICODE)
    
    for line in msg.split('\n\n'):
        #print(line)
        
        match_obj = compile_obj.search(line)

        # Retrieve group(s) from match_obj
        all_groups = match_obj.groups()
        
        #print(all_groups)
        
        x = match_obj.group(4)
        
        #print(x)
        
        match_obj2 = compile_obj2.search(x)    
        
        
        if match_obj2 != None:
            #print(match_obj2.groups())
            #k = match_obj2.group(1)
            #print(line)
            
            trigger = match_obj2.group('trigger')
            
            print('triger:',trigger)
            
            mts.trigger(trigger)
            print(mts.p_state, '-->', mts.state)
            #print(trigger, ':', status_d[trigger])
            print('<<<<<<<<<<')
        else:
            pass
        
        #print('>>>>>>>>>>>>>>>>>>>>')


def test1():
    

    
    #print(status_d)
    
    v = '|'.join(status_d.keys())
    v = '(?P<trigger>%s)' % v
    #print(v)
    return v


if __name__ == '__main__':
    test()
    #test1()
