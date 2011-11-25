# Brief instructions for tesvsavedump

WHAT IS THIS?
tesvsavedump will decode a TESV: Skyrim game save file and dump into
a more human friendly format.
WARNING: Not all the fields are decoded and you may run into a lot of hex code
         I suppose you can read it :)

REQUISITES:
    . python 2.7.2
    
INSTALLATION:
    Copy/Extract data.py and save_file.py into a directory of your choice
    
USAGE:
    Open a terminal/command prompt and cd to the installation directory
    e.g cd C:\tesvsavedump
    e.g cd ~/tesvsavedump
    
    run the following:
    > python save_file.py [path_to_save_file]
    
    the program will dump the file to the console, if you want to dump into
    a file do:
    
    > python save_file.py [path_to_save_file] > [path_to_dump_file]
    
CONTRIBUTIONS:
If you can decode/reverse engineer any of the fields please do so and modify 
the code, or tell me how to do it.
You can open an issue here on github to contact me.