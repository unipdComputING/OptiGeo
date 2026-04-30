import pandas as pd
import re

def get_variable_name(var, namespace):
    return [name for name, value in namespace.items() if value is var]

def write_the_file(filename, globalproperties, nodes, beams, tetra, hexa, properties, solvers):
    combined_list = [globalproperties, nodes, beams, tetra, hexa, properties, solvers]
    mega_list = []
    for item in combined_list:
        item_name = get_variable_name(item, locals())[0]
        match item_name:
            case "nodes":
                mega_list.append(["#start"+item_name])
                mega_list.append([item_name.upper() +"    "+str(len(item))])
                coords = nodes[["id", "x", "y", "z"]].copy()
                dofs = nodes[["id", "dof x", "dof y", "dof z"]].copy()
                fix = nodes[["id", "fix x", "fix y", "fix z"]].copy()
                load = nodes[["id", "load x", "load y", "load z"]].copy()
                mini_list = []
                for df in [coords, dofs, fix, load]:
                    mini_list.append([name for name in df.columns])
                    for i in range(len(df)):
                        mini_list.append(df.iloc[i].tolist())
                larghezze = [max(len(str(riga[i])) for riga in mini_list) for i in range(len(mini_list[0]))]
                for element in mini_list:
                        mega_list.append([" | ".join(str(cell).ljust(larghezze[i]) for i, cell in enumerate(element))])
            case _:
                mini_list = []
                mega_list.append(["#start"+item_name])
                mega_list.append([item_name.upper() +"    "+str(len(item))])
                mini_list.append([name for name in item.columns])
                if len(item) > 0:
                    for i in range(len(item)):
                        mini_list.append(item.iloc[i].tolist())
                    larghezze = [max(len(str(riga[i])) for riga in mini_list) for i in range(len(mini_list[0]))]
                    for element in mini_list:
                        mega_list.append([" | ".join(str(cell).ljust(larghezze[i]) for i, cell in enumerate(element))])
        
        with open(filename, "w") as file:
            for line in mega_list:
                file.write(line[0]+"\n")
        file.close()


     