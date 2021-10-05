import os
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from components.text_box import CustomText

# from threading import Thread

class FileManager():
    def __init__(self, root, text_box, status_bar) -> None:
        self.open_file_name = False

        self.root, self.text_box, self.status_bar = root, text_box, status_bar
        
    def new_file(self):
        self.open_file_name = False
        self.text_box.delete("1.0",END)
        self.root.title("*New File")
        self.status_bar.config(text="Unsaved")

    def open_file(self, path=None):
        text_file = askopenfilename(title="Open File", filetypes=[("Boilerplate File","*.bt")]) if path is None else path
        if text_file is None or text_file == "":
            return

        self.open_file_name = text_file

        self.text_box.delete("1.0",END)
        name = os.path.split(text_file)[1].split(".")[0]
        self.root.title(name)
        self.status_bar.config(text="Open")

        with open(text_file, "r") as f:
            self.text_box.insert(END,f.read())
            self.text_box.update(False)

    def save_as(self):
        text_file = asksaveasfilename(title= "Save File",defaultextension=".bt", filetypes=[("Boilerplate Files",".bt"),("Text Files",".txt")])
        if text_file:
            self.open_file_name = text_file

            name = os.path.split(text_file)[1].split(".")[0]
            self.root.title(name)
            self.status_bar.config(text="Saved")
        
            with open(text_file, "w") as f:
                f.write(self.text_box.get(1.0, END))

    def save(self):
        if self.open_file_name:
            with open(self.open_file_name, "w") as f:
                f.write(self.text_box.get(1.0, END))
                self.root.title(os.path.split(self.open_file_name)[1].split(".")[0])
        else:
            self.save_as()

def text_editor(path=None):

    def config_keyboard_shortcuts():
        root.bind("<Control-Key-x>", cut)
        root.bind("<Control-Key-c>", copy)
        # this is just a return value place holder not to run paste twice
        root.bind("<Control-Key-v>", lambda x : paste)
        root.bind("<Control-Key-k>", toggle_comment)
        root.bind("<Control-Key-a>", select_all)

    def config_file_menu():
        file_menu.add_command(label="New", command=file_manager.new_file)
        file_menu.add_command(label="Open", command=file_manager.open_file)
        file_menu.add_command(label="Save", command=file_manager.save)
        file_menu.add_command(label="SaveAs", command=file_manager.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=root.quit)
    
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
        # this must be in mainloop to work
        # if messagebox.askokcancel("Quit", "Do you want to save befor qutting?"):
        #     file_manager.save()
        root.quit()


    root = Tk()

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

    status_bar = Label(root, text="No errors", anchor = E)

    file_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_manager = FileManager(root, text_box, status_bar)
    # config file menu depends on file_manager
    config_file_menu()

    edit_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Edit", menu=edit_menu)
    config_edit_menu()

    view_menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="View", menu=view_menu)
    config_view_menu()

    status_bar.pack(fill=X, side=BOTTOM, pady=5)

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