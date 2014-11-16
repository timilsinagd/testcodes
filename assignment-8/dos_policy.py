# Udacity
# Computer Networking
# Assignment 8: Applications of SDN
#
# Professor: Nick Feamster
# Teaching Assistant: Ben Jones
#
# TODO completed by Nam Pho (npho3) on 11/15/14
#
################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
# author: Muhammad Shahbaz (muhammad.shahbaz@gatech.edu)                       #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

from ..policies.base_policy import *
from ..drivers.sflow_event import *
from ..globals import *

HOST = 'localhost'
PORT = 8008

class DDoSPolicy(BasePolicy):
    
    def __init__(self, fsm):
        self.fsm = fsm

    def block_policy(self):
        return drop
        
    def allow_policy(self):
        return passthrough
    
    def action(self):
        if self.fsm.trigger.value == 0:
            # TODO- set the policy for this application
            #
            # To set the policy for this application, implement the
            # following steps:
            #
            # 1. get the list of hosts in ddos attacker state
            #
            # 2. match the incoming packet's source and destination ip
            #  against that list of hosts (using pyretic predicates
            #  i.e., "match", "modify", and "if_" etc)
            #
            # 3. if there is a match apply drop policy, else apply
            #  policy passthrough and return the policy you just
            #  created

            # Parallel composition- return the policy that you created
            
            p1 = ~self.fsm.get_policy("ddos-attacker")
            
            return p1

        else:
            return self.turn_off_module(self.fsm.comp.value)
