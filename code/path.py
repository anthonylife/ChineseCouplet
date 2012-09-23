#!/usr/bin/env python
#encoding=utf8

def AddSysPath(new_path):
    '''
    Add new directory path to  Python's sys.path
    Does not add the directory if it does not exist or if it's already on
    Return 1 if OK, -1 if new_path does not exist, 0 if it was already on sys.path
    '''
    import sys, os

    # Avoid adding nonexistent path
    if not os.path.exists(new_path):
        return -1

    # Standardize the path
    new_path = os.path.abspath(new_path)

    for x in sys.path:
        x = os.path.abspath(x)
        if new_path in (x, x+os.sep):
            return 0

    sys.path.append(new_path)

    return 1
