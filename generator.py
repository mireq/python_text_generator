# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import pickle
from itertools import chain


TEXT_START = ''
SENTENCE_END = ['.', '?', '!']
WORD_END = '\0'
SPECIAL_TOKENS = set(SENTENCE_END + [TEXT_START, WORD_END, ','])


class TextGenerator(object):
	def __init__(self, token_list, token_transitions):
		self.token_list = token_list
		self.token_transitions = token_transitions
		self.token_list_search = {s: i for i, s in enumerate(self.token_list) if s in SPECIAL_TOKENS}
		self.stop_tokens = set([self.token_list_search[w] for w in (SENTENCE_END + [WORD_END])])
		self.token_transitions_idx = tuple(tuple(chain(*[[v[0]] * v[1] for v in val])) for val in self.token_transitions)

	def __generate_word(self):
		word = []
		current_part = self.token_list_search[TEXT_START]
		stop = self.token_list_search[WORD_END]
		while current_part not in self.stop_tokens:
			parts = self.token_transitions_idx[current_part]
			current_part = parts[random.randrange(0, len(parts))]
			if current_part != stop:
				word.append(self.token_list[current_part])
		return ''.join(word)

	def get_word(self, uppercase=False, include_stops=False, min_length=1):
		word = ''
		while len(word) < min_length:
			word = self.__generate_word()
		if not include_stops and word[-1] in SPECIAL_TOKENS:
			word = word[:-1]
		if uppercase:
			if len(word) > 1:
				word = word[0].upper() + word[1:]
			else:
				word = word.upper()
		return word

	def get_sentence(self):
		words = []
		word = ''
		while word[-1:] not in set(SENTENCE_END):
			word = self.get_word(uppercase=len(words) == 0, include_stops=True)
			words.append(word)
		return ' '.join(words)

	def get_paragraph(self, length=None):
		paragraph = []
		if length is None:
			length = int(random.expovariate(.25) + random.randint(5, 10))
		return ' '.join(self.get_sentence() for _ in range(length))

	@staticmethod
	def from_file(filename):
		token_list, token_transitions = pickle.load(open(filename, 'rb'))
		return TextGenerator(token_list, token_transitions)
