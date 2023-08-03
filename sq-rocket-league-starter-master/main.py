# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits    

class Bot(GoslingAgent):
        # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.get_intent() is not None:
            return
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        targets = {
            'at_opponet_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self,targets)
        if len(hits['at_opponet_goal']) > 0:
            self.set_intent(hits['at_opponet_goal'][0])
            return
        if len(hits['away_from_our_net'])>0:
            self.set_intent(hits['away_from_our_net'][0])
            return 
        
        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return
        
        available_boost = [boost for boost in self.boosts if boost.large and boost.active]
        closest_boost = None
        closest_distance = 10000
        for boost in available_boost:
            distance = (self.me.location - boost.location).maginitude()
            if closest_boost is None or distance < closest_distance:
               closest_boost = boost
               closest_distance = distance
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            
        # closest_boost = self.get_closest_boost()
        
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            return
       