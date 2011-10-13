from __future__ import absolute_import

"""
Nothing here but dictionaries for generating LinearSegmentedColormaps,
and a dictionary of these dictionaries.
"""

import numpy as np
import matplotlib.colors as colors

# FIXME: Give me a proper name.
def _mkx(i, steps, n):
    """ Generate list according to pattern of g0 and b0. """
    x = []
    for step in steps:
        x.extend(range(i, step + n, n))
        i = step + (n - 1)
    return x

def padfr(lst, len_, pad=0):
    """ Pad lst to contain at least len_ items by adding pad to the front. """
    diff = len_ - len(lst)
    diff = 0 if diff < 0 else diff
    return [pad] * diff + lst

def paden(lst, len_, pad=0):
    """ Pad lst to contain at least len_ items by adding pad to the end. """
    diff = len_ - len(lst)
    diff = 0 if diff < 0 else diff
    return lst + [pad] * diff


# The following values describe color table 3 for IDL (Red Temperature)
r0 = np.array(paden([0,1,2,4,5,7,8,10,11,13,14,15,17,18,20,21,23,24,26,27,28,30,31,33,34,36,37,39,40,42,43,44,46,47,49,50,52,53,55,56,57,59,60,62,63,65,66,68,69,70,72,73,75,76,78,79,81,82,84,85,86,88,89,91,92,94,95,97,98,99,101,102,104,105,107,108,110,111,113,114,115,117,118,120,121,123,124,126,127,128,130,131,133,134,136,137,139,140,141,143,144,146,147,149,150,152,153,155,156,157,159,160,162,163,165,166,168,169,170,172,173,175,176,178,179,181,182,184,185,186,188,189,191,192,194,195,197,198,199,201,202,204,205,207,208,210,211,212,214,215,217,218,220,221,223,224,226,227,228,230,231,233,234,236,237,239,240,241,243,244,246,247,249,250,252,253], 256, 255))
g0 = np.array(padfr(_mkx(1, xrange(17, 256, 17), 2), 256))
b0 = np.array(padfr(_mkx(3, xrange(51, 256, 51), 4), 256))
    
c0 = np.arange(256, dtype='f')
c1 = (np.sqrt(c0) * np.sqrt(255.0)).astype('f')
c2 = (np.arange(256)**2 / 255.0).astype('f')
c3 = ((c1 + c2/2.0) * 255.0 / (c1.max() + c2.max()/2.0)).astype('f')

def aia_color_table(wavelength):
    '''Returns one of the fundamental color tables for SDO AIA images.
       Based on aia_lct.pro part of SDO/AIA on SSWIDL written by Karl Schriver (2010/04/12).
    '''
    try:
        r, g, b = {
            1600: (c3, c3, c2), 1700: (c1, c0, c0), 4500: (c0, c0, b0/2.0),
            94: (c2, c3, c0), 131: (g0, r0, r0), 171: (r0, c0, b0),
            193: (c1, c0, c2), 211: (c1, c0, c3), 304: (r0, g0, b0),
            335: (c2, c0, c1)
        }[wavelength]
    except KeyError:
        raise ValueError(
            "Invalid AIA wavelength. Valid values are "
            "1600,1700,4500,94,131,171,193,211,304,335."
        )
   
    # Now create the color tuples
    i = np.linspace(0, 1, r0.size)
    
    cdict = dict(
        (name, list(zip(i, el/255.0, el/255.0)))
        for el, name in [(r, 'red'),  (g, 'green'), (b, 'blue')]
    )
    
    return colors.LinearSegmentedColormap('mytable', cdict)

eit_yellow_r = np.array([0,1,2,3,5,6,7,8,10,11,12,14,15,16,17,19,20,21,22,24,25,26,28,29,30,31,33,34,35,36
,38,39,40,42,43,44,45,47,48,49,51,52,53,54,56,57,58,59,61,62,63,65,66,67,68,70,71,72,73,75
,76,77,79,80,81,82,84,85,86,87,89,90,91,93,94,95,96,98,99,100,102,103,104,105,107,108,109,110,112,113
,114,116,117,118,119,121,122,123,124,126,127,128,130,131,132,133,135,136,137,138,140,141,142,144,145,146,147,149,150,151
,153,154,155,156,158,159,160,161,163,164,165,167,168,169,170,172,173,174,175,177,178,179,181,182,183,184,186,187,188,189
,191,192,193,195,196,197,198,200,201,202,204,205,206,207,209,210,211,212,214,215,216,218,219,220,221,223,224,225,226,228
,229,230,232,233,234,235,237,238,239,240,242,243,244,246,247,248,249,251,252,253,255,255,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])

eit_yellow_g = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29
,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60
,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,82,83,84,85,86,87,88,89,90,91
,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121
,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152
,153,154,155,156,157,158,159,160,161,162,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183
,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,205,206,206,207,209,209,210,210,212,213
,213,215,216,216,218,219,219,221,221,222,224,224,225,227,227,228,230,230,231,231,232,234,234,235,237,237,238,240,240,241
,241,243,244,244,246,247,247,249,250,250,252,252,253,255,255,255])

eit_yellow_b = np.concatenate((np.zeros(201).astype('int'), np.array([7,7,15,22,22,30,30,37,45
,45,52,60,60,67,75,75,82,82,90,97,97,105,112,112,120,127,127,135,135,142,150,150,157,165,165,172,180,180,187
,187,195,202,202,210,217,217,225,232,232,240,240,247,255,255,255])))
 
eit_dark_blue_r = np.concatenate((np.zeros(206).astype('int'), np.array([9,13,21,25
,25,29,33,41,49,53,57,65,69,73,77,77,85,94,98,102,110,114,118,122,134,134,138,142,146,154,158,162,166,179
,183,183,187,191,199,203,207,215,223,227,231,231,235,243,247,255])))

eit_dark_blue_g = np.concatenate((np.zeros(128).astype('int'), np.array([2,2,4,5,7,12,13,15,17,20,21,21,23,25,29,31,33,34,37,39,41,41
,44,47,49,50,52,55,57,60,61,61,65,66,68,69,73,76,77,79,82,82,84,85,87,92,94,95,97,100,102,103
,103,105,110,111,113,114,118,119,121,122,122,127,129,130,132,135,137,138,142,145,145,146,148,150,153,154,158,159,162,164
,164,166,167,170,174,175,177,180,182,183,185,185,188,191,193,195,198,199,201,203,207,207,209,211,212,215,217,219,220,225
,227,227,228,230,233,235,236,239,243,244,246,246,247,251,252,255])))

eit_dark_blue_b = np.concatenate((np.zeros(52).astype('int'), np.array([1,4,5,6,8,8,10,12
,14,16,18,20,21,23,25,25,28,29,31,33,35,36,37,42,43,43,44,46,48,50,51,52,56,58,59,61,61,63
,65,66,69,71,73,74,75,78,78,80,81,84,86,88,89,90,93,94,94,97,99,101,103,104,105,108,111,112,112,113
,116,118,119,120,124,126,127,128,131,131,132,134,135,139,141,142,143,146,147,147,149,150,154,155,157,158,161,162,164,164
,166,169,170,172,173,176,177,180,181,181,184,185,187,188,191,193,195,196,199,199,200,202,203,207,208,210,211,214,215,217
,217,218,222,223,225,226,229,230,231,233,233,237,238,240,241,244,245,246,249,252,252,253,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])))

eit_dark_green_r = np.concatenate((np.zeros(130).astype('int'), np.array([1,3,4,9,11,12,14,17,19,19,20,22,27,29,30,32,35,37,38,38
,41,45,46,48,50,53,54,58,59,59,62,64,66,67,71,74,75,77,80,80,82,83,85,90,91,93,95,98,100,101
,101,103,108,109,111,112,116,117,119,121,121,125,127,129,130,133,135,137,140,143,143,145,146,148,151,153,156,158,161,163
,163,164,166,169,172,174,175,179,180,182,183,183,187,190,192,193,196,198,200,201,206,206,208,209,211,214,216,217,219,224
,225,225,227,229,232,234,235,238,242,243,245,245,246,250,251,255])))

eit_dark_green_g = np.concatenate((np.zeros(52).astype('int'), np.array([1,3,4,5,6,6,8,9
,11,12,14,15,16,17,19,19,21,22,23,25,26,27,28,31,32,32,33,34,36,37,38,39,42,43,44,45,45,47
,48,49,51,53,54,55,56,58,58,59,60,62,64,65,66,67,69,70,70,72,73,75,76,77,78,80,82,83,83,84
,86,87,88,89,92,93,94,95,97,97,98,99,100,103,104,105,106,108,109,109,110,111,114,115,116,117,119,120,121,121
,123,125,126,127,128,130,131,133,134,134,136,137,138,139,141,143,144,145,147,147,148,149,150,153,154,155,156,158,159,160
,160,161,164,165,166,167,169,170,171,172,172,175,176,177,178,180,181,182,184,186,186,187,188,189,191,192,194,195,197,198
,198,199,200,202,204,205,206,208,209,210,211,211,213,215,216,217,219,220,221,222,225,225,226,227,228,230,231,232,233,236
,237,237,238,239,241,242,243,245,247,248,249,249,250,252,253,255])))

eit_dark_green_b = np.concatenate((np.zeros(197).astype('int'), np.array([3,10,17,17,20,24,27,34,37,44,48,55,58
,58,62,65,72,79,82,86,93,96,99,103,103,110,117,120,124,130,134,137,141,151,151,155,158,161,168,172,175,179,189
,192,192,196,199,206,210,213,220,227,230,234,234,237,244,248,255])))

eit_dark_red_r = np.concatenate((np.zeros(52).astype('int'), np.array([1,4,5,7,8,8,11,13
,15,17,20,21,23,24,27,27,30,31,33,36,37,39,40,44,46,46,47,49,52,53,55,56,60,62,63,65,65,68
,69,70,73,76,78,79,81,84,84,85,86,89,92,94,95,97,99,101,101,104,105,108,110,111,113,115,118,120,120,121
,124,126,127,128,133,134,136,137,140,140,141,143,144,149,150,152,153,156,157,157,159,160,165,166,168,169,172,173,175,175
,178,181,182,184,185,188,189,192,194,194,197,198,199,201,204,207,208,210,212,212,214,215,217,221,223,224,226,228,230,231
,231,233,237,239,240,241,244,246,247,249,249,253,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])))

eit_dark_red_g = np.concatenate((np.zeros(148).astype('int'), np.array([1,1
,5,9,11,13,15,18,20,24,26,26,30,32,34,35,39,43,45,47,51,51,52,54,56,62,64,66,68,71,73,75
,75,77,83,85,86,88,92,94,96,98,98,103,105,107,109,113,115,117,120,124,124,126,128,130,134,136,139,141,145,147
,147,149,151,154,158,160,162,166,168,170,171,171,175,179,181,183,187,188,190,192,198,198,200,202,204,207,209,211,213,219
,221,221,222,224,228,230,232,236,239,241,243,243,245,249,251,255])))

eit_dark_red_b = np.concatenate((np.zeros(204).astype('int'), np.array([3,7,15,19,27,31
,31,35,39,47,54,58,62,70,74,78,82,82,90,98,102,105,113,117,121,125,137,137,141,145,149,156,160,164,168,180
,184,184,188,192,200,204,207,215,223,227,231,231,235,243,247,255])))

def eit_color_table(wavelength):
    '''Returns one of the fundamental color tables for SOHO EIT images.'''
    # SOHO EIT Color tables
    # EIT 171 IDL Name EIT Dark Bot Blue
    # EIT 195 IDL Name EIT Dark Bot Green
    # EIT 284 IDL Name EIT Dark Bot Yellow
    # EIT 304 IDL Name EIT Dark Bot Red
    try:
        r, g, b = {
            171: (eit_dark_blue_r, eit_dark_blue_g, eit_dark_blue_b), 
            195: (eit_dark_green_r, eit_dark_green_g, eit_dark_green_b), 
            284: (eit_yellow_r, eit_yellow_g, eit_yellow_b),
            304: (eit_dark_red_r, eit_dark_red_g, eit_dark_red_b)
        }[wavelength]
    except KeyError:
        raise ValueError(
            "Invalid EIT wavelength. Valid values are "
            "171, 195, 284, 304."
        )

    # Now create the color tuples
    i = np.linspace(0, 1, r0.size)
    
    cdict = dict(
        (name, list(zip(i, el/255.0, el/255.0)))
        for el, name in [(r, 'red'),  (g, 'green'), (b, 'blue')]
    )
    
    return colors.LinearSegmentedColormap('mytable', cdict)