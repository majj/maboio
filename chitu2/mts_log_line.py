# -*- coding: utf-8 -*-

"""

"""


import ast

import re
import time

import pprint

import pendulum
from transitions import Machine

import json
import toml

def get_conf(conf_file_path)->dict:
    """read toml conf file for latter use.


    :param conf_file_path: absolute path of conf file.
    :return:dict.
    """
    with open(conf_file_path) as conf_file:
        config = toml.loads(conf_file.read())
    
    #pprint.pprint(config)
    return config
    
def set_transitions(config)->dict:
    with open(config['mts']['transitions']['conf_dict']) as json_file:
        c = ast.literal_eval(json_file.read())
        config['mts']['transitions']['table'] = c 
    return config

class MtsStateMachine(object):
    """"""
    
    def __init__(self, config):
        """"""
        
        self.p_state = None
        self.p_time = None
        
        self.TRANSITIONS_set = set()        
        self.TRANSITIONS = []
        
        self.time_sum = {}

        self.pattern_mts_log_line = config['mts']['line_pattern']        
        self.compile_obj = re.compile(self.pattern_mts_log_line,  re.DOTALL | re.UNICODE)

        self.states = config['mts']['states']

        self.transitions = config['mts']['transitions']['table']
        # add common callback
        self.__build_trigger_pattern()      
    
    def __build_trigger_pattern(self):
        
        triggers = []
        
        for transition in self.transitions:
            
            triggers.append((transition['trigger']))
            # add 'before' and 'after' for each transition
            transition.update(before='on_enter', after='on_exit')
        
        trigger_pattern = '^"(?P<trigger>%s)' % '|'.join(triggers)
        
        self.compile_obj2 = re.compile(trigger_pattern,  re.DOTALL | re.UNICODE)
        
    def __sum(self, src, durition):
        
        if src in self.time_sum:
            self.time_sum[src] = self.time_sum[src] + durition.total_seconds()
        else:
            self.time_sum[src] = durition.total_seconds()
            
    def show(self, msg, src, trigger, dest, timestamp, duration):
        try:
            #if(src == 'run' and trigger == 'Stopped' and dest == 'stop'):
            print(">>> %s --- %s ---> %s [%s][%d][%s]" %(src, trigger, dest, timestamp, durition.total_seconds(), durition.in_words()))
            print(msg)
            #[%0d %0d %02d:%02d:%02d] durition.weeks, durition.remaining_days, durition.hours, durition.minutes, durition.seconds%60, 
        except Exception as ex:
            print(">>> %s --- %s ---> %s [%s]" %(src, trigger, dest, timestamp))
            print(ex)        
        
    def show_transitions(self):
        """show real transitions"""
        
        print(self.transitions)
        
    def parse_line(self, line):
        """return parsed line"""
        
        #match_obj = self.compile_obj.search(line)
        
        match_obj = self.compile_obj.search(line)
        
        if match_obj == None:
            return None, None, None, None

        # Retrieve group(s) from match_obj
        #all_groups = match_obj.groups()
        
        #print(all_groups      
        else:
        
            timestamp = match_obj.group(1)
            log_level = match_obj.group(2)
            logger = match_obj.group(3)
            msg_line = match_obj.group(4)        
            
            return timestamp, log_level, logger, msg_line
            
    def find_trigger(self, msg_line):
        """ find trigger from msg_line for state machine"""
        
        try:
            match_obj2 = self.compile_obj2.search(msg_line) 
        except Exception as ex:
            print(ex)
            print(msg_line)
            raise(Exception("error"))
        
        if match_obj2 != None:
            trigger = match_obj2.group('trigger')
            return trigger
        else:
            return None          
    
    def on_enter(self, event):
        """"""        
        #if 'timestamp' in event.kwargs:
        timestamp_str = event.kwargs['timestamp']
        timestamp = pendulum.parse(timestamp_str)
        msg = event.kwargs['message']
            
        if self.p_time == None:
            self.p_time = timestamp
            durition = timestamp - self.p_time
        else:    
            durition = timestamp - self.p_time
            
        
        src = event.transition.source
        dest = event.transition.dest
        trigger = event.event.name
        
        # transition table line
        transition = {'trigger': trigger, 'source': src, 'dest': dest }
        
        key_str = str(transition)
        if durition.total_hours() > 1:
            print("%s - %s,%s:%s" %(self.p_time.to_datetime_string(), 
                timestamp.to_datetime_string(), src,durition))
            print(key_str)
        
        self.__sum(src, durition)
        
        if key_str in self.TRANSITIONS_set:
            pass
        else:
            self.TRANSITIONS_set.add(key_str)
            self.TRANSITIONS.append(transition)
        #self.TRANSITIONS.add([trigger, src, dest ])
        self.p_state = src#self.state
        self.p_time = timestamp
    
    def on_exit(self, event):
        """"""
        if (self.p_state == self.state):
            #raise(Exception('no state changed!'))
            #print("state NO CHANGE!")
            pass
        
    def on_enter_error(self, event): 
        """"""
        #print(">>>Error!")
    
    def on_exit_error(self, event): 
        """"""
        #print(">>>No Error!")
        
    def build_point(self):
        """"""
        
        pass
    
class MtsLogLine(object):
    """"""
    
    def __init__(self, config):
        """"""

        self.data_files = {}
        
        self.config = set_transitions(config)
        
        #pprint.pprint(self.config)
        
    def __check_machine(self, filename):
        """"""
        
        # multi-state-machine for one machine        
        if filename in self.data_files:
            mts = self.data_files[filename]
        else:
            mts = MtsStateMachine(self.config)
            self.data_files[filename] = mts            
            #mts = MTSState()
            # Initialize
            machine = Machine(mts, states=mts.states, send_event=True, transitions=mts.transitions, initial='init')        
        
        return mts        
    
    def process_line(self, filename, line):       
        """"""
        
        mts = self.__check_machine(filename)  
        
        timestamp, log_level, logger, msg_line = mts.parse_line(line)
        try:
            trigger = mts.find_trigger(msg_line)
        except Exception as ex:
            print(msg_line)
            raise(Exception('error'))
            
        if trigger != None:
            #print(mts)
            mts.trigger(trigger, timestamp=timestamp, message = msg_line)
            #print(mts.p_state, '-->', mts.state)
            #print(trigger, ':', status_d[trigger])
            #print('<<<<<<<<<<')
        else:
            pass
            
        return mts



def gen_dot(states, TRANSITIONS):
    """"""
    
    #print(self.time_sum)
    
    nodes = ' '.join(states)
    
    x = []
    c = ['red','blue','green','midnightblue','deeppink4','darkorchid2','deepskyblue','deeppink1','forestgreen','brown','darkviolet']
    colors = {}
    i = 0
    s = set()
    for t in TRANSITIONS:
        s.add(t['trigger'])
        
    for t in s:
        colors[t] ='green'# c[i]
        i = i + 1
    
    for d in TRANSITIONS:
        s = '%s -> %s [ label = "%s" fontcolor="%s" color="%s" ];' %(d['source'], d['dest'], d['trigger'], colors[d['trigger']], colors[d['trigger']])
        x.append(s)
    
    edges = '\n'.join(x)
    
    dot = """
    digraph MTS {
        rankdir=LR;
        # size="8,5"
        
        node [shape = circle fillcolor=lightcyan style = filled];%s;
        %s
        }""" %(nodes, edges)
    
    #print(dot)
    with open('t6.dot','w') as fh:
        fh.write(dot)

def test(filename):
    """"""
    
    config = get_conf('app.toml')
    
    #print(config)
    
    mts_log_line = MtsLogLine(config)
    
    with open(filename, mode='rb') as fh: #, errors='ignore'
        msg = fh.read().decode('ISO-8859-1')
    #print(msg)
    for line in msg.split('\r\n'):
        if line != '':
            #print(line)
            mts = mts_log_line.process_line(filename, line)
        else:
            print('------')
            
    for filename in mts_log_line.data_files:
        mts = mts_log_line.data_files[filename]
        print(mts.time_sum)
        gen_dot(mts.states, mts.TRANSITIONS)

if __name__ == '__main__':
        
    fn = '../log/GEM control arm - two axle-5.log'
    test(fn)
    fn = '../log/GEM control arm - two axle-4.log'
    #test(fn)
