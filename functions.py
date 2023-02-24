from AccessDatabase import AccessDB
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
AbsPathDir = script_dir + '/'
print(script_dir)
db = AccessDB(AbsPathDir + 'Database.accdb')

def ListGen(table, columns):
    res = []
    listofcl = db.get_colums_from_table(table, columns)
    for line in listofcl:
        curline = ''
        for i in line:
            curline = curline + str(i)
        res.append(curline)
    return res
