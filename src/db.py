# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 01:23:19 2021

@author: sebde
"""
import chess.pgn

def format_game(game):
    mark = game.find('###') + 4
    game = game[mark:]
    game = game.replace('W', '')

    done = False
    firstB = 0
    while not done:
        firstB = game.find(' B', firstB+3)
        if firstB < 0:
            done = True
        else:
            game_sub1 = game[:firstB+1]
            game_sub2 = game[firstB+1 :]
            next_point = game_sub2.find('.')
            game_sub2 = game_sub2[next_point+1 :]
            game = game_sub1 + game_sub2
    game = game.replace('.', ' ')
    return game

def loadit(game):
    f = open('tmp/current.pgn', 'w')
    print(game, file=f)
    f.close()
    f = open('tmp/current.pgn', 'r')
    pgn = chess.pgn.read_game(f)
    return pgn

def find_all_instances(text: str, substring: str):
    indices = []
    index = 0
    while index < len(text):
        index = text.find(substring, index)
        if index == -1:
            break
        indices.append(index)
        index += len(substring)
    return indices