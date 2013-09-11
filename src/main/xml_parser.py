'''
Created on Sep 10, 2013

@author: Harold
'''
from collections import deque
from re import compile
from xml.etree import ElementTree as ET

numeric = compile('^\d+$')
alphabetic = compile('^[\'\"][A-Z][\'\"]$')

def convert_copybook_to_xml(copybook):
    '''Converts a COBOL copybook to XML format. Line numbers are not permissible. Also, entries
    in the copybook must not be split across multiple lines.'''
    lines = map(_split_up_line, copybook.split('\n'))
    tags = deque([])
    for level, name, rest in lines:
        tag = _create_tag(level, name, rest)
        if isinstance(tag, list):
            tags.extend(tag)
        else:
            tags.append(tag)
    tree = _create_tree(tags.popleft(), tags)
    for tag in tree.getiterator():
        tag.set('level', str(tag.get('level')))
    return tree


def _split_up_line(line):
    line = line[:-1] if line.endswith('.') else line
    level, name, *rest = line.split()
    return int(level), name, [s.upper() for s in rest]


def _create_tag(level, name, rest):
    attribs = {'name': name, 'level': level}
    if not rest:
        tag = 'Block'
    elif rest[0] == 'OCCURS':
        tag = 'Block'
        attribs.update(_create_occurs_attribs(rest))
    elif rest[0] == 'REDEFINES':
        tag = 'Block'
        attribs['redefines'] = rest[1]
    elif level is 88:
        tag = 'Indicator'
        if 'THRU' not in rest and 'THROUGH' not in rest:
            attribs['value'] = rest[1]
        else:
            return _create_88_thru_tags(attribs, rest)
    elif rest[0] == 'PIC':
        tag = 'Picture'
        attribs['picFormat'] = rest[1]

    return ET.Element(tag, attribs)


def _create_88_thru_tags(attribs, values_clause):
    if numeric.match(values_clause[-1]) and numeric.match(values_clause[-3]):
        valmapper, ranger = str, int
    elif alphabetic.match(values_clause[-1]) and alphabetic.match(values_clause[-3]):
        valmapper, ranger = chr, lambda s: ord(s[1:-1])
    else:
        raise ValueError('Currently only integers and single letter supported for THRU clauses')

    els = [
        ET.Element('Indicator', attr) for attr in
        (
            dict(list(attribs.items()) + [('value', valmapper(i))])
            for i in range(ranger(values_clause[-3]), ranger(values_clause[-1])+1)
        )
    ]
    return els


def _create_occurs_attribs(occurs_clause):
    times_index = occurs_clause.index('TIMES')
    attribs = {
        'occursMin': occurs_clause[times_index-(3 if 'TO' in occurs_clause else 1)],
        'occursMax': occurs_clause[times_index-1]
    }
    if 'DEPENDING' in occurs_clause:
        attribs['occursDepends'] = occurs_clause[-1]
    return attribs


def _create_tree(tree, tags):
    if not tags:
        return tree

    tag_to_append = tags.popleft()
    append_level = tag_to_append.get('level')

    for tag in reversed(list(tree.getiterator())):
        if tag.get('level') < append_level:
            tag.append(tag_to_append)
            return _create_tree(tree, tags)