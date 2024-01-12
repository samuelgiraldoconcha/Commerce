from . import models

def highest_bid(listing_id):
    bids = list(models.Listing.objects.get(id=listing_id).bids.all())
    if bids:
        highest_bid = max(bids, key= lambda x: x.offering_price)
        return highest_bid
    else:
        return None