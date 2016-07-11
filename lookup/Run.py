'''
Created on May 17, 2016

@author: Shauryadeep Chaudhuri
'''
import os

from server.Launcher import Launcher


if __name__ == '__main__':
    configPath = os.path.join(os.getcwd(), "config.cfg")
    launch = Launcher(configPath)
    launch.startServer()
