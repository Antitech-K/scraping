import csv


with open('resault.csv', 'r', newline='') as file:

    re=csv.reader(file, dialect='excel', delimiter = ",")
    n_list =[]
    c = 0
    
    for i in re:
        if i != []:
            n_list.append (i)
        c +=1
for j in n_list:
    try:
        ps=str(j[1])
        j.pop(1)
        j.insert(1, ps[:6])   
    except:
        None

    try:
        ds=str(j[5])
        j.pop(5)
        j.insert(5, ds[:6])
    except:
        None

    try:
        ds=str(j[7])
        j.pop(7)
        j.insert(7, ds[:6])
    except:
        None
    if j == ['']:
        print ('ytttt')
        break
    
    ffile = open("resault_re.csv", "a")
    write=csv.writer(ffile, dialect='excel')
    write.writerow(j)
    ffile.close()     
    