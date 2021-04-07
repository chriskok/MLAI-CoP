import os

found = []
for d in os.listdir():
    if os.path.isdir(d):
        if os.path.isfile(d + os.sep + 'main.py'):
            found.append(d)

if len(found):
    print('\nusage: run the main.py in one of the example directories:')
    for d in found:
        print(' ', d)
    print()


