class Ride:
    rideNumber: int
    rideCost: int
    tripDuration: int

    # initialize the ride triplet assuming the number of active rides does not exceed 2000
    def __init__(self, rn, rc, td):
        self.rideNumber = rn
        self.rideCost = rc
        self.tripDuration = td

    # python function to convert object to string
    def __str__(self) -> str:
        return f'({self.rideNumber},{self.rideCost},{self.tripDuration})'