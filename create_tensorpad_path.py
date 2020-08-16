
def create_tensorpad_path(mainpath):

    import datetime
    import shutil 
    import os



    if os.path.exists(mainpath):
        if os.getcwd() != mainpath:
            os.chdir(mainpath)

    path = os.getcwd()


    log_path = os.path.join(path, "logs")
    log_path = os.path.join(log_path, "fit")


    if os.path.exists(log_path):
        with os.scandir(log_path) as entries:
            for entry in entries:
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
    else:
        os.mkdir(log_path)
        os.chdir(log_path)
        os.mkdir("fit")
        log_path = os.getcwd()
    
    if os.getcwd() != log_path:
        os.chdir(log_path)
    log_dir = os.path.join(log_path, "logs" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    os.chdir(mainpath)
    return(log_path, log_dir)