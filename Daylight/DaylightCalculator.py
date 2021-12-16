# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 13:29:22 2016

@author: Thomas Clark

This script calculates areas within a floorplate over a threshold lux level

Ensure this file is located in the same directory as the radiance output .vtp files.
A new directory, 'output' will be created, into which results will be written.

"""

# preamble
import xml.etree.ElementTree
import os
import numpy as np
import sys

files=[]
output={}

# user input for evaluation
minVal=[]

evalType = input('Please input evaluation type (lux or DF): ')

if evalType == 'lux' or evalType == 'Lux':
    for item in (input('Please input lux values to evaluate, separated by commas: ').split(',')):
        minVal.append(float(item))
elif evalType == 'df' or evalType == 'DF':
    for item in (input('Please input DF values to evaluate, separated by commas: ').split(',')):
        minVal.append(float(item))
else:
    print('Unknown value entered, program exit')    
    sys.exit()

# get current working folder
folder=os.getcwd()

# output results to csv
outname = "Illuminance Results"
if not os.path.exists(os.path.join(folder,"output")):
    os.makedirs(os.path.join(folder,"output"))
numfiles=len(os.listdir(os.path.join(folder,"output")))
outputname=outname+"_"+str(numfiles+1)+".csv"
foutName = os.path.join(folder,"output", outputname)

# create lsit of vtp files in folder
for file in os.listdir(folder):
    if file.endswith(".vtp"):
        files.append(file)

# initialise areas for calculations
totalArea=0
totalOver=0

"""
Classes and helper functions
"""

class Polygon:
    #inputs: tuple of point names, centre and normal as floats
    def __init__(self,allpoints,points,centre,normal,val):
        self.centre=[]
        self.normal=[]
        self.pointVals=[]
        self.area=0
        self.val=val

        for item in points:
            point_value_list=(float(allpoints[int(item)].x),float(allpoints[int(item)].y),float(allpoints[int(item)].z))
            self.pointVals.append(point_value_list)

        """
        The below adapted from function written by Jamie Bull, source:
        http://stackoverflow.com/questions/12642256/python-find-area-of-polygon-from-xyz-coordinates
        """

        def unit_normal(a, b, c):
            x = np.linalg.det([[1,a[1],a[2]],
                     [1,b[1],b[2]],
                     [1,c[1],c[2]]])
            y = np.linalg.det([[a[0],1,a[2]],
                     [b[0],1,b[2]],
                     [c[0],1,c[2]]])
            z = np.linalg.det([[a[0],a[1],1],
                     [b[0],b[1],1],
                     [c[0],c[1],1]])
            magnitude = (x**2 + y**2 + z**2)**.5
            return (x/magnitude, y/magnitude, z/magnitude)

        if len(self.pointVals) < 3: # not a plane - no area
            return 0
        total = [0, 0, 0]
        N = len(self.pointVals)
        for i in range(N):
            vi1 = self.pointVals[i]
            vi2 = self.pointVals[(i+1) % N]
            prod = np.cross(vi1, vi2)
            total[0] += prod[0]
            total[1] += prod[1]
            total[2] += prod[2]
        result = np.dot(total, unit_normal(self.pointVals[0], self.pointVals[1], self.pointVals[2]))
        self.area=(abs(result/2))

    def __repr__(self):
        return str(self.centre)

class Point:
    def __init__(self,name,x,y,z):
        self.name=name
        self.value=(x,y,z)
        self.x=x
        self.y=y
        self.z=z

"""
Functions
"""

# calculate area >minVal (this returns #points > 200lux / #points)
def loadData(file,name,value,evalType):
    e = xml.etree.ElementTree.parse(file).getroot()

    allpoints=[]
    polygons=[]

    pointsTemp=[]
    connectivityTemp=[]
    offsetsTemp=[]
    offsetsTemp2=[]
    centresTemp=[]
    normalsTemp=[]
    valTemp=[]

    total_area=0
    area_over=0

    #pulls data from xml and adds to above lists
    for item in e[0][0][0][0].text.split(' '):
        pointsTemp.append(float(item))
    for item in e[0][0][1][0].text.split(' '):
        connectivityTemp.append(item)
    for item in e[0][0][1][1].text.split(' '):
        offsetsTemp.append(item)
    for item in e[0][0][1][2].text.split(' '):
        centresTemp.append(float(item))
    for item in e[0][0][1][3].text.split(' '):
        normalsTemp.append(float(item))
    for item in e[0][0][2][0].text.split(' '):
        valTemp.append(float(item))

    # creates polygon points
    i = 0
    while (i<len(pointsTemp)):
        x=pointsTemp[i]
        y=pointsTemp[i+1]
        z=pointsTemp[i+2]
        allpoints.append(Point(i//3,x,y,z))
        i+=3

    # reformat offsets to individual point groups
    for i in range(len(offsetsTemp)-1):
        if i==0:
            offsetsTemp2.append(int(offsetsTemp[i]))
        else:
            offsetsTemp2.append(int(offsetsTemp[i])-int(offsetsTemp[i-1]))
    # print(offsetsTemp2)

    # create polygon by assigning points according to connectivity
    last_index=0
    n=0
    for item in offsetsTemp2:
        poly_points=()
        for i in range(item):
            poly_points=poly_points+(connectivityTemp[last_index+i],)
        polygons.append(Polygon(allpoints,poly_points,centresTemp[n],normalsTemp[n],valTemp[n]))
        n+=1
        last_index+=item

    for polygon in polygons:
        total_area+=polygon.area
        if polygon.val > value:
            area_over+=polygon.area

    print('Completed: '+name+' for area over: '+str(value) +' '+ evalType)

    # write to file
    fout.write("\n{},{},{}".format(name,str(area_over),str(round((area_over/total_area)*100,4))+'%'))

    # update total areas for overall area calculation
    global totalArea, totalOver
    totalArea+=total_area
    totalOver+=area_over

"""
Run Script
"""

# open file for writing
fout = open(foutName,'w')
fout.write("Illuminance Results")

# run
for value in minVal:
    fout.write("\n\nGrid,Area,% Over "+str(value)+" "+evalType)
    for object in files:
        loadData(os.path.join(folder, object),object,value,evalType)
    fout.write('\n\nTotal % Area, '+str(round(totalOver))+','+str(round((totalOver/totalArea)*100,4))+'%')
fout.close()
print('Complete, file written: '+outputname)