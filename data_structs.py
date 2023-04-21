from ride import Ride
from rbtree import RedBlackTree
from minheap import Minheap

# initialize class for simultaneous operations between Red Black Tree and Min Heap
class CommonDataHandler:
    def __init__(self) -> None:
        self.mh = MinHeap()
        self.rbt = RBT()

    # Operation 1: prints the triplet (rideNumber, rideCost, tripDuration)
    def Print(self, rideNumber):
        res = self.rbt.SearchRide(rideNumber)
        return res

    # Operation 2:  prints all triplets (rx, rideCost, tripDuration) for which rideNumber1 <= rx <= rideNumber2
    def PrintRange(self, ride_number_start, ride_number_end):
        return self.rbt.SearchRideRange(ride_number_start, ride_number_end)
    
    # Operation 3: Inserts a ride where rideNumber differs from existing ride numbers
    def Insert(self, ride: Ride):
        if self.Print(ride.rideNumber).rideNumber == -1:
            self.rbt.Insert(ride)
            self.mh.Insert(ride)
        else:
            raise Exception("Duplicate RideNumber")
        
    # Operation 4: when this function is invoked, the ride with the lowest rideCost (ties are broken by 
    # selecting the ride with the lowest tripDuration) is output. This ride is then Deleted from the data structure
    def GetNextRide(self):
        removed = self.mh.Remove()
        if removed.rideNumber != -1:
            self.rbt.Remove(removed)
        return removed
    
    # Operation 5:  Deletes the triplet (rideNumber, rideCost, tripDuration) from the data 
    # structures, can be ignored if an entry for rideNumber doesn’t exist
    def CancelRide(self, rideNumber):
        r = self.rbt.SearchRide(rideNumber)
        self.rbt.Remove(r)
        self.mh.Delete(r.rideNumber)

    # Operation 6: updates the trip where the rider wishes to change destination with respect to certain cases
    def UpdateTrip(self, rideNumber, new_duration):
        original_ride = self.rbt.SearchRide(rideNumber)
        # condition a)
        if new_duration <= original_ride.tripDuration:
            self.CancelRide(original_ride.rideNumber)
            self.Insert(Ride(original_ride.rideNumber, original_ride.rideCost, new_duration))
        #  condition b)
        elif original_ride.tripDuration < new_duration <= 2 * original_ride.tripDuration:
            self.CancelRide(original_ride.rideNumber)
            self.Insert(Ride(original_ride.rideNumber, original_ride.rideCost + 10, new_duration))
        # condition c)
        elif new_duration > 2 * original_ride.tripDuration:
            self.CancelRide(original_ride.rideNumber)

# initialize class for Red Black Tree for operations such as Insertion, deletion and searching a ride
class RBT:
    def __init__(self) -> None:
        self.rbt = RedBlackTree()
    
    def Insert(self, ride: Ride):
        self.rbt.Insert(ride)
    
    def Remove(self, ride: Ride):
        self.rbt.Delete(ride)

    def SearchRide(self, rideNumber):
        res = self.rbt.Search(rideNumber)
        return res.item
    
    def SearchRideRange(self, start, end):
        return self.rbt.RangeSearch(start, end)

# initialize class for Min Heap for operations such as Insertion, deletion, pop, push and heapify
class MinHeap:
    def __init__(self) -> None:
        self.heapq = Minheap()
    
    def Insert(self, ride: Ride):
        self.heapq.PushHeap(ride)
        self.heapq.Heapify()
    
    def Remove(self):
        if len(self.heapq.heap_internal) == 0:
            return Ride(-1, -1, -1)
        ride_Remove = self.heapq.PopHeap()
        self.heapq.Heapify()
        return ride_Remove
    
    # Deletes ride by ride number
    def Delete(self, rideNumber):
        for r in self.heapq.heap_internal:
            if r.rideNumber == rideNumber:
                self.heapq.heap_internal.remove(r)
                break
        self.heapq.Heapify()