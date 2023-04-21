from operation_type import OperationType
class FileParser:

    # initialize a file handling class for reading input and writing to output text files
    def __init__(self, filename: str = "input.txt") -> None:
        self.input_file = open(filename, "r")
        self.output_file = open("output_file.txt", "w+")

    # function to parse each parameter identified as ride triplets or none in certain operations in each input line
    def ParseParam(self, line: str):
        parameter = line[line.index("(") + 1: line.index(")")]
        if len(parameter) != 0:
            return [eval(i) for i in parameter.split(",")] 
        else:
            return []

    # function to parse each line from the input file and categorise its operation type based on its function call start
    def ParseLine(self, line: str):
        p = self.ParseParam(line)
        if line.startswith("Insert"):
            return OperationType.INSERT, p
        elif line.startswith("GetNextRide"):
            return OperationType.GET_NEXT_RIDE, None
        elif line.startswith("Print"):
            if len(p) == 2:
                return OperationType.PRINT_MULTIPLE, p
            else:
                return OperationType.PRINT_SINGLE, p
        elif line.startswith("UpdateTrip"):
            return OperationType.UPDATE_TRIP, p
        elif line.startswith("Cancel"):
            return OperationType.CANCEL_RIDE, p

    def ParseFile(self):
        inputLines = self.input_file.readlines()
        parsedLines = []

        for eachLine in inputLines:
            parsedLines.append(self.ParseLine(eachLine))
        return parsedLines

    # function to append all output lines instead of printing to terminal to an output text file
    def AppendToOutput(self, line: str):
        self.output_file.write(line + "\n")

    # function to close all open input and output files
    def CloseAllFiles(self):
        self.input_file.close()
        self.output_file.close()