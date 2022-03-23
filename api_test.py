import requests
import json

categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke',
              'dance', 'cringe']

for i in range(len(categories)):
    print(f'{i+1}) {categories[i]}')

userIn = int(input('Choose a category: '))
response = requests.get(f'https://api.waifu.pics/sfw/{categories[userIn - 1]}').text
response_object = json.loads(response)
print(response_object['url'])
