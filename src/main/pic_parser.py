from re import compile
from src.main.utils import memoize

alpha = compile('^A\(\d+\)$')
all_chars = compile('^X\(\d+\)$')

def create_pic_mutator_fns(pic_setup_value, coerce=False):
    mutator_fns = [str] if coerce else []

    if isinstance(pic_setup_value, list):
        mutator_fns.append(_create_88_pic_validator(pic_setup_value))
    elif alpha.match(pic_setup_value):
        if coerce:
            mutator_fns.append(lambda s: s.rjust(int(pic_setup_value[2:-1])))
        mutator_fns.append(_create_alpha_validator(pic_setup_value))
    elif all_chars.match(pic_setup_value):
        if coerce:
            mutator_fns.append(lambda s: s.rjust(int(pic_setup_value[2:-1])))

    return mutator_fns

def _create_88_pic_validator(pic_setup_values):
    if not all(len(val) == len(pic_setup_values[0]) for val in pic_setup_values):
        raise ValueError('The following are not all the same length: %s' % ', '.join(pic_setup_values))

    regex = compile('(%s)' % '|'.join(pic_setup_values))

    def validator(new_value):
        if not regex.match(new_value):
            raise ValueError('%s does not match any of the following: %s' % (new_value, ', '.join(pic_setup_values)))

        return new_value

    return validator

def _create_alpha_validator(pic_setup_value):
    regex = compile('[A-Z]{%s}' % pic_setup_value[2:-1])

    def validator(new_value):
        if not regex.match(new_value):
            raise ValueError('%s contains non-alphabet characters' % new_value)

        return new_value

    return validator

@memoize
def _justify(char, maxlen):
    def j(new_value):
        return str.rjust(new_value, maxlen, char)
    return j