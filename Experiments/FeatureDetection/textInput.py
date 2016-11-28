import sys,os


message = ''
while message != 'wq':
    message = raw_input('Here we go:\n')
    if message == "Hello":
        print "Good job"
    elif message == "Toto":
        print "Version 2"

