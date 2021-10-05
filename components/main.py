import os
from colorama import Fore, Style


cmd_dic = {
    'load' : lambda path :load_file(path),
    'copy' : lambda to_path, from_path : from_write_to(to_path, from_path)
}

def load_template(template_path, des_path=""):
    if (txt_arr := load_file(template_path, as_lines=True)):

        for idx,line in enumerate(txt_arr):
            line_sep = line.split(sep=" ")
            line_sep = [i.replace("\n","") for i in line_sep if i not in ['','\n']]

            if len(line_sep) == 0: 
                continue

            cmd = line_sep[0].lower()

            if "#" in cmd:
                continue

            if cmd in list(cmd_dic.keys()) :
                cmd = line_sep.pop(0).lower()
                # if there is a command and a src and destination file
                if len(line_sep)>1:
                    from_path = line_sep.pop(0)
                    to_paths = line_sep

                    for to_path in to_paths:
                        to_path = os.path.join(des_path , to_path)
                        cmd_dic[cmd](to_path, from_path)

                else:
                    print(Fore.RED, f"\n Too few arguments in line : {Fore.BLUE}{idx} \n", Style.RESET_ALL)
            else:
                for path in line_sep:
                    path = os.path.join(des_path, path)
                    write_to(path=path, text='')

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_to(path, text):
    if path == '' or path is None:
        return

    # creates dir
    if (dir := os.path.split(path)[0]) != '':
        create_dir(dir)
    
    # we can't retutn before creating a directory 
    if os.path.split(path)[1] == "":
        return

    try :
        with open(path, 'w') as f:
            f.write(text)
            print(Fore.GREEN, "\n----Success----\n", Style.RESET_ALL)
    except :
        print(Fore.RED,"\nSomething Went Wrong... maybe path is wrong\n", Style.RESET_ALL)

def load_file(path, as_lines=False):

    if path is None:
        return False

    if not os.path.exists(path):
        print(Fore.RED, f"\n {path} File doesn't exist\n", Style.RESET_ALL)
        return False

    try :
        with open(path, 'r') as f:
            if as_lines:
                return f.readlines()

            return f.read()
    except:
        print(Fore.RED,f"\n Can't read file from {path} \n", Style.RESET_ALL)
        return False

def from_write_to(to_path, from_path=None):
    
    if (txt := load_file(from_path)):
        try :
            write_to(path=to_path, text= txt)
        except:
            print(Fore.RED, f"\n Can't read from file from {from_path}\n", Style.RESET_ALL)


    elif from_path == '' or from_path is None:
        write_to(path=to_path, text='')

# load_template('cmds.template')
