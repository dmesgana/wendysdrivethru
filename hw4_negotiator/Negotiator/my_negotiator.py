from negotiator_base import BaseNegotiator
from random import random


class MyNegotiator(BaseNegotiator):

    def make_offer(self, offer):
        self.offer = offer
        if random() < 0.125 and offer is not None:
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer
        else:
            ordering = self.preferences
            ourOffer = []
            for item in ordering.keys():
                if random() < 0.2:
                    ourOffer = ourOffer + [item]
            self.offer = ourOffer
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer