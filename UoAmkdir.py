#!/usr/bin/python3
import os
import sys

course = input("Course Name >>")
chapter = input("Chapter Name >>")
startwith = int(input("Start Number >>"))
endwith = int(input("End Number >>"))

os.mkdir(course)
os.chdir(course)
for num in range(startwith, endwith+1):
    os.mkdir(chapter+"{:02}".format(num))
