import csv


def get_code(class_name,file_loc):
  with open(file_loc,encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = []
    #print (csv_reader)
    for row in csv_reader:
      #print (row)
      rows.append(row)
  codes = [item[0] for item in rows]
  names = [item[1] for item in rows]
  #print (names[5])
  try:
    ind = names.index(class_name)

    return codes[ind]
  except:
    return class_name
  
def get_name(class_code,file_loc):
  with open(file_loc,encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rows = []
    #print (csv_reader)
    for row in csv_reader:
      #print (row)
      rows.append(row)
  codes = [item[0] for item in rows]
  names = [item[1] for item in rows]
  #print (names[5])
  try:
    ind = codes.index(class_code)
    return names[ind]
  except:
    return class_code