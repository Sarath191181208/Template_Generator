# import all functions from the tkinter
import tkinter as tk
from tkinter.constants import END
from tkinter.font import Font
from tkinter.colorchooser import askcolor

# how to create a custon text class and adding a event trigger is refered from stackoverflow from : https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        self.tags = [
                    ("copy",        "#FF0287", None ),
                    ("directory",   "#2185e8", None ),
                    ("comment",     "#06d420", None ),
                    ("src",         "#f6a440", None ),
                    ("des"        , "#d000fa", None )
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
                except tk.TclError:
                        pass

    def clear(self):
        for tag, _,_ in self.tags:
            self.tag_remove(tag,"1.0","end")

    def update(self,e):
        self.clear()
        txt = self.get(1.0,END)

        line_count = 1
        word_count = 0

        comment = False
        comment_start_count = 0

        copy_placed = False
        src_placed = False
        # is_copy = False

        word = ""
        for idx,char in enumerate(txt):
            word += char.lower()
            word_count += 1

            if not comment and char == "/":
                self.highlight_text(start=f"{line_count}.{word_count-len(word)}", end=f"{line_count}.{word_count}", tag="directory")
                
            if char == "#":
                comment = True
                comment_start_count = word_count-1

            if not comment and word in ['copy','copy ','copy\n','copy\t'] and (txt[idx+1] in [' ','\n','\t',''] if len(txt)-1 > idx else True):
                self.highlight_text(start=f"{line_count}.{word_count-4}", end=f"{line_count}.{word_count}", tag="copy")
                copy_placed = True
                # is_copy = True

            if char in [' ','\t']:

                if not comment and copy_placed and src_placed and word not in ['','\n','\t',' ']:
                    self.highlight_text(start=f"{line_count}.{word_count-len(word)}", end=f"{line_count}.{word_count}", tag="des")
                
                elif not comment and copy_placed and word not in ['','\n','\t',' ','copy','copy ','copy\n','copy\t']:
                    src_placed = True
                    self.highlight_text(start=f"{line_count}.{word_count-len(word)}", end=f"{line_count}.{word_count}", tag="src")

                word = ''

            if char == '\n':
                if comment:
                    self.highlight_text(start=f"{line_count}.{comment_start_count}", end=f"{line_count}.{word_count}", tag="comment")
                    comment = False
                elif copy_placed and src_placed and word not in ['','\n','\t',' ']:
                    self.highlight_text(start=f"{line_count}.{word_count-len(word)}", end=f"{line_count}.{word_count}", tag="des")
                elif copy_placed and word not in ['','\n','\t',' ','copy','copy ','copy\n','copy\t']:
                    src_placed = True
                    self.highlight_text(start=f"{line_count}.{word_count-len(word)}", end=f"{line_count}.{word_count}", tag="src")

                word = ''
                line_count += 1
                word_count = 0
                copy_placed, src_placed = False, False

        if comment:
            self.highlight_text(start=f"{line_count}.{comment_start_count}", end=f"{line_count}.{word_count}", tag="comment")
            comment = False

def demo():

        # Create a GUI window
        root = tk.Tk()

        # place Pad object in the root window
        # TextBox(root).pack(expand=1, fill="both")
        CustomText(root).pack()


        # start the GUI
        root.mainloop()

# Driver code
if __name__ == "__main__":

        # function calling
        demo()
