'''
Udacity: ud436/sdn-firewall
Professor: Nick Feamster

TODO completed by Nam Pho (npho3) on 11/1/2014
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
from csv import DictReader


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

# Add your global variables here ...

# Note: Policy is data structure which contains a single
# source-destination flow to be blocked on the controller.
Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def read_policies (self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy(EthAddr(row['mac_0']), EthAddr(row['mac_1']))
        return policies

    def _handle_ConnectionUp (self, event):
        policies = self.read_policies(policyFile)
        for policy in policies.itervalues():
            # TODO: implement the code to add a rule to block the flow
            # between the source and destination specified in each policy

            # Note: The policy data structure has two fields which you can
            # access to turn the policy into a rule. policy.dl_src will
            # give you the source mac address and policy.dl_dst will give
            # you the destination mac address

            # Note: Set the priority for your rule to 20 so that it
            # doesn't conflict with the learning bridge setup

            # create generic table entry
            msg = of.ofp_flow_mod()
            msg.priority = 20
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

            # create generic match
            match = of.ofp_match()

            # policy in one direction
            match.dl_src = policy.dl_src
            match.dl_dst = policy.dl_dst
            msg.match = match
            event.connection.send(msg)

            # policy for opposite direction
            match.dl_src = policy.dl_dst
            match.dl_dst = policy.dl_src
            msg.match = match
            event.connection.send(msg)

            # debug
            log.info("Installing firewall rule for src=%s, dst=%s" % (policy.dl_src, policy.dl_dst))
            log.debug(msg)
        
        log.info("Hubifying %s", dpidToStr(event.dpid))

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
