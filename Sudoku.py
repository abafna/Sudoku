# Imports
import numpy as np


class Sudoku(object):

    def __init__(self, grid):
        self.grid = grid
        self.gridChanged = True
        self.singletonCells = []
        self.rows = {}
        self.columns = {}
        self.blocks = {}
        self.possibleValuesInCells = {}
        for i in range(9):
            self.rows[i] = [1,2,3,4,5,6,7,8,9]
            self.columns[i] = [1,2,3,4,5,6,7,8,9]
            self.blocks[i] = [1,2,3,4,5,6,7,8,9]
        for i in range(81):
            self.possibleValuesInCells[i] = [1,2,3,4,5,6,7,8,9]

        # Update possible values for rows, columns, blocks from input grid.
        for i in range(81):
            rowNumber = int(i / 9)
            columnNumber = i % 9
            blockNumber = 3 * int(rowNumber / 3) + int(columnNumber / 3)
            digit = grid[rowNumber][columnNumber]
            if not digit == 0:
                self.rows[rowNumber].remove(digit)
                self.columns[columnNumber].remove(digit)
                self.blocks[blockNumber].remove(digit)
                self.possibleValuesInCells[i] = []

        # Update possible values for each cell
        for i in range(81):
            rowNumber = int(i / 9)
            columnNumber = i % 9
            blockNumber = 3 * int(rowNumber / 3) + int(columnNumber / 3)
            digit = grid[rowNumber][columnNumber]
            if digit == 0:
                self.possibleValuesInCells[i] = list(set.intersection(set(self.rows[rowNumber]), set(self.columns[columnNumber]), set(self.blocks[blockNumber])))

    def AddToGrid(self, gridIndex, digit):
        """
        Adds digit to the grid index and updates object.

        :param gridIndex: Grid index in row major format.
        :param digit: Digit to be added.
        """
        rowNumber = int(gridIndex / 9)
        columnNumber = gridIndex % 9
        blockRowNumber = int(rowNumber / 3)
        blockColumnNumber = int(columnNumber / 3)
        blockNumber = 3 * blockRowNumber + blockColumnNumber

        self.grid[rowNumber][columnNumber] = digit
        if digit not in self.rows[rowNumber]:
            raise ValueError("Digit %d already used." % digit)
        else:
            self.rows[rowNumber].remove(digit)
        if digit not in self.columns[columnNumber]:
            raise ValueError("Digit %d already used." % digit)
        else:
            self.columns[columnNumber].remove(digit)
        if digit not in self.blocks[blockNumber]:
            raise ValueError("Digit %d already used." % digit)
        else:
            self.blocks[blockNumber].remove(digit)
        self.possibleValuesInCells[gridIndex] = []

        for i in range(9):
            if digit in self.possibleValuesInCells[i * 9 + columnNumber]:
                self.possibleValuesInCells[i * 9 + columnNumber].remove(digit)
            if digit in self.possibleValuesInCells[rowNumber * 9 + i]:
                self.possibleValuesInCells[rowNumber * 9 + i].remove(digit)
        for j in range(blockRowNumber * 3, blockRowNumber * 3 + 3):
            for k in range(blockColumnNumber * 3, blockColumnNumber * 3 + 3):
                if digit in self.possibleValuesInCells[j * 9 + k]:
                    self.possibleValuesInCells[j * 9 + k].remove(digit)

    def Solve(self):
        """
        Solves current sudoku grid.

        """
        while self.gridChanged:
            self.gridChanged = False

            # Run singleton checks
            for cellNumber in range(81):
                if len(self.possibleValuesInCells[cellNumber])==1:
                    self.singletonCells.append(cellNumber)

            for i in self.singletonCells:
                if len(self.possibleValuesInCells[i]) == 1:
                    self.AddToGrid(i,self.possibleValuesInCells[i][0])
            self.singletonCells=[]

            # Run remaining number checks in blocks, rows, columns
            for i in range(9):

                # Check row for each remaining number in row i
                temp = {}
                for j in range(9):
                    cellNumber = 9 * i + j
                    for d in self.possibleValuesInCells[cellNumber]:
                        if d not in temp:
                            temp[d] = []
                        temp[d].append(cellNumber)
                for d in temp:
                    if len(temp[d]) == 1:
                        self.AddToGrid(temp[d][0], d)
                        self.gridChanged = True

                # Check column for each remaining number in column i
                temp = {}
                for j in range(9):
                    cellNumber = 9 * j + i
                    for d in self.possibleValuesInCells[cellNumber]:
                        if d not in temp:
                            temp[d] = []
                        temp[d].append(cellNumber)
                for d in temp:
                    if len(temp[d]) == 1:
                        self.AddToGrid(temp[d][0], d)
                        self.gridChanged = True

                # Check block for each remaining number in block i
                temp = {}
                startRow = int(i / 3)
                startCol = i % 3
                for j in range(startRow * 3, startRow * 3 + 3):
                    for k in range(startCol * 3, startCol * 3 + 3):
                        cellNumber = 9 * j + k
                        for d in self.possibleValuesInCells[cellNumber]:
                            if d not in temp:
                                temp[d] = []
                            temp[d].append(cellNumber)
                for d in temp:
                    if len(temp[d]) == 1:
                        self.AddToGrid(temp[d][0], d)
                        self.gridChanged = True

        if len(np.argwhere(self.grid == 0)) == 0:
            print("Solved.")
        else:
            print("Unsolved.")


if __name__ == "__main__":
    # input = np.array(
    #         [[0,0,8,5,6,0,0,0,1],
    #          [2,4,0,3,0,0,7,5,0],
    #          [5,0,0,0,0,0,0,8,3],
    #          [6,0,0,0,5,3,1,0,8],
    #          [0,0,0,9,0,6,0,0,0],
    #          [9,0,3,2,1,0,0,0,4],
    #          [1,9,0,0,0,0,0,0,7],
    #          [0,5,2,0,0,4,0,1,9],
    #          [8,0,0,0,3,9,6,0,0]])
    # input = np.array(
    #         [[0,0,6,9,0,0,3,0,0],
    #          [0,0,3,0,0,7,9,1,8],
    #          [0,9,0,0,5,4,0,0,0],
    #          [9,1,0,7,0,0,0,8,0],
    #          [6,5,0,0,0,0,0,9,2],
    #          [0,8,0,0,0,9,0,7,1],
    #          [0,0,0,2,7,0,0,5,0],
    #          [2,7,1,4,0,0,8,0,0],
    #          [0,0,5,0,0,1,7,0,0]])
    # input = np.array(
    #         [[5,0,0,0,0,9,3,0,0],
    #          [0,0,9,0,0,0,8,0,0],
    #          [0,0,0,3,0,0,7,6,0],
    #          [0,0,0,1,9,0,0,2,5],
    #          [6,0,0,0,0,0,0,0,7],
    #          [7,2,0,0,6,8,0,0,0],
    #          [0,6,4,0,0,3,0,0,0],
    #          [0,0,7,0,0,0,2,0,0],
    #          [0,0,8,5,0,0,0,0,1]])
    # input = np.array(
    #         [[0,0,5,0,0,0,2,0,0],
    #          [0,1,0,0,0,7,0,0,0],
    #          [7,2,0,0,0,4,0,6,8],
    #          [0,0,0,0,4,5,0,9,0],
    #          [5,0,2,0,0,0,3,0,6],
    #          [0,7,0,1,2,0,0,0,0],
    #          [2,3,0,9,0,0,0,5,1],
    #          [0,0,0,7,0,0,0,3,0],
    #          [0,0,6,0,0,0,8,0,0]])
    # input = np.array(
    #         [[0,0,0,0,0,0,0,0,2],
    #          [7,0,0,0,9,4,8,0,0],
    #          [6,3,0,0,0,0,4,0,0],
    #          [0,0,2,0,0,1,0,0,0],
    #          [1,8,0,3,0,6,0,5,9],
    #          [0,0,0,8,0,0,3,0,0],
    #          [0,0,7,0,0,0,0,3,8],
    #          [0,0,1,5,3,0,0,0,7],
    #          [5,0,0,0,0,0,0,0,0]])

    mySudoku = Sudoku(grid=input)
    mySudoku.Solve()
