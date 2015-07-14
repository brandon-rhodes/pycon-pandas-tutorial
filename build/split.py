#!/usr/bin/env python2.7

import glob
import json
import os
import re

def blank_code_cell():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {
            "collapsed": True
        },
        "outputs": [],
        "source": [],
    }

def question_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {
            "collapsed": True
        },
        "source": '### ' + text.strip(),
    }

def main():
    session_cells = {n: [] for n in range(1, 6+1)}
    f = open(os.path.dirname(os.path.abspath(__file__)) + '/../All.ipynb')
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

def convert(filename):
    f = open(filename)
    j = json.load(f)
    j['cells'] = list(filter_cells(filename, j['cells']))
    assert 'Solutions' in filename
    with open(filename.replace('Solutions', 'Exercises'), 'w') as f:
        f.write(json.dumps(j, indent=2))

def filter_cells(filename, cells):
    n = 0
    starting = True
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        source = u''.join(cell['source'])

        if starting:
            if not source.startswith('# '):
                yield cell
            else:
                starting = False

        if not source.startswith('# '):
            continue

        question = []

        for line in cell['source']:
            if not line.startswith('# '):
                break
            question.append(line[2:].strip())

        question = ' '.join(question)

        yield question_cell(question)

        yield blank_code_cell()
        yield blank_code_cell()

        n += 1
    print '{:6}   {}'.format(n, filename)

def main2():
    for filename in sorted(glob.glob('Solutions-*.ipynb')):
        convert(filename)

if __name__ == '__main__':
    main2()
