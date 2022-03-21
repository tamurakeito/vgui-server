content = ''
content += 'S : NS_B CMD NS_E\n'
header = 'CMD : '
nl = '\n'
path = 'cmd.grammar'
cmd = 'CMD'

command = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

for i in command:
    content += header + i + cmd + nl

for i in command:
    for j in command:
        content += header + i + cmd + ' ' + j + cmd + nl


w = open(path)
with open(path, mode='w') as f:
    f.write(content)