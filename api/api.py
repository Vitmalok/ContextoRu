import time
import pickle
from zipfile import ZipFile

from .gameclass import GameData

GAME_COUNT_LIMIT = 64

class TimeDict(dict):
	def __init__(self):
		self.times = {}
	def __setitem__(self, index, value):
		self.times[index] = time.time()
		dict.__setitem__(self, index, value)
	def __getitem__(self, index):
		self.times[index] = time.time()
		return dict.__getitem__(self, index)
	def get_agest(self):
		return min([(self.times[key], key) for key in self.keys()])[1]

class Game:
	def __init__(self, gamedata):
		self.closest_top_size = gamedata.closest_top_size
		self.bits_per_word = gamedata.bits_per_word
		self.wordtop = gamedata.wordtop
		self.closest_top = gamedata.closest_top
	def word_to_place(self, word):
		return self.wordtop[worddict[word]]
	def place_to_word(self, place):
		if place <= self.closest_top_size:
			return self.wordlist[self.closest_top[place]]
		print(f'Попытка получить подсказку по слову с номером {place}, хотя предусмотрено только {self.closest_top_size}')
	def get_closest_top(self, size):
		if size <= self.closest_top_size:
			return list(self.closest_top)
		print(f'Попытка получить топ {size} ближайших слов, хотя предусмотрено только {self.closest_top_size}')

def load_game(name):
	with open(f'games/{name}.pickle', 'rb') as f:
		gamedata = pickle.load(f)
	loaded_games[name] = Game(gamedata)
	if len(loaded_games) > GAME_COUNT_LIMIT:
		loaded_games.pop(agest := loaded_games.get_agest())
		print(f'Освобождена память из-под игры {agest}')

loaded_games = TimeDict()

with ZipFile('api/wordlist.zip', 'r') as zipfile:
	with zipfile.open('wordlist.pickle', 'rb') as f:
		wordlist = pickle.load(f)

worddict = {word: i for i in range(len(wordlist))}
