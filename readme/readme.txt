Plugin for CudaText
Finds and highlightes bracket under caret and its pair bracket (pair bracket is searched considering nested brackets).

Gives items in Plugins menu:
- Go to pair bracket
- Select to pair bracket 
- Select to pair bracket, inside
Item in Options / Settings-plugins:
- Config

Config file:

- Section [brackers_lexers]
  Brackets per lexer, e.g.
  PHP=()[]{} 
  Key "default" sets default value.

- Section [brackets_file_types]
  Brackets per file extension, with dot, lower case, e.g. 
  .ini=[]()
  Section is used only for files without lexer.

- Color of highlighting (use Color Picker plugin to edit HTML colors here)


Author: Alexey (CudaText)
License: MIT
