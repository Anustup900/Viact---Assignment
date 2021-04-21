import sys
import json
import getClassDescription as gd
import argparse


def breadcrumb(json_dict_or_list, value):
  if json_dict_or_list == value:
    return [json_dict_or_list]
  elif isinstance(json_dict_or_list, dict):
    for k, v in json_dict_or_list.items():
      p = breadcrumb(v, value)
      if p:
        return [k] + p
  elif isinstance(json_dict_or_list, list):
    lst = json_dict_or_list
    for i in range(len(lst)):
      p = breadcrumb(lst[i], value)
      if p:
        return [i] + p

def get_hierarchy(json_dict, value):

    if json_dict == value:
        
        return [json_dict]
    elif isinstance(json_dict, dict):
        
        class_name = json_dict["LabelName"]
        
        for k, v in json_dict.items():
            #k1 = json_dict["LabelName"]
            
            p = get_hierarchy(v, value)
            if p:
                k = class_name
                return [k] + p
    elif isinstance(json_dict, list):
        #class_name = json_dict["LabelName"]
        lst = json_dict
        for i in range(len(lst)):
            p = get_hierarchy(lst[i], value)
            if p:
                
                return p
                #return [str(i)] + p

def get_siblings(data,keys_list):
   
    #delete the class name and "LabelName" from list
    #to get the subcategory
    keys_list.reverse()
    ind = keys_list.index("Subcategory")
    keys_list.reverse()
    keys_list = keys_list[0:-ind]
    
    #print (keys_list)
    #get sibling class names
    siblings_list = data
    for i in keys_list:
        siblings_list = siblings_list[i]
    #print (siblings_list)
    #print (hierarchy_list)
    siblings_list = [i["LabelName"] for i in siblings_list]
    return siblings_list

def main():
    
    
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--jsonfile", required=True,default="bbox_labels_600_hierarchy.json",
      help="path to input json file")
    ap.add_argument("-d", "--descriptions", type=str, default="oidv6-class-descriptions.csv",
      help="path to output loss/accuracy plot")
    ap.add_argument("-c", "--classname", type=str,
      help="class name")
    args = vars(ap.parse_args())

    #path to data
    #json_file = "bbox_labels_600_hierarchy.json"
    #class_desc_file = "oidv6-class-descriptions.csv"
    #class_name = "Sargassumfish"

    json_file = args["jsonfile"]
    class_desc_file = args["descriptions"]
    class_name = args["classname"]

    print ("\n\n-------START-----------\n\n")
    print ("Looking for " + class_name + "in the labels file\n")

    #get the code from class descriptions.csv
    class_label = gd.get_code(class_name,class_desc_file)
    
    if class_label is None:
      print (class_name + "is not present in the description file\n")
      return
    #read the json file
    with open(json_file) as f:
        data = json.load(f)
    
    
    print ("Looking for " + class_name + "in the json file\n")

    #return the hierarchy 
    hierarchy_list = get_hierarchy(data,class_label)
    

    if hierarchy_list == None:
      print (class_name + " is not present in " + json_file + "\n")
      return
    hierarchy_list = hierarchy_list[:-1]
    

    #return the key values to the given class name
    keys_list = breadcrumb(data,class_label)
    
    siblings_list = get_siblings(data,keys_list)
    
    
    siblings_list = [gd.get_name(i,class_desc_file) for i in siblings_list]
    hierarchy_list =[gd.get_name(i,class_desc_file) for i in hierarchy_list][1:]


    print ("==========siblings==============")
    for s,i in enumerate(siblings_list):
      print (" "  + str(s) +"   " + i)
    print ("========= hierarchy tree ========= ")

    for i in hierarchy_list:
      print ("   "+i)
      print ("     |       ")
      print ("     |       ")
      print ("     \/       ")

    print ("--------END--------\n")
if __name__ == "__main__":
    main()