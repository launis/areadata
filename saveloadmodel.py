def save_obj(obj, filename, Verbose = True):

    import pickle

    if Verbose:   
        print('Save model filename ', filename)
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename, Verbose = True):

    import pickle
    import os

    if os.access(filename, os.R_OK):
        if Verbose:
            print('Load model filename ', filename)      
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return(None)
