import unittest
import numpy as np
from numpy import testing as nptest
import scipy.ndimage.measurements as measurements
import cv2

class Picross:
    def __init__(self,x,rows,cols):
        self.width=x
        self.image=np.zeros((x,x))
        self.rows=rows
        self.cols=cols

    def get_slices(self,line):
        ret=[]
        labels,numLabels=measurements.label(line!=-1)
        for i in range(numLabels):
            ret.append(line[labels==i+1])
        return ret

    def analyse_slices(self,line,key):
        slices=self.get_slices(line)
        return slices


    def fillInColumnZerosWithMinusOne(self,idx):
        zero=self.image[:,idx]==0
        self.image[zero,idx]=-1

    def solve(self):
        i=0
        while(i<100):

            self.solveRows(self.rows)
            self.solveRows(self.cols,True)

            i+=1

        return self.image

    def solveRows(self,clues,flipped=False):
        if flipped:
            image = self.image.swapaxes(0,1)
        else:
            image = self.image

        for idx, row in enumerate(clues):
            if sum([clue for clue in row]) == self.width:
                image[idx] = 1
                continue

            if image[idx, 0] == 1:
                image[idx, :row[0]] = 1
                if row[0] != self.width:
                    image[idx, row[0]] = -1
                    #
                    # rowTest=[]
                    # currentNumber=0
                    # for element in self.image[2]:
                    #     if element==1:
                    #         currentNumber+=1
                    #     if element==-1:
                    #         rowTest.append(currentNumber)
                    #         currentNumber=0
                    # print rowTest
                    # for expected,result in zip(self.rows[2],rowTest):
                    #     if expected!=result:
                    #         pass

            if sum(image[idx]==1)==sum([clue for clue in row]):
                self.fillInColumnZerosWithMinusOne(idx)



class test_picross(unittest.TestCase):
    def show(self,image):
        image+=1
        image*=0.5
        cv2.imshow("picross",cv2.resize(image,(400,400)))
        cv2.waitKey(0)

    def setUp(self):
        rows=[[20],[5,10,2],[1,6,4,3,1],[6,6,1],[5,4,2],[2,2,8],[4,5,1],[4,7],[1,1,3],[1,1,1,3],[1,1,1,1,3,1],[3,1,3,3],[1,2,1,3,2,1],[1,3,1,5,1],[1,2,1,2,2,1],[4,1,1,1,2,3],[1,2,2,2,1,3,1],[1,1,1,1,1,2],[1,3,1,1,1,2],[1,1,1,2,2]]
        cols=[[8,2,2],[2,5,2,2],[5,2,2,2,2],[10,6],[6,2,2,1],[1,2,2,1,1],[3,2,4],[3,1,1],[2,3,5],[3,1,1],[3,2],[4,2,1],[6,4,4],[2,11],[16],[11,7],[1,2,3,2,4],[1,3,2,2],[2,2,1,2,3],[8,2,2]]
        self.Picross = Picross(20,rows,cols)
        self.picross = self.Picross.solve()


    def test_twentyFillsWholeLine(self):
        nptest.assert_array_equal(np.ones((20)),self.picross[0,:])

    def test_oneDoesntFillWholeLine(self):
        self.assertEqual(False,(np.ones(20)==self.picross[1,:]).all())

    def test_firstColumn_has_first_8_filled(self):
        nptest.assert_array_equal(np.ones(8),self.picross[:8,0])

    def test_0_9_minus1(self):
        self.assertEqual(-1,self.picross[8,0])

    def test_row_4_first_6_filled(self):
        nptest.assert_array_equal(np.ones(6),self.picross[3,:6])

    def test_when_column_complete_fill_rest_with_zeros(self):
        line=np.zeros(20)
        line[:16]=1
        line[16:]=-1
        nptest.assert_array_equal(line,self.picross[:,14])

    def test_third_line_returns_a_set_of_slices(self):
        line=[np.ones(1),np.array((1,1,1,0,1,1)),np.ones(4),np.array((1,1,0,0)),np.ones(1)]
        slices=self.Picross.get_slices(self.picross[2])
        nptest.assert_array_equal(line[0],slices[0])
        nptest.assert_array_equal(line[1],slices[1])
        nptest.assert_array_equal(line[2],slices[2])
        nptest.assert_array_equal(line[3],slices[3])
        nptest.assert_array_equal(line[4],slices[4])

    def test_third_line_fills_in_six(self):
        nptest.assert_array_equal(np.ones(6),self.Picross.analyse_slices(self.picross[2],self.Picross.rows[2])[1])


