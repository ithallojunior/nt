#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:  Ithallo J. A. Guimarães
Note taking app
"""
import commands, tty, sys, termios, os
from subprocess import call
import colorama #colors
import time
class notes:

    def __init__(self): 
        #either edit it or use the setup
        self.notes_path = "PATH" + ".notes/"
        self.default_editor = "EDITOR"
        self.marker = colorama.Back.MARKER
        self.no_marker = colorama.Style.RESET_ALL

        self.file_to_edit = ""  
        self.cmd = ""
        self._position = 0
        self.files = []
    
    def _getchar(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        self.cmd = ch

    def _get_all_files(self): 
        #self.files = commands.getoutput(" ls %s"%self.notes_path).split()
        self.files = os.listdir(self.notes_path)
    def _clear(self):
        os.system(" clear")

    def _editor(self):
        call([self.default_editor, "%s%s"%(self.notes_path, self.file_to_edit)] )

    def _move_controller(self):
        if  (self.files == [] ):
            return # returns in case of no file
        else:
            if ((self.cmd=="j") and (self._position<len(self.files))):
                self._position += 1 #goes down the files
                if (self._position==len(self.files)):
                    self._position = 0

            elif ((self._position >= 0) and (self.cmd=="k")):
                self._position -= 1 #goes  up the files 
                if (self._position == -1):
                    self._position = len(self.files) - 1
            else:
                #delete
                if(self.cmd == "D"):
                    print("\nDelete %s? [y/N]"%self.files[self._position])
                    self._getchar()
                    if (self.cmd == "y"):
                        #os.system(" rm %s%s"%(self.notes_path, self.files[self._position]) )
                        os.remove(self.notes_path + self.files[self._position])
                        print("\n%s deleted!"%self.files[self._position])
                        time.sleep(1)
                        self._position = 0
                #open
                elif((self.cmd == "e") or (self.cmd == "l") ):
                    self.file_to_edit =  self.files[self._position]
                    self._editor()
                else:
                    pass
    
    def  run(self):
        self._clear()
        #get the new archive
        if (len(sys.argv)>1):
            if (sys.argv[1][0]=="-"):
                print("Kept for commands")
            else:
                self.file_to_edit = "".join(i + " " for i in sys.argv[1:])[:-1]    
                self._editor()
        
        #check for file path existence
        if (commands.getstatusoutput(" ls %s"%self.notes_path)[0] != 0):
            #commands.getoutput(" mkdir %s"%self.notes_path)
            os.mkdir(self.notes_path)
            print("Note path created")
        else:
            pass
        
        while(1):
            self._get_all_files()
            print(self.no_marker+"__________________________________________________________________")
            print(self.no_marker+"|N - new | D - delete | e/l - edit | q - quit | j - down | k - up|")
            print(self.no_marker+"|--------|------------|------------|----------|----------|-------|\n")
            if (self.files!=[]):
                for i in self.files:
                    try:
                        if (i==self.files[self._position]):
                            mark = self.marker
                        else:
                            mark = self.no_marker
                    except IndexError:
                        self._position = 0
                    
                    
                    #preview = commands.getoutput(' cat %s%s | awk "NR==1" '%(self.notes_path, i))
                    with open(self.notes_path + i, "r") as f:
                        preview = f.readline()

                    data = commands.getoutput(" ls -l %s%s"%(self.notes_path, i)).split()[5:8]
                    info = "".join(" " + j for j in data)
                    print("%s %s - %s : %s"%(mark, i, info, preview ) )
            else:
                print(self.no_marker+"                   ------No files yet------                    ")
            print(self.no_marker+"\n-----------------------------end---------------------------------") 
            #### commands
            self._getchar() 
            #to quit
            if (self.cmd == "q"):
                print("Quitting")
                time.sleep(0.5)
                self._clear()
                #TODO commit to git here
                break
            #new
            if(self.cmd == "N"):
                self.file_to_edit = raw_input("\nType the filename: ") #Python 3.x warning
                self._editor()
                self._position = 0
            
            self._move_controller()
            self._clear()
            
            

if __name__=="__main__":
    myNotes = notes()
    myNotes.run()

