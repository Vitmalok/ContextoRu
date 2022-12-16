import pickle

from api.gamedata import GameData, str_to_bytes, bytes_to_str



def generate(secret_word, model_type='int'):
	global KeyedVectors, model_int, model_str, wordlist, worddict
	
	if 'KeyedVectors' not in globals():
		from gensim.models import KeyedVectors
		print('Импортированы KeyedVectors')
	if model_type == 'str' and 'model_str' not in globals():
		model = KeyedVectors.load_word2vec_format('all.norm-sz500-w10-cb0-it3-min5-cleared-bin.w2v', binary=True)
		print('Загружена модель')
	if model_type == 'int' and 'model_int' not in globals():
		with open('model.pickle', 'rb') as f:
			model = pickle.load(f)
		print('Загружена модель')
	if 'wordlist' not in globals():
		with open('wordlist.pickle', 'rb') as f:
			wordlist = pickle.load(f)
		print('Загружен список слов')
	if 'worddict' not in globals():
		worddict = {wordlist.words_bytes[i]: i for i in range(len(wordlist))}
		print('Построена хеш-таблица индексов слов')
	
	if model_type == 'str':
		wordtop = model.most_similar(secret_word, topn=len(wordlist))
		print('Построен топ most_similar')
		top = {worddict[str_to_bytes(secret_word)]: 1}
		for place in range(len(wordtop)):
			top[worddict[str_to_bytes(wordtop[place][0])]] = place + 2
		print('Топ преобразован')
	elif model_type == 'int':
		secret_index = worddict[str_to_bytes(secret_word)]
		wordtop = model.most_similar(secret_index, topn=len(wordlist))
		print('Построен топ most_similar')
		top = [None]*len(wordlist)
		top[secret_index] = 1
		for place in range(len(wordtop)):
			top[wordtop[place][0]] = place + 2
		print('Топ преобразован')
	
	gamedata = GameData(top)
	print('Создан объект данных игры')
	return gamedata

def save(gamedata, gamename):
	with open(f'games/{gamename}.pickle', 'wb') as f:
		pickle.dump(gamedata, f)



if __name__ == '__main__':
	while True:
		print('Введите загаданное слово')
		gamedata = generate(secret_word := input(' >> '))
		print('Введите имя игры')
		save(gamedata, gamename := input(' >> '))
		print(f'Сохранено в games/{gamename}.pickle')
