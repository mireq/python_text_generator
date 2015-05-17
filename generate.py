# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from generator import TextGenerator
import sys


def main():
	if len(sys.argv) != 2:
		sys.stderr.write(sys.argv[0] + " build_db_output\n")
		sys.exit(1)

	generator = TextGenerator.from_file(sys.argv[1])
	print(generator.get_paragraph())


if __name__ == '__main__':
	main()
