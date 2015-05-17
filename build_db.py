# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
import re
import sys
from io import open

import pyphen

from generator import TEXT_START, WORD_END, SPECIAL_TOKENS


def splitword(word):
	return re.split(r'-|([!?.])', word, re.U)


def get_hyphen_text():
	text = open(sys.argv[1], encoding='utf-8').read()
	words = [word.lower() for word in re.findall(r'[\w]+[?.!,]?', text, re.U)]
	dic = pyphen.Pyphen(lang=sys.argv[3])

	text = []
	for word in words:
		text += [i for i in splitword(dic.inserted(word)) if i] + [WORD_END]
	return text


def main():
	if len(sys.argv) != 4:
		sys.stderr.write(sys.argv[0] + " input.txt output language\n")
		sys.exit(1)

	text = get_hyphen_text()
	token_list = tuple(set(text).union(SPECIAL_TOKENS))
	token_list_search = {s: i for i, s in enumerate(token_list)}
	token_transitions = [{} for _ in token_list]

	lastword = TEXT_START
	for s in text:
		if lastword in SPECIAL_TOKENS and s in SPECIAL_TOKENS:
			continue
		new_idx = token_list_search[s]
		last_idx = token_list_search[lastword]
		token_transitions[last_idx].setdefault(new_idx, 0)
		token_transitions[last_idx][new_idx] += 1
		lastword = TEXT_START if s in SPECIAL_TOKENS else s

	token_transitions = tuple(tuple(v.items()) for v in token_transitions)

	pickle.dump((token_list, token_transitions), open(sys.argv[2], 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	main()
