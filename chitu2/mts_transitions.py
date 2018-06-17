[
    { 'trigger': 'Error', 'source': '*', 'dest': 'error'},
    { 'trigger': 'error', 'source': '*', 'dest': 'error'},
    { 'trigger': 'System', 'source': '*', 'dest': 'error'},            
    # { 'trigger': 'Loading station', 'source': '*', 'dest': 'load'  },            
    # { 'trigger': 'Running FG', 'source': '*', 'dest': 'run'},            
    { 'trigger': 'Running', 'source': '*', 'dest': 'run'},            
    { 'trigger': 'Procedure Interlocked', 'source': '*', 'dest': 'error'},            
    { 'trigger': 'Holding', 'source': '*', 'dest': 'hold'},
    # { 'trigger': 'Stopped FG', 'source': '*', 'dest': 'stop'}, 
    { 'trigger': 'Stopped', 'source': '*', 'dest': 'stop'},            
    { 'trigger': 'Entering Stopped', 'source': '*', 'dest': 'stop'},
    { 'trigger': 'End of test', 'source': '*', 'dest': 'stop'},
    { 'trigger': 'Aborted', 'source': '*', 'dest': 'stop'},  
    { 'trigger': 'Procedure Interlocked', 'source': '*', 'dest': 'stop'},             
    { 'trigger': 'Exiting Stopped', 'source': '*', 'dest': 'idle'}
]