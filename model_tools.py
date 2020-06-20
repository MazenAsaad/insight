# Import libraries and functions
import numpy as np
import pandas as pd
from spotify_tools import *



# Turn popularity scores into classes based on percentile cutoffs
def pop_classes(pop_vals, cutoffs=[75]):
    # Check if the cutoffs is a single integer and not a list
    if isinstance(cutoffs,int):
        cutoffs = [cutoffs]
    
    # Convert popularity values to a numpy array (for speed)
    p = np.array(pop_vals)
    
    # Set each percentile chunk to a different class (in ranked order)
    classes = np.array([0]*len(p))
    for pct in cutoffs:
        c = np.where(p >= np.percentile(p,pct),1,0)
        classes = classes + c
    return classes