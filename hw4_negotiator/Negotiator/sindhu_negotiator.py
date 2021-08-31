from negotiator_base import BaseNegotiator
from random import random

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class SindhuNegotiator(BaseNegotiator):

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        if offer is None or self.getUtility(offer) <= self.getUtility(self.preferences):
            # first offer is for everything
            print("counter offer BITCH ", self.preferences)
            offer = self.preferences
        else:
            print("here")
        self.offer = offer
        return self.offer

    def getUtility(self, offer):
        temp = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = temp
        return util