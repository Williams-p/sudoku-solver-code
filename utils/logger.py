# Logging mechanism

import sys, os, datetime

class Logger(object) :
    def __init__(self, level, toscreen) :
        self.loglevel = level # Int value
        self.toscreen = toscreen # Boolean; true if user wants the log on-screen
        if not self.toscreen : # Write to file? Initialize it.
            now = datetime.datetime.now()
            self.logname = "logs/" + now.strftime("%Y-%m-%d %H:%M") + ".log"
            self.outfile = open(self.logname, 'w')
        if self.loglevel > 5 : # Me being pedantic...
            message = "[WARN]: Log level set greater than maximum value (5)."
            message += " Setting level to 5."
            self.log(message, 2)
            self.loglevel = 5
        message = "[INFO]: Logger initialized at level " + repr(level) + "."
        self.log(message, 3)

    def __del__(self) :
        message = "[INFO]: Logger destructor called.\n"
        self.log(message, 3)

    def log(self, message, msg_level) :
        if self.toscreen :
            if msg_level <= self.loglevel :
                print message

        if not self.toscreen :
            if msg_level == 1 : # Always put errors on screen
                print message
            if self.loglevel > 0 and msg_level <= self.loglevel :
                message += "\n"
                try : # Guess and check method closes file: test to see if open
                    self.outfile.write(message) 
                except ValueError :
                    self.outfile = open(self.logname, 'wa')
                    self.outfile.write(message)
