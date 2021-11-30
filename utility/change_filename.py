import os

path = './sounds_complete/'

for file in os.listdir(path):
    name = str.split(file,'.')[0]
    ext = str.split(file,'.')[1]
    newName = str.upper(name) + '.' + ext
    os.rename(os.path.join(path, file), os.path.join(path, newName))
    print('rename:  ' + newName)