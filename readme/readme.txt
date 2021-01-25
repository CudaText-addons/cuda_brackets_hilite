Plugin for CudaText.
Finds and highlights bracket under caret and its pair bracket (pair bracket
is searched considering nesting). Plugin also considers kind of brackets,
so if source bracket is inside code/comment/string, the found bracket must
be of the "same kind" (have the same lexer style).

Gives items in the Plugins menu:
- Go to pair bracket
- Select to pair bracket
- Select to pair bracket, inside
And item in "Options / Settings-plugins / Bracket Hilite":
- Config

Config file
-----------

- Section [brackets_lexers]
  Bracket pairs, listed per lexer. For ex:
    PHP=()[]{}
    Go=()
  Key "default": value for all not mentioned lexers.

- Section [brackets_file_types]
  Bracket pairs, listed per file extension (with dot, lower case). For ex:
    .cuda-snippet=[]()
  Section is used only for files without lexer.

- Section [color]
  Keys "fore" and "back".
  Colors of highlighting, in HTML form, "#rrggbb" or "#rgb".
  Use "Color Picker" plugin to edit HTML color values here.

- Section [op]
  cannot_use_sel (0/1): disable plugin work if selection exists.
  max_line_count (0/1): max count of lines in a file, when plugin work is enabled.


Author: Alexey Torgashin (CudaText)
License: MIT