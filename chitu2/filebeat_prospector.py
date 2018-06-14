# -*- coding: utf-8 -*-

"""
move data from redis[filebeat] to influxdb

http://redisdoc.com/

configuration of multiline merge in filebeat.yum:
https://www.elastic.co/guide/en/beats/filebeat/current/multiline-examples.html

multiline.pattern: '^\['
multiline.negate: true
multiline.match: after


"""

import os

import json
import time

import re

import pendulum
import redis

class PostgreSQLClient(object):
    
    pass


class TSDBClient(object):
    
    pass


class InfluxClient(object):
    
    def __init__(self):
        """
        """
        
    def _send(self):
        """
        """
        
    def send(self):
        """
        """
        
        measurement = "MTS"
        tags = None
        timestamp = 1
        fields = []
            
        time_precision = ''
        
        josn_data = [
            {
                'measurement': measurement,
                'tags': tags,
                'time': timestamp,
                'fields': fields
            }
        ]

        print(josn_data, time_precision, sep=' ', end='\n')
    
    
class EtcdClient(object):
    
    pass

def gPRCClient():
    
    pass

def HeatbeatLine():        
    
    pass
    
class MTSLog(object):
    
    def __init__(self):
        
        """
        - timestamp (line num?)
        - status
        - level
        - logger
        - offset
        - task
        - seq? (in the same second), if timestamp changed then reset seq.
        """

class Processor(object):
    
    """
    prospector / processor
    """
    
    def __init__(self):
        """
        
        """
        
        pattern_log = r"""\[(.*)\] (\w+): (\w+): (.*)"""
        
        #time, level, logger, message
        pattern_mts_log = r"""\((.*)\) (\w+) \[(.*)\] (.*)"""
        

        # https://www.elastic.co/guide/en/beats/filebeat/current/_examples_of_multiline_configuration.html
        self.compile_obj = re.compile(pattern_mts_log,  re.DOTALL | re.UNICODE)
        
        error = ['Error','error','Sys']
        running = ['Running']
        stop   = ['Stop','Hold','Aborted','End of test','Entering Stopped']
        
        status = {
            'Error':'error',
            'error':'error',
            'Sys':'error',
            'Running':'running',
            'Stop':'stop','Hold':'stop',
            'Aborted':'stop','End of test':'stop',
            'Entering Stopped':'stop'
        }
        
        log_level = {'Warning':4,
                'Information' : 6,
                'debug' : 7,
                'notice' : 5,
                'Error' : 3,
                'crit' : 2,
                'alert':1,
                'emerg':0}
        
        pass

    def _parse_line(self, msg_line):
        """
                
        """
        
        print(msg_line)    
        

        match_obj = self.compile_obj.search(msg_line)

        # Retrieve group(s) from match_obj
        all_groups = match_obj.groups()

        # Retrieve group(s) by index
        # timestamp, level, logger, message
        time_str = match_obj.group(1)
        group_2 = match_obj.group(2)
        group_3 = match_obj.group(3)
        group_4 = match_obj.group(4)
        
        
        timestamp = int(self.parse_timestamp(time_str))
        
        return (timestamp)
        
    def parse_timestamp(self, time_str) -> int:
        
        print(time_str)
        
        timestamp = pendulum.parse(time_str) #, tz='Asia/Shanghai')
        #print(timestamp.int_timestamp)
        #print(timestamp.microsecond)
        return 1000000 * timestamp.float_timestamp
        
    def _get_task(self, source):
        
        x = source.split(os.sep)
        
        if x[-1].count('full') > 0:
            print('1')
        else:
            print('full')
        
        print(x)
        #print(source)
    
    def msg_process(self, filebeat):
        
        
        offset = filebeat['offset']
        
        print('offset:', offset)
        
        source =filebeat['source']
        
        t2 = self.parse_timestamp(filebeat['@timestamp'])
        
        (timestamp) = self._parse_line(filebeat['message'])
        
        
        if t2 - timestamp > 10000000:
            print('diff:', t2 - timestamp)
        
        self._get_task(source)
        
        tags = {'a':'b'}
        
        fields = {'offset':offset}
        
        point = {
                'measurement': 'measurement',
                'tags': tags,
                'time': timestamp,
                'fields': fields
            }
        
        
        return point
    
class BeatChecker(object):
    """ Beat Checker """
    
    def __init__(self):
        """ test for read filebeat """
        
        self.list_key = 'filebeat'
        
        with open("t1.lua") as fh:
            lua_script = fh.read()

        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        
        # EVALSHA 
        self.multiply = self.r.register_script(lua_script)        
        
        # create Processor class here
        self.processor = Processor()
        
        
    def _check(self):
        """
        filebeat:
        {'@metadata': {'beat': '', 'type': 'doc', 'version': '6.2.4'},
         '@timestamp': '2018-06-12T10:40:34.233Z',
         'beat': {'hostname': 'MABO', 'name': 'MABO', 'version': '6.2.4'},
         'message': '[2018-06-12 10:40:34.033552] DEBUG: gen_log: msg 38346',
         'offset': 1120,
         'prospector': {'type': 'log'},
         'source': 'G:\\github\\maboio\\log\\heartbeat.log',
         'tags': ['sim']}          
        """
        
        # lpop for filebeat: first in first out
        data = self.r.lpop(self.list_key)
        
        self.r.rpush("fb_test", data)
        
        if data == None:
            return 0
            
        json_str =data.decode('utf-8')
        
        filebeat_d = json.loads(json_str)        
        
        point = self.processor.msg_process(filebeat_d)
        
        return point
        """
        if i == 0:            
            # call lua script
            rtn = self.multiply(keys=['eqpt','msg'], 
                    args=[filebeat_d['message'],
                          filebeat_d['@timestamp']])
            
            print(rtn)
        """
        
    def check(self) -> bool:
        """
        check redis LIST
        """
        
        list_len = self.r.llen(self.list_key)
        
        print(list_len)
        
        list_len = self.r.llen(self.list_key)
        
        if list_len>0:
            
                point = self._check()
                
                self.r.rpush('data_queue', point)

    def run(self):    
        """
        run this beat checker
        """
        
        while True:        
            try:
                self.check()
            except Exception as ex:
                print(ex)
            finally:
                time.sleep(1)

if __name__ == '__main__':

    checker = BeatChecker()
    
    checker.run()