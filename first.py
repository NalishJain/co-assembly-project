import sys

inp = sys.stdin.read().split('\n')

new = []

for i in inp:
    new.append(i+'lolz\n')
newstr = ''
for i in inp:
    newstr += i + 'lolz\n'

sys.stdout.write(newstr)


