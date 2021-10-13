import matplotlib as mpl
import numpy as np


def GenerateColor(rating, vmin, vmax):
    """
    

    Parameters
    ----------
    rating : INT
        The value to generate a color for
    vmin : TYPE
        DESCRIPTION.
    vmax : TYPE
        DESCRIPTION.

    Returns
    -------
    light_state : TYPE
        DESCRIPTION.

    """
    # sample the colormaps that you want to use. Use 90% from RdYlGn_r and 10% from Plasma
    # colors in total
    
    cMap = []
    for value, colour in zip([0,30,40,60,70,80,100],["DarkGreen", "LightGreen", "Yellow", "Orange", "IndianRed", "DarkRed", "Purple"]):
        cMap.append((value/100.0, colour))

    cm = mpl.colors.LinearSegmentedColormap.from_list("custom", cMap)
    
    
    
    norm = mpl.colors.Normalize(vmin, vmax)
    convert = mpl.colors.rgb_to_hsv
    color = cm(norm(rating))
    
    hue, saturation, color_temp = convert(color[0:3])
    #hue, saturation, color_temp = color[0:3]
    
    
    light_state = {
            "hue": int(hue*360),
            "saturation": int(saturation*100),
            "brightness": int(color_temp*100),
        }
    
    return light_state