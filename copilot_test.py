import requests
import json

# joke = requests.get('https://icanhazdadjoke.com/',
#                     headers={"Accept": "application/json"})
# # send the fact
# print(joke.json()['joke'])

# get the synopsis from a movie, the user has to specify the movie
# synopsis = requests.get('http://www.omdbapi.com/?t=the+matrix&apikey=thewdb')
# print(synopsis.json()['Plot'])

# ask the user for input
userIn = input('What is your favorite movie? ')
# get the synopsis from the user input
synopsis = requests.get('http://www.omdbapi.com/?t={}&apikey=thewdb'.format(userIn))
# print the synopsis
print(synopsis.json()['Plot'])