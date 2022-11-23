from pickle import load

def read_pkl_lists(pkl_path):
    with open(pkl_path, 'rb') as f:
        dub_list = pickle.load(f)
    return dub_list
