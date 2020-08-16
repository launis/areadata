def set_path(apppath):
    import os

    if os.path.exists(apppath):
        if os.getcwd() != apppath:
            os.chdir(apppath)
    mainpath = os.getcwd()
    path = os.path.join(mainpath, "data")

    if not os.path.exists(path):
        os.mkdir(path)
    return(mainpath, path)
