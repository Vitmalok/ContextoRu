import math
import pickle

def smart_bin(int_, bits):
	return bin(int_)[2:].rjust(bits, '0')
def add_buffer_to_list(list_, buffer_):
	list_.extend([int(buffer_[i:i + 8], 2) for i in range(0, len(buffer_), 8)])

class Bitset:
	def __init__(self, numbers, bits, index_offset=0):
		self.bits = bits
		self.index_offset = index_offset
		self.length = len(numbers)
		list_ = []
		buffer_ = ''
		for number in numbers:
			buffer_ += smart_bin(number, bits)
			if not len(buffer_)%8:
				add_buffer_to_list(list_, buffer_)
				buffer_ = ''
		if buffer_:
			add_buffer_to_list(list_, buffer_.ljust(math.lcm(bits, 8), '0'))
		self.bytes = bytes(list_)
	def __len__(self):
		return self.length
	def __getitem__(self, index):
		index += self.index_offset
		if index >= self.length:
			raise IndexError
		if index < 0:
			return None
		first_bit = index*self.bits
		byte_offset, bit_offset = divmod(first_bit, 8)
		return int(''.join([
			smart_bin(byte, 8) for byte in self.bytes[byte_offset:byte_offset + self.bits//8 + 2]
		])[bit_offset:bit_offset + self.bits], 2)

# word везде означает индекс слова в базе, а place - позиция слова в топе (нумерация начинается с 1)
# wordtop - список, сопоставляющий индексу слова в базе его позицию в топе
# closest_top - список, сопоставляющий первым closest_top_size позициям топа индексы слов
class GameData:
	def __init__(self, wordtop, closest_top_size=1000):
		self.closest_top_size = closest_top_size
		self.bits_per_word = math.log2(len(wordtop)).__ceil__()
		self.wordtop = Bitset(wordtop, self.bits_per_word)
		self.closest_top = Bitset([
			pair[1] for pair in sorted([(wordtop[word], word) for word in range(len(wordtop)) if wordtop[word] < closest_top_size])
		], self.bits_per_word, -1)

# Функции для компактного хранения слов, состоящих только из маленьких русских букв
INT_TO_CHAR = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
CHAR_TO_INT = {INT_TO_CHAR[i]: i for i in range(len(INT_TO_CHAR))}
BITS_PER_CHAR = 5
def str_to_bytes(str_):
	bits = ''.join([smart_bin(CHAR_TO_INT[char], BITS_PER_CHAR) for char in str_])
	bits = smart_bin(mod := len(bits)%8, 3) + bits + '0'*((-mod - 3)%8)
	return bytes([int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)])
def bytes_to_str(bytes_):
	bits = ''.join([smart_bin(byte, 8) for byte in bytes_])
	bits = bits[3:-((-int(bits[:3], 2) - 3)%8)]
	return ''.join([INT_TO_CHAR[int(bits[i:i + BITS_PER_CHAR], 2)] for i in range(0, len(bits), BITS_PER_CHAR)])

class RuWordList:
	def __init__(self, wordlist):
		self.words_bytes = [str_to_bytes(word) for word in wordlist]
	def __len__(self):
		return len(self.words_bytes)
	def __getitem__(self, index):
		return bytes_to_str(self.words_bytes[index])
