#!/usr/bin/env python2.7

import json
import os
import re

def main():
    session_cells = {n: [] for n in range(1, 6+1)}
    f = open(os.path.dirname(__file__) + '/../All.ipynb')
    j = json.load(f)
    cells = j['cells']
    for cell in cells:
        source = u''.join(cell['source'])
        m = re.search(r'# +(\d+)\. ', source.strip())
        if not m:
            continue
        n = int(m.group(1))
        session_cells[n].append(cell)
    for n, cells in sorted(session_cells.items()):
        print 'Session {}: {} cells'.format(n, len(cells))

if __name__ == '__main__':
    main()
