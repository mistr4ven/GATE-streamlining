from lxml import etree

def create_new_macro(xml_path, macro_data):
    # create Root node
    root = etree.Element("NUK-Macro")

    # store the amount of different macro_branches 
    global_amount = etree.SubElement(root, "global_amount", type="metadata", amount=str(len(macro_data)))

    # for each macro_branch
    for arg_list in macro_data:
        # create macro_branch root node
        macro_branch = etree.SubElement(root, "branch", type="branch")
        
        # create transform Element
        transform = etree.SubElement(macro_branch, "element", type="element", input_file=arg_list[0]["Transform_input_file"], opfile=arg_list[0]["Transform_operations_file"], output_file=arg_list[0]["Transform_output_file"])

        # create math Element
        math = etree.SubElement(macro_branch, "element", type="element", input_file=arg_list[1]["Math_input_file"], opfile=arg_list[1]["Math_operations_file"], output_file=arg_list[1]["Math_output_file"])
    
    # write the XML file
    tree = etree.ElementTree(root)
    tree.write(xml_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')



def read_macro_data(xml_path):
    # Parse the XML file
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # Initialize the structure to hold the extracted data
    macro_data = []

    # Read the macro branches
    for branch in root.findall('branch'):
        transform_data = {
            "Transform_input_file": branch.find("element[@type='element'][1]").get("input_file"),
            "Transform_operations_file": branch.find("element[@type='element'][1]").get("opfile"),
            "Transform_output_file": branch.find("element[@type='element'][1]").get("output_file")
        }
        
        math_data = {
            "Math_input_file": branch.find("element[@type='element'][2]").get("input_file"),
            "Math_operations_file": branch.find("element[@type='element'][2]").get("opfile"),
            "Math_output_file": branch.find("element[@type='element'][2]").get("output_file")
        }

        macro_data.append([transform_data, math_data])
    
    return macro_data
