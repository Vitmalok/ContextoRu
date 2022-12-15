import random
import pickle
from zipfile import ZipFile

from api.gamedata import GameData

wordlist = [
	'кошка',
	'собака',
	'апельсин',
	'арбуз',
	'рыба',
	'мышь',
	'карандаш',
	'лягушка',
	'морковь',
	'сосиска',
	'тарелка',
	'клавиша',
	'мозг',
	'человек',
	'животное',
	'небо',
	'луна',
	'звезда',
	'дом',
]

with ZipFile('wordlist.zip', 'w') as zipfile:
	with zipfile.open('wordlist.pickle', 'w') as f:
		pickle.dump(wordlist, f)

wordtop = list(range(1, len(wordlist) + 1))
random.shuffle(wordtop)
print(wordtop)  # [4, 15, 2, 9, 16, 13, 10, 1, 6, 14, 8, 5, 17, 7, 18, 19, 11, 12, 3]
game = GameData(wordtop)

with open('games/test3.pickle', 'wb') as f:
	pickle.dump(game, f)
