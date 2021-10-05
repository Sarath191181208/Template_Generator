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
                except tk.TclError:
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

                    self.highlight_text(start=f"{line_cnt+1}.{word_count}", end=f"{line_cnt+1}.{idx}", tag="src")
                    self.highlight_text(start=f"{line_cnt+1}.{idx+1}", end=f"{line_cnt+1}.end", tag="des")
                    
                    # continue

                idx += 1
                if char in [" ","\t"]:
                    word = ""

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
