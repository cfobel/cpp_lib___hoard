from path import path
import re
import itertools
from pprint import pprint

if __name__ == '__main__':
    d = path('make_targets.txt').lines()
    d = [re.sub(r'\\#', r'#', l) for l in d]
    default_paths = ['.', 'heaplayers', 'heaplayers/util']
    platforms, commands = zip(*[l.split(' := ') for l in d])
    commands = [re.sub(r'(-o|libhoard\.\w+)', '', c) for c in commands]
    commands = [re.split(r'\s+', c.strip())[1:] for c in commands]

    paths = [[f[2:] for f in flags if f.startswith('-I') and f[2:] not in default_paths] for flags in commands]
    libs = [[f[2:] for f in flags if f.startswith('-l')] for flags in commands]
    sources = [[f for f in flags if re.match(r'.*\.cpp', f)] for flags in commands]

    #print [list(itertools.chain(*avoid)) for avoid in zip(paths, libs, source)]
    #pprint([['-I%s' % p for p in default_paths] + list(itertools.chain(*avoid)) + ['-shared', '-static'] for avoid in zip(paths, libs, source)])
    #raise SystemExit

    commands = [[f for f in flags if not f in ['-I%s' % p for p in default_paths] + list(itertools.chain(*avoid)) + ['-shared', '-static']] for flags, avoid in zip(commands, zip(paths, libs, sources))]

    print 'env = Environment(CPPPATH=%s)\nsources = []' % str(default_paths)
    i = 0
    for platform, command, path_list, lib_list, source in zip(platforms, commands, paths, libs, sources):
        if i > 0:
            print 'elif',
        else:
            print 'if',
            i = 1

        print ''''%s' in COMMAND_LINE_TARGETS:''' % platform.lower()
        source.insert(0, 'libhoard.cpp')
        print '''    sources = %s''' % str(source)
        print '''    env.Append(CPPFLAGS=%s)''' % str(command)
        if len(path_list):
            print '''    env.Append(CPPPATH=%s)''' % str(path_list)
        if len(lib_list):
            print '''    env.Append(LIBS=%s)''' % str(lib_list)

    print '\n\n'

    print '''libhoard = env.SharedLibrary(sources, SHLIBPREFIX='')'''

    print '''\nDefault()'''
    for platform in platforms:
        print '''Alias('%s', libhoard)''' % platform.lower()
