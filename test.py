import gdown

url = 'https://drive.google.com/uc?id=1YIU9CyG6PJhojiam13znjC5migGxVEJj'

output = 'lol.txt'
gdown.download(url, output, quiet=False)