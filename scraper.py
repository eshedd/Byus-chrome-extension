import urllib.request

opener = urllib.request.FancyURLopener({})
f = opener.open('http://textfiles.com/news/092793.txt')
content = list(f.read().decode("utf-8"))
newContent = []
for i in range(len(content)):
    if content[i] == '\r':
        content[i] = ' '
    elif content[i] == '\n':
        content[i] = ''
print(''.join(str(y) for y in content))