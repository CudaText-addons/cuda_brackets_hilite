import os
import shutil
from cudatext import *
from cudax_lib import html_color_to_int
from .proc_brackets import *

MARKTAG = 10 #uniq value for all markers plugins
CANNOT_USE_SEL = False #cannot work if selection

NAME_INI = 'cuda_brackets_hilite_.ini'
ini_app = os.path.join(app_path(APP_DIR_SETTINGS), NAME_INI)
ini_def = os.path.join(os.path.dirname(__file__), NAME_INI)

if not os.path.isfile(ini_app) and os.path.isfile(ini_def):
    shutil.copyfile(ini_def, ini_app)

COLOR_FONT = html_color_to_int(ini_read(ini_app, 'color', 'fore', '#000000'))
COLOR_BG = html_color_to_int(ini_read(ini_app, 'color', 'back', '#80c080'))

brackets_lexers = {}
brackets_types = {}


def get_chars_filetype():

    global brackets_types

    fn = os.path.basename(ed.get_filename())
    if not fn: return ''

    npos = fn.rfind('.')
    if npos<0: return ''

    fn = fn[npos:].lower()
    res = brackets_types.get(fn, None)
    if res is not None: return res

    res = ini_read(ini_app, 'brackets_file_types', fn, '')
    #print('ini_read types')
    brackets_types[fn] = res
    return res


def get_chars():
    global prev_lexer
    global prev_chars
    global brackets_lexers
    global brackets_types

    lexer = ed.get_prop(PROP_LEXER_CARET)
    val = brackets_lexers.get(lexer, None)
    if val is not None:
        return val

    val_def = ini_read(ini_app, 'brackets_lexers', 'default', '')
    val_lexer = ini_read(ini_app, 'brackets_lexers', lexer, val_def)
    val_type = get_chars_filetype()
    #print('val_def _lexer _type: "%s", "%s", "%s"'%(val_def, val_lexer, val_type))

    if lexer:
        brackets_lexers[lexer] = val_lexer
        return val_lexer

    if val_type:
        return val_type

    if val_def:
        return val_def

    return ''


class Command:
    entered=False

    def config(self):
        if os.path.isfile(ini_app):
            file_open(ini_app)
        else:
            msg_box('Cannot find config: '+ini_app, MB_OK)

    def on_caret(self, ed_self):
        if self.entered: return
        self.entered=True

        try:
            marks = ed.attr(MARKERS_GET)
            if marks:
                ed.attr(MARKERS_DELETE_BY_TAG, MARKTAG)

            carets = ed.get_carets()
            if len(carets)!=1:
                return
            x, y, x1, y1 = carets[0]
            if CANNOT_USE_SEL:
                if x1>=0:
                    return

            chars = get_chars()
            if not chars: return

            line = ed.get_text_line(y)
            if line is None: return

            if not 0<=x<len(line):
                if x>0 and x==len(line) and line[x-1] in '()[]{}':
                    x -= 1
                else:
                    return

            #check caret is on bracket
            if not line[x] in '()[]{}':
                #allow caret after bracket
                if x>0 and line[x-1] in '()[]{}':
                    x -= 1
                else:
                    return

            res = find_matching_bracket(ed, x, y, chars)
            if res is None:
                return
            x1, y1 = res

            ed.attr(MARKERS_ADD, MARKTAG, x, y, 1, COLOR_FONT, COLOR_BG)
            ed.attr(MARKERS_ADD, MARKTAG, x1, y1, 1, COLOR_FONT, COLOR_BG)
        finally:
            self.entered=False

    def jump(self):
        self.do_find(True)
    def select(self):
        self.do_find(False)
    def select_in(self):
        self.do_find(False, True)

    def do_find(self, is_jump, select_inside=False):
        carets = ed.get_carets()
        if len(carets)!=1:
            msg_status('Cannot go to bracket if multi-carets')
            return

        x, y, x1, y1 = carets[0]
        if x1>=0:
            msg_status('Cannot go to bracket if selection')
            return

        chars = get_chars()
        if not chars: return

        res = find_matching_bracket(ed, x, y, chars)
        if res is None:
            msg_status('Cannot find pair bracket')
            return
        x1, y1 = res

        if is_jump:
            ed.set_caret(x1, y1)
            msg_status('Go to pair bracket')
        else:
            #select from (x,y) to (x1,y1)
            sel_delta = -1 if select_inside else 0
            if (y1>y) or ((y1==y) and (x1>x)):
                #sel down
                ed.set_caret(
                  x1+1+sel_delta, y1,
                  x-sel_delta, y)
            else:
                #sel up
                ed.set_caret(
                  x1-sel_delta, y1,
                  x+1+sel_delta, y)
            msg_status('Selected to pair bracket')
