# Pythonic way to do enums:
# http://stackoverflow.com/a/1695250/195722
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['val'] = reverse
    return type('Enum', (), enums)