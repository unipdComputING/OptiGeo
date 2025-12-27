from re import match
import pandas as pd
import numpy as np

def read_main_file(path):
    dfnode = pd.DataFrame(columns = ["name","id", "x", "y", "z", "dof x", "dof y", "dof z", "fix x", "fix y", "fix z", "load x", "load y", "load z", "type elem", "id elem"])
    dftetra = pd.DataFrame(columns = ["name","id", "x", "y", "z", "prop", "N1", "N2", "N3", "N4"])
    dfhexa = pd.DataFrame(columns = ["name","id", "x", "y", "z", "prop", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"])
    dfprops = pd.DataFrame(columns = ["name", "id", "Modulus", "Poisson", "Density"])
    f = open(path)
    #content = f.readlines()
    content = [r.split() for r in f.readlines()]
    i = 0
    j = 0
    k = 0
    z = 0
    m = 0
    mnodes = []
    mtetra = []
    mhexa = []
    mprops = []
    for item in content:
        match item[0]:
            case "N":
                dfnode.loc[i] = list(element for element in item)
                i += 1
                mnodes.append(m)
            case "T":
                dftetra.loc[j] = list(element for element in item)
                j += 1
                mtetra.append(m)
            case "H":
                dfhexa.loc[k] = list(element for element in item)
                k += 1
                mhexa.append(m)
            case "P":
                dfprops.loc[z] = list(element for element in item)
                z += 1
                mprops.append(m)
        m += 1
    f.close()
    return dfnode, dftetra, dfhexa, dfprops, mnodes, mtetra, mhexa, mprops

path = "stuff.txt"
dfnode, dftetra, dfhexa, dfprops, mnodes, mtetra, mhexa, mprops = read_main_file(path)