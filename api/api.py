import time
import pickle

from .gamedata import GameData, RuWordList, str_to_bytes, bytes_to_str

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
		return self.wordtop[worddict[str_to_bytes(word)]]
	def place_to_word(self, place):
		if place <= self.closest_top_size:
			return wordlist[self.closest_top[place]]
		print(f'Попытка получить подсказку по слову с номером {place}, хотя предусмотрено только {self.closest_top_size}')
	def get_closest_top(self, size):
		if size <= self.closest_top_size:
			return list(self.closest_top)
		print(f'Попытка получить топ {size} ближайших слов, хотя предусмотрено только {self.closest_top_size}')

class GameDict:
	def __init__(self):
		self.loaded_games = TimeDict()
	def __getitem__(self, gamename):
		if gamename not in self.loaded_games:
			with open(f'games/{gamename}.pickle', 'rb') as f:
				gamedata = pickle.load(f)
			self.loaded_games[gamename] = Game(gamedata)
			if len(self.loaded_games) > GAME_COUNT_LIMIT:
				self.loaded_games.pop(agest := self.loaded_games.get_agest())
				print(f'Освобождена память из-под игры {agest}')
		return self.loaded_games[gamename]

with open('wordlist.pickle', 'rb') as f:
	wordlist = pickle.load(f)

worddict = {wordlist.words_bytes[i]: i for i in range(len(wordlist.words_bytes))}
games = GameDict()
