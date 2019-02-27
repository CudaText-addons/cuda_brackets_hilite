import cudatext as app
from .getline import get_line

def find_matching_bracket(ed, from_x, from_y, chars):
    '''
    Example of chars: "()[]{}".
    Direction of search (up/down) is auto-detected from "chars".
    Gets tuple (pos_x, pos_y, char_here, char_pair) or None if not found.
    '''
    cache = {}

    def find_token_type(x, y):

        tokens = cache.get(y)
        if tokens is None:
            tokens = ed.get_token(app.TOKEN_LIST_SUB, y, y)
            cache[y] = tokens
            
        if tokens:
            for t in tokens:
                if t['x1']<=x<t['x2']:
                    return t['style']
        return ''

    line = get_line(ed, from_y)
    if line is None: return
    if not from_x in range(len(line)): return
    ch = line[from_x]
    pos = chars.find(ch)
    if pos<0: return
    
    if pos%2==0:
        ch_end = chars[pos+1]
        down = True
    else:
        ch_end = chars[pos-1]
        down = False 

    to_x = from_x
    to_y = from_y
    cnt = 0
    type_from = find_token_type(from_x, from_y)
    #print('find "%s" from (%d,%d)'%(ch,to_x,to_y))
    
    while True:
        for pos in (range(to_x, len(line)) if down else
                    range(to_x, -1, -1)):
            ch_now = line[pos]
            # ignore tokens of different type (in comments/strings)
            if find_token_type(pos, to_y)!=type_from:
                continue
            if ch_now==ch:
                cnt+=1
            elif ch_now==ch_end:
                cnt-=1
                if cnt==0:
                    return (pos, to_y, ch, ch_end)
                    
        if down:
            to_y+=1
        else:
            to_y-=1
        line = get_line(ed, to_y)
        if line is None: return
        if down:
            to_x=0
        else:
            to_x=len(line)-1
