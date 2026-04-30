import pandas as pd
import re

### Allora, il workflow dovrebbe essere questo
# il file basic_input_file esiste sempre e da questo si parte per il resto dell programma
# quando ogni cambiamento viene memorizzato nei dataframe, e poi nel file
# quando si salva il file si sovrascrive tutto e lo si legge nuovamente
#dipende ovviamente se siamo dentro l'editor di testo o la tabella

def parse_input_file(file_path):

    with open(file_path, 'r') as f:
        content = f.readlines()

    line_at = 0
    n_nodes_subdivision = 4
    df_globalproperties = pd.DataFrame(columns=["name","value"])
    df_nodes = pd.DataFrame(columns = ["id", "x", "y", "z", "dof x", "dof y", "dof z", "fix x", "fix y", "fix z", "load x", "load y", "load z"])
    df_beams = pd.DataFrame(columns=["id", "NODE1", "NODE2"])
    df_tetra = pd.DataFrame(columns=["id", "NODE1", "NODE2", "NODE3", "NODE4"])
    df_hexa = pd.DataFrame(columns=["id", "NODE1", "NODE2", "NODE3", "NODE4","NODE5","NODE6", "NODE7", "NODE8"])
    ##################################################################################################################################################################################################
    df_properties = pd.DataFrame()
    df_solvers = pd.DataFrame()

    for line in content:
        if line == "#startglobalproperties\n":
            n_global_properties = int(content[line_at + 1].split()[1])
            for i in range(n_global_properties):
                #df_globalproperties.loc[i] = list(element.strip("\n") for element in content[line_at + 2 + i].split())
                df_globalproperties.loc[i] = content[line_at + 3 + i].replace("|", " ").split()
        elif line == "#startnodes\n":
            n_nodes = int(content[line_at + 1].split()[1])
            for i in range(n_nodes):
                k = 0
                single_node_list = []
                for j in range(n_nodes_subdivision):
                    new_line = content[line_at + 3 + n_nodes*j + i + k].replace("|"," ").split() #se si utilizza il file con COORDINATES; DOF e i rimanenti header allora bisogna cambiare 2 in 3 e k += 2
                    single_node_list += new_line
                    k += 1
                    print(new_line)
                    """
                    line_1 = content[n_nodes + 3 + n_nodes*0 + i].replace("|"," ").split()
                    line_2 = content[n_nodes + 5 + n_nodes*1 + i].replace("|"," ").split()
                    line_3 = content[n_nodes + 7 + n_nodes*2 + i].replace("|"," ").split()
                    line_4 = content[n_nodes + 9 + n_nodes*3 + i].replace("|"," ").split()
                    """
                single_node_list.pop(4)
                single_node_list.pop(7)
                single_node_list.pop(10)
                df_nodes.loc[i] = single_node_list
            
        elif line == "#starttetra\n":
            n_tetra = int(content[line_at + 1].split()[1])
            for i in range(n_tetra):
                df_tetra.loc[i] = content[line_at + 3 + i].replace("|", " ").split()
            
        elif line == "#starthexa\n":
            n_hexa = int(content[line_at + 1].split()[1])
            for i in range(n_hexa):
                df_hexa.loc[i] = content[line_at + 3 + i].replace("|", " ").split()
            # GMSH ha i meshatori con i file stl, iges... (meglio sat)
            # preprocessing nel GMSH e post processing nel vtk?
        elif line == "#startbeams\n":
            n_beams = int(content[line_at + 1].split()[1])
            for i in range(n_beams):
                df_beams.loc[i] = content[line_at + 3 + i].replace("|", " ").split()
        line_at += 1
    ##########################################################################################################################################################################################
    # return dataframes, number of element, number of properties, ...
    return df_globalproperties.copy(), df_nodes.copy(), df_beams.copy(), df_tetra.copy(), df_hexa.copy(), df_properties.copy(), df_solvers.copy()


#file_path = r"C:\Users\ad251\Programmi VSCode\Optigeo\OptiGeo-Dorozhkin\basic_input_file.txt"
#parse_input_file(file_path)

