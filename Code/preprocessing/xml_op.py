from lxml import etree
from timer_deco import timer

def create_new_macro(xml_path, macro_data):
    print(xml_path)
    print(macro_data)
    # create Root node
    root = etree.Element("NUK-Macro")

    # store the amount of different macro_branches 
    global_amount = etree.SubElement(root, "global_amount", type="metadata", amount=str(len(macro_data)))

    # create macro_branch root node
    macro_branch = etree.SubElement(root, "branch", type="branch")
    
    # create file Element
    file_branch = etree.SubElement(macro_branch, "element", type="element", dummy_macro_file=macro_data[0]["dummy_macro_file"], seed_file=macro_data[0]["seed_file"], output_location=macro_data[0]["output_location"])

    # create split Element
    split_branch = etree.SubElement(macro_branch, "element", type="element", split_amount=macro_data[1]["split_amount"], particle_amount=macro_data[1]["particle_amount"])

    # create hardware Element
    hardware_branch = etree.SubElement(macro_branch, "element", type="element", cores=macro_data[2]["cores"], ram=macro_data[2]["ram"])

    # create dimension Element
    dimension_branch = etree.SubElement(macro_branch, "element", type="element", dim_x=macro_data[3]["dim_x"], dim_y=macro_data[3]["dim_y"], dim_z=macro_data[3]["dim_z"])

    # create size Element
    size_branch = etree.SubElement(macro_branch, "element", type="element", size_x=macro_data[4]["size_x"], size_y=macro_data[4]["size_y"], size_z=macro_data[4]["size_z"])

    # write the XML file
    tree = etree.ElementTree(root)
    tree.write(xml_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')


@timer
def read_macro_data(xml_path):
    # Parse the XML file
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # Initialize the structure to hold the extracted data
    macro_data = []

    # Read the macro branches
    for branch in root.findall('branch'):
        file_data = {
            "dummy_macro_file": branch.find("element[@type='element'][1]").get("dummy_macro_file"),
            "seed_file": branch.find("element[@type='element'][1]").get("seed_file"),
            "output_location": branch.find("element[@type='element'][1]").get("output_location")
        }

        split_data = {
            "split_amount": branch.find("element[@type='element'][2]").get("split_amount"),
            "particle_amount": branch.find("element[@type='element'][2]").get("particle_amount")
        }

        hardware_data = {
            "cores": branch.find("element[@type='element'][3]").get("cores"),
            "ram": branch.find("element[@type='element'][3]").get("ram")
        }

        dimension_data = {
            "dim_x": branch.find("element[@type='element'][4]").get("dim_x"),
            "dim_y": branch.find("element[@type='element'][4]").get("dim_y"),
            "dim_z": branch.find("element[@type='element'][4]").get("dim_z")
        }

        size_data = {
            "size_x": branch.find("element[@type='element'][5]").get("size_x"),
            "size_y": branch.find("element[@type='element'][5]").get("size_y"),
            "size_z": branch.find("element[@type='element'][5]").get("size_z")
        }
        
        macro_data = ([file_data, split_data, hardware_data, dimension_data, size_data])
    
    return macro_data
