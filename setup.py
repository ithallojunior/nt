import sys, os

def run():
    try:
        option = sys.argv[1]
        with open("configs", "r") as f:
            settings = eval(f.read())
        
        npath = os.path.join(os.getcwd(), settings["PATH"])
        settings.update({"PATH": npath})

        #adding / to the end
        if (settings["PATH"][-1] != "/" ):
            npath = settings["PATH"] + "/"
            settings.update({"PATH":npath})
        
        if ((option=="install") or (option=="full_install")):
            
            print("Modifying file")
            
            with open("nt.py", "r") as f:
                text = f.read()
            
            for i in settings.keys():
                text = text.replace(i, settings[i])
            
            print("Installing to '%s'"%settings["PATH"])
           
            try:
                with open(settings["PATH"]+"nt.py" ,"w") as f:
                    f.write(text)
                    f.flush()
            except IOError:
                print("Ops! Check the path")
                #os.makedirs(settings["PATH"])
                return
            
            if (option=="full_install"):
                try:
                    with open(settings["RC_PATH"] ,"a") as f:
                        f.write("\n#added by nt \nalias nt='python %s' \n"%(settings["PATH"]+"nt.py"))
                    print("alias added to '%s'"%settings["RC_PATH"])
                except IOError:
                    print("Ops! Check the RC path")
                    return
            print("Installed")
        else:
         print("Not installed, use python setup.py install or python setup.py full_install")
    except IndexError:
         print("Not installed, use python setup.py install or python setup.py full_install")
    
if __name__=="__main__":
    run()    
