from enum import Enum

# defining operations for better identification
class OperationType(Enum):
    PRINT_SINGLE = 1
    PRINT_MULTIPLE = 2
    INSERT = 3
    GET_NEXT_RIDE = 4
    CANCEL_RIDE = 5
    UPDATE_TRIP = 6