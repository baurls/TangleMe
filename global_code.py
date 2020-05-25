#global constants
import numpy as np
#input

#output
IMG_OUTPUT_PATH = 'plots/'

#...........................................................................................
#                                      reusable functionality
#...........................................................................................
base_set = 'a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z'
lower_chars = base_set.split('.')
upper_chars = base_set.upper().split('.')
numbers = [str(i) for i in range(10)]
char_set = lower_chars + upper_chars + numbers

def get_random_name_of_length(k):
    positions = np.random.randint(low=0, high=len(char_set), size=k)
    name = ''
    for pos in positions:
        name += char_set[pos]
    return name