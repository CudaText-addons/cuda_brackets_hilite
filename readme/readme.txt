Plugin for CudaText
Finds and highlightes bracket under caret and its pair bracket 
(pair bracket is searched considering nesting).

Gives items in Plugins menu:
- Go to pair bracket
- Select to pair bracket 
- Select to pair bracket, inside
Item in Options / Settings-plugins:
- Config

Config file
-----------

- Section [brackers_lexers]
  Bracket pairs, listed per lexer, e.g.
    PHP=()[]{}
    Go=() 
  Key "default": value for all not mentioned lexers.

- Section [brackets_file_types]
  Bracket pairs, listed per file extension (with dot, lower case), e.g. 
  .ini=[]()
  Section is used only for files without lexer.

- Section [color]
  Keys "fore" and "back".
  Colors of highlighting, in HTML form, "#rrggbb" or "#rgb".
  Use "Color Picker" plugin to edit HTML color values here.

- Section [op]
  Other options. Plugin saves default values here, so no need to mention them.  


Author: Alexey (CudaText)
License: MIT
