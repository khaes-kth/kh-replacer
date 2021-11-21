import sys
import os


def main(argv):
    line = input()
    print('NAME,LINE_START,LINE_END,COLUMN_START,COLUMN_END,ABS_PATH,VALUE,PARENT_LINE_START,PARENT_LINE_END,PARENT_COLUMN_START,PARENT_COLUMN_END,PARENT_NAME,VISIBILITY')
    while (line):
        parts = line.split(",")
        ind = 0
        name = parts[ind]
        ind += 1
        if '\"' in parts[1]:
            ls = parts[1].replace('\"', "")
            cs = parts[2]
            le = parts[3]
            ce = parts[4].replace('\"', "")
            ind += 4
        else:
            ls = cs = le = ce = 'null'
            ind += 1
        pname = parts[ind]
        ind += 1
        if '\"' in parts[ind]:
            pls = parts[ind].replace('\"', "")
            pcs = parts[ind + 1]
            ple = parts[ind + 2]
            pce = parts[ind + 3].replace('\"', "")
            ind += 4
        else:
            pls = pcs = ple = pce = 'null'
            ind += 1
        val = parts[ind]
        ind += 1
        abs_path = parts[ind]
        ind += 1
        if 'visibility=public' in parts[ind]:
            vis = 'public'
        elif 'visibility=private' in parts[ind]:
            vis = 'private'
        elif 'visibility=protected' in parts[ind]:
            vis = 'protected'
        else:
            vis = 'null'
        ind += 1
        print(f'{name},{ls},{le},{cs},{ce},{abs_path},{val},{pls},{ple},{pcs},{pce},{pname},{vis}')
        try:
            line = input()
        except:
            break

if __name__ == "__main__":
    main(sys.argv[1:])
