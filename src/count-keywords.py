# -*- coding: utf-8 -*-

"""
Script para contar palavras chave em um arquivo de texto.
"""

from __future__ import division, print_function, unicode_literals

import argparse
from collections import Counter

from tokenizer import tokenize
from nltk import ngrams

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+',
                        help='Arquivos de texto')
    parser.add_argument('output', help='Arquivo de saída para escrever '
                                       '(n-gramas e contagem)')
    parser.add_argument('-p', dest='keywords',
                        help='Lista com palavras e n-gramas para buscar')
    args = parser.parse_args()

    keywords = set()
    with open(args.keywords, 'r') as f:
        for line in f:
            line = line.strip().lower()

            # armazena keywords com mais de uma palavra como tuplas
            # (para ficar igual aos n-gramas do NLTK)
            if ' ' in line:
                line = tuple(line.split())

            keywords.add(line)

    counter = Counter()
    for filename in args.inputs:
        with open(filename, 'r') as f:
            for line in f:
                tokens = tokenize(line.lower())
                counter.update(tokens)

                bigrams = ngrams(tokens, 2)
                counter.update(bigrams)

                trigrams = ngrams(tokens, 3)
                counter.update(bigrams)

    keyword_counts = [(keyword, counter[keyword])
                      for keyword in keywords if keyword in counter]
    keyword_counts.sort(key=lambda t: t[1], reverse=True)

    with open(args.output, 'w') as f:
        for keyword, count in keyword_counts:
            if isinstance(keyword, tuple):
                keyword = ' '.join(keyword)

            line = '%s\t%d\n' % (keyword.title(), count)
            f.write(line)
