import os
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter.colorchooser import askcolor

# from threading import Thread
class CustomText(Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        self.tags = [
                    # tagname       text color     background color
                    ("copy",        "#FF0287",      None ),
                    ("directory",   "#2185e8",      None ),
                    ("comment",     "#06d420",      None ),
                    ("src",         "#f6a440",      None ),
                    ("des"        , "#d000fa",      None ),
                    ("error",          None  ,      "#ffbbbb")
                ]
        self.configure_colors()

        self.bind("<<TextModified>>", self.update)
        
    def configure_colors(self):

        for tag, front_clr, back_clr in self.tags:
            self.tag_configure(tag,foreground=front_clr,background=back_clr)
    
    def change_clr(self,idx, Fore=None, back=None):
        for i,(tag, _, _) in enumerate(self.tags):
            if idx== tag:
                self.tags[i] = (tag, Fore, back)
        self.configure_colors()
    
    def change_text_clr(self,idx):
        clr = askcolor(title = f"Choose {idx} color")
        if clr == '' or clr is None:
            return
        print(idx)
        for i,(tag, _, back) in enumerate(self.tags):
            if idx== tag:
                self.tags[i] = (tag,clr[1],back)
                print(self.tags[i])
        self.configure_colors()
    
    def change_background_clr(self,idx):
        clr = askcolor(title = f"Choose {idx}'s background color")
        if clr == '' or clr is None:
            return
        for i,(tag, Fore, _) in enumerate(self.tags):
            if idx== tag:
                self.tags[i] = (tag,Fore, clr[1])
        self.configure_colors()


    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        try:
            result = self.tk.call(cmd)
        except:
            return
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

    def highlight_text(self, start, end, tag="copy"):
        # if no text is selected then tk.TclError exception occurs
        try:
            if start is not None and end is not None:
                self.tag_add(tag,start,end)

                # self.text.tag_add("copy", "sel.first", "sel.last")		
        except TclError:
            pass

    def clear(self):
        for tag, _,_ in self.tags:
            self.tag_remove(tag,"1.0","end")

    def update(self,e):
        self.clear()
        txt = self.get(1.0,END).split('\n')

        for line_cnt, line in enumerate(txt):
            word = ""
            word_count = 0
            idx = 0

            while(idx<len(line)):
                char = line[idx]
                word += char.lower()
                word_count += 1

                if char == "/":
                    self.highlight_text(start=f"{line_cnt+1}.{word_count-len(word)}", end=f"{line_cnt+1}.{word_count}", tag="directory")

                if char == "#":
                    self.highlight_text(start=f"{line_cnt+1}.{word_count-1}", end=f"{line_cnt+1}.end", tag="comment")
                    idx = len(line)

                if word == 'copy':
                    self.highlight_text(start=f"{line_cnt+1}.{word_count-4}", end=f"{line_cnt+1}.{word_count}", tag="copy")
                    # i = idx+1
                    idx += 1
                    while(idx<len(line) and (line[idx] in ['\n','\t',' '])):
                        idx +=1
                    while(idx < len(line) and not (line[idx] in ['\n','\t',' '])):
                        idx+=1
                    end_idx = idx
                    while(end_idx<len(line) and not(line[end_idx] == '#')):
                        end_idx += 1

                    self.highlight_text(start=f"{line_cnt+1}.{word_count}", end=f"{line_cnt+1}.{idx}", tag="src")
                    self.highlight_text(start=f"{line_cnt+1}.{idx+1}", end=f"{line_cnt+1}.{end_idx}", tag="des")


                idx += 1
                if char in [" ","\t"]:
                    word = ""


class FileManager():
    def __init__(self, root, text_box) -> None:
        self.open_file_name = False

        self.root, self.text_box = root, text_box
        
    def new_file(self):
        self.open_file_name = False
        self.text_box.delete("1.0",END)
        self.root.title("*New File")

    def open_file(self, path=None):
        text_file = askopenfilename(title="Open File", filetypes=[("Boilerplate File","*.bt")]) if path is None else path
        if text_file is None or text_file == "":
            return

        self.open_file_name = text_file

        self.text_box.delete("1.0",END)
        name = os.path.split(text_file)[1].split(".")[0]
        self.root.title(name)

        with open(text_file, "r") as f:
            self.text_box.insert(END,f.read())
            self.text_box.update(False)

    def save_as(self):
        text_file = asksaveasfilename(title= "Save File",defaultextension=".bt", filetypes=[("Boilerplate Files",".bt"),("Text Files",".txt")])
        if text_file:
            self.open_file_name = text_file

            name = os.path.split(text_file)[1].split(".")[0]
            self.root.title(name)
        
            with open(text_file, "w") as f:
                f.write(self.text_box.get(1.0, END))

    def save(self):
        print('save')
        if self.open_file_name:
            with open(self.open_file_name, "w") as f:
                f.write(self.text_box.get(1.0, END))
                self.root.title(os.path.split(self.open_file_name)[1].split(".")[0])
        else:
            self.save_as()


def text_editor(path=None):

    def config_keyboard_shortcuts():
        root.bind("<Control-Key-n>",lambda x: file_manager.new_file())
        root.bind("<Control-Key-s>",lambda x: file_manager.save())
        root.bind("<Control-Key-r>",lambda x: file_manager.open_file())
        root.bind("<Control-Shift-S>",lambda x: file_manager.save_as())
        root.bind("<Control-Key-q>",lambda x: close())

        root.bind("<Control-Key-x>", cut)
        root.bind("<Control-Key-c>", copy)
        # this is just a return value place holder not to run paste twice
        root.bind("<Control-Key-v>", lambda x : paste)
        root.bind("<Control-Key-k>", toggle_comment)
        root.bind("<Control-Key-a>", select_all)

    def config_file_menu():
        file_menu.add_command(label="New",accelerator="Ctrl+n",  command=file_manager.new_file)
        file_menu.add_command(label="Open",accelerator="Ctrl+o", command=file_manager.open_file)
        file_menu.add_command(label="Save",accelerator="Ctrl+s", command=file_manager.save)
        file_menu.add_command(label="SaveAs",accelerator="Ctrl+Shift+s", command=file_manager.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=close)
    
    def config_edit_menu():
        edit_menu.add_command(label="Cut           "  , accelerator="Ctrl+x" , command= lambda : cut(False) )
        edit_menu.add_command(label="Copy          " , accelerator="Ctrl+c" , command= lambda : copy(False) )
        edit_menu.add_command(label="Paste         ", accelerator="Ctrl+v" , command= lambda : paste(False) )
        edit_menu.add_command(label="Toggle Comment", accelerator="Ctrl+k" , command= lambda : toggle_comment(False) )
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo    " , accelerator="Ctrl+z" , command= lambda : text_box.edit_undo )
        edit_menu.add_command(label="Redo    " , accelerator="Ctrl+y" , command= lambda : text_box.edit_redo )
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All" , accelerator="Ctrl+a" , command= lambda : select_all(False) )
        edit_menu.add_command(label="Clear All" , command= lambda : clear(False) )
    
    def config_view_menu():
        view_menu.add_command(label=f"Change Copy Colour", command= lambda : text_box.change_text_clr('copy'))
        view_menu.add_command(label=f"Change Copy Background Colour", command= lambda: text_box.change_background_clr('copy'))
        view_menu.add_separator()

        view_menu.add_command(label=f"Change Directory Colour", command= lambda : text_box.change_text_clr('directory'))
        view_menu.add_command(label=f"Change Directory Background Colour", command= lambda: text_box.change_background_clr('directory'))
        view_menu.add_separator()

        view_menu.add_command(label=f"Change Comment Colour", command= lambda : text_box.change_text_clr('comment'))
        view_menu.add_command(label=f"Change Comment Background Colour", command= lambda: text_box.change_background_clr('comment'))
        view_menu.add_separator()

        view_menu.add_command(label=f"Change Src Colour", command= lambda : text_box.change_text_clr('src'))
        view_menu.add_command(label=f"Change Src Background Colour", command= lambda: text_box.change_background_clr('src'))
        view_menu.add_separator()

        view_menu.add_command(label=f"Change Des Colour", command= lambda : text_box.change_text_clr('des'))
        view_menu.add_command(label=f"Change Des Background Colour", command= lambda: text_box.change_background_clr('des'))

    def cut(e) :
        try :
            if text := text_box.selection_get():
                # selected = text 
                text_box.delete("sel.first", "sel.last")
                root.clipboard_clear()
                root.clipboard_append(text) 
        except TclError:
                pass

    def copy(e):
        try :
            if text := text_box.selection_get():
                # selected = text
                root.clipboard_clear()
                root.clipboard_append(text) 
        except TclError:
                pass

    def paste(e):
        try:
            selected = root.clipboard_get()
        except :
            return
        if selected:

            # delete selcted before pasting
            try :
                if text_box.selection_get():
                    text_box.delete("sel.first", "sel.last")
            except:
                pass

            pos = text_box.index(INSERT)
            text_box.insert(pos, selected)

    def select_all(e):
        text_box.tag_add("sel","1.0","end")

    def clear(e):
        text_box.delete(1.0,END)

    def toggle_comment(e):
        pos = text_box.index(INSERT)
        start = pos.split('.')[0]
        end = start + ".2"
        start += ".0"
        txt = text_box.get(start, end )
        if "# " in txt:
            text_box.delete(start,end)
            return
        elif "#" in txt:
            text_box.delete(start,end)
            return
        else:
            text_box.insert(start, "# ")

    def close():
        if messagebox.askokcancel("Quit", "Do you want to save before qutting?"):
            file_manager.save()
        root.quit()

    root = Tk()
    root.iconbitmap('F:\sarath\python/template_generator\editor/icon.ico')
    root.title("Boiler Plate Editor")

    window_frame = Frame(root, padx=5,pady=5)
    window_frame.pack()

    txt_scroll_bar = Scrollbar(window_frame)
    txt_scroll_bar.pack(side=RIGHT, fill=Y)

    horizontal_scroll_bar = Scrollbar(window_frame, orient="horizontal")
    horizontal_scroll_bar.pack(side=BOTTOM, fill=X)

    text_box = CustomText(window_frame, padx=5, pady=5, font=("",14), selectbackground="#bbb", undo=True,wrap="none",xscrollcommand=horizontal_scroll_bar.set, yscrollcommand=txt_scroll_bar.set)
    text_box.pack()

    txt_scroll_bar.config(command=text_box.yview)
    horizontal_scroll_bar.config(command=text_box.xview)

    main_menu = Menu(root)
    root.config(menu=main_menu)

    file_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_manager = FileManager(root, text_box)
    # config file menu depends on file_manager
    config_file_menu()

    edit_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Edit", menu=edit_menu)
    config_edit_menu()

    view_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="View", menu=view_menu)
    config_view_menu()

    config_keyboard_shortcuts()

    if path is not None:
        print(path)
        file_manager.open_file(path)

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()

if __name__ == "__main__":
    
    # t = Thread( target=text_editor, args=('cmds.bt',))
    # t2 = Thread( target=text_editor, args=('cmds2.bt',))

    # t.start()
    # t2.start()
    text_editor()