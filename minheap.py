# Implementation of minHeap assuming size of the heap is between 0 to 100
# If external list is passed as parameter it will be converted to heap inplace.
# Otherwise, a new list will be returned as heap
class Minheap:

    # initialize a heap as an empty list
    def __init__(self,heap=[]):
        self.heap_internal: list = heap

    # function to compare based on rideCost for a minHeap, in case of a tie, tripDuration is compared for the lower value
    def CompareRide(self, ride_1, ride_2):
        if ride_1.rideCost == ride_2.rideCost:
            return ride_1.tripDuration < ride_2.tripDuration
        return ride_1.rideCost < ride_2.rideCost

    # correct a heap by placing element at end to its correct place.
    # It compare childs with their parent and makes parent smallest by swapping. 
    # Same keeps looping until finds correct relation.
    def AdjustDown(self,start,end):
        heap=self.heap_internal
        newitem=heap[end]
        while end>start:
            parentpos=(end-1)>>1
            parent=heap[parentpos]
            if self.CompareRide(newitem, parent):
                heap[end]=parent
                end=parentpos
                continue
            break
        heap[end]=newitem

    #  adjust item at pos to its correct position and following sub tree, if misplaced
    def AdjustUp(self,pos):
        heap=self.heap_internal
        child=2*pos+1 # left child
        smallest=pos
        if child<len(heap) and self.CompareRide(heap[child], heap[smallest]):
            smallest=child
        if child+1<len(heap) and self.CompareRide(heap[child+1], heap[smallest]):
            smallest=child+1
        if smallest!=pos: 
            # if true means that node is incorrect.
            # So it swap with smaller child and recurse on child.
            heap[smallest],heap[pos]=heap[pos],heap[smallest]
            self.AdjustUp(smallest)

    # push item on the heap maintaining heap property.
    # Simply append item and then correct heap by AdjustDown
    def PushHeap(self,item):
        heap=self.heap_internal
        heap.append(item)
        self.AdjustDown(0,len(heap)-1)
    
    # remove item from the heap maintaining heap property.
    # It will swap last item with topmost and then correct the heap by AdjustUp
    def PopHeap(self):
        heap=self.heap_internal
        lastitem=heap.pop()
        if heap:
            topmost=heap[0]
            heap[0]=lastitem
            self.AdjustUp(0)
            return topmost
        return lastitem
    
    # create heap from rawlist
    def Heapify(self):
        heap=self.heap_internal
        for i in reversed(range(len(heap)//2)):
            self.AdjustUp(i)