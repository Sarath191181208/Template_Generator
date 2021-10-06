# Boiler Plate

Ever wondered if you could just create files at bulk and copy some code over, This solves just that.
When I was creating a bunch of pygame projects I realised that I was just copying a bunch of code over and over again. Realising this was a problem that almost everyone has, I strived to solve it.

# Description

Using the main.exe in dist/main you can run **.bt** files which are just simple commands written in a file. To know more about .bt files refer to the Usage section. Dist folder also contains another exe namely eidtor.exe which is just a text editor for **.bt** files you can use any text editor but this editor provides syntax highlighiting for **.bt** files. You can edit **.bt** files in almost any editor.

## Demo

![Image](https://github.com/Sarath191181208/Template_Generator/blob/master/images/Screenshot.png)

## Features

- Copy the text of any file from one to other.
- Create directories.
- Create files.
- Write Comments.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/Template_Generator
```

Go to the project directory

```bash
  cd ./Template_Generator
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## Creating an exe

Note : Editor and Template Manager must be created seperately.

Make sure to install pyinstaller `pip install pyinstaller`.

Make sure to change the paths of the files
You can also use `auto-py-to-exe` for ease, using the json file.

You can know more about [auto-py-to-exe](https://dev.to/eshleron/how-to-convert-py-to-exe-step-by-step-guide-3cfi)

```bash
pyinstaller --noconfirm --onedir --windowed --icon "pre_path/template_generator/icon.ico" --add-data "pre_path/template_generator/assets;assets/" --add-data "pre_path/template_generator/components;components/" --add-data "pre_path/template_generator/save;save/" --add-data "pre_path/template_generator/icon.png;."  "pre_path/template_generator/main.py"
```

## References

Converting python files to exe from a youtube channel named Python Simplified :
https://www.youtube.com/watch?v=Y0HN9tdLuJo

Icons ->
Icons are picked from Internet, made the file icon myself.

## Usage

- Make sure to create a templates folder you can call anything you want, we will be creating our **.bt** file here.

- Create a file named template ending with **.bt**.

- You can also do the following in Editor and save it to template folder afterward.

## Creating a file

- First of write a filename on first line
  ex : test.txt
- When run this creates a test.txt in selected folder

## Creating a directory

- Write a directory (folder) ex : test/
- This creates a directory (folder) in selected folder.
- Chaining the first two you can also creating a file in a directory like ex : test/test.txt

## Copying a file from another

- Create a test.txt in templates folder write some text in it.
- Write COPY test.txt my_txt.txt .
- Note : COPY isn't case sensitive you can also use copy if you prefer.
- Here test.txt exists in templates folder.
- This copies text in test.txt to my_txt.txt in your selcted directory.
- You can Chain this with the previous ones above .
- Create a test folder inside templates folder
- Create a test.txt inside test folder.
- Write `COPY test/test.txt my_dir/test.py `
- Here the test/test.txt is source dirctory and my_dir/test.py is the destination directory.
- This copies text inside test folder and in test.txt and copies it to test.py which is in a folder which is created called my_dir.
- Note : you can use any file you like ,
  ex: COPY this.py that.py, this is completely fine.
- Note : The path of source directory is relative.

## Adding a comment

- You can add a **_#_** before a line or inline it just doesn't execute the commands after that.

## Hot keys in Editor

- Ctrl+N : New file
- Ctrl+S : Save
- Ctrl+Shift+S : Save As
- Ctrl+R : Load/Read a file
- Ctrl+Q : Quit

- Ctrl+Z : Undo
- Ctrl+Y : Redo
- Ctrl+X : Cut
- Ctrl+C : Copy
- Ctrl+V : Paste
- Ctrl+K : Add a comment
- Ctrl+A : Select all

## Requirements

- python `Make sure to add to path`
- pygame `pip install pygame`
- tkinter `default`
- pyinstaller `pip install pyinstaller` this is to create an exe alternatively you can use auto-py-to-exe `pip install auto-py-to-exe`

## Authors

- [Sarath](https://www.github.com/https://github.com/Sarath191181208)
