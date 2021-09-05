# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 01:27:21 2021

@author: sebde
"""

import pandas as pd
import networkx as nx

from src import db

# minimum number of moves
min_moves = 10
halfmoves_to_analyze = 10
nr_games = 2000
display_threshold = 0.005
folder = 'data'
filename = 'all_with_filtered_anotations_since1998.txt'
# filename='dummy.txt'


# read file and make list of games and list of edges
colnames = ['Board_from', 'Board_to', 'FEN_from', 'FEN_to', 'game_nr', 'halfmove_nr']
edge_list = pd.DataFrame(columns=colnames)
games = []
f = open(folder + '/' + filename, 'r')
for i, game in enumerate(f):
    if i <= nr_games:
        print(f'Game {i}, extracting moves...')
        game = db.format_game(game) # removing unnecessary information
        if (game[0] == '1') and (str(min_moves) in game): # do not analyze junk lines or miniature games
            games.append(game)
            pgn = db.loadit(game)
            board = pgn.board()
            board1 = board.copy()
            fen1 = board.fen()
            limit = db.find_all_instances(fen1, ' ')[-2] #remove number of moves otherwise some positions will be considered different
            fen1 = fen1[:limit]
            for j, move in enumerate(pgn.mainline_moves()):
                if j <= halfmoves_to_analyze:
                    # print(f'Half-move {j}...')
                    board.push(move)
                    board2 = board.copy()
                    fen2 = board.fen()
                    limit = db.find_all_instances(fen2, ' ')[-2]
                    fen2 = fen2[:limit]
                    new_line = pd.Series([board1, board2, fen1, fen2, i, j], index=colnames)
                    edge_list = edge_list.append(new_line, ignore_index=True)
                    fen1 = fen2
                    board1 = board2.copy()
                else:
                    break
    else:
        break

# remove and count doublons:

net = edge_list.loc[:, ['FEN_from', 'FEN_to']]
net2 = net.groupby(net.columns.tolist()).size().reset_index().rename(columns={0:'count'}).sort_values(by='count', ascending=False)
G = nx.from_pandas_edgelist(net2[net2['count']>=(display_threshold*nr_games)], source='FEN_from', target='FEN_to', edge_attr='count')
Gc = sorted(nx.connected_components(G), key=len, reverse=True)
G_main = G.subgraph(Gc[0])
nx.draw(G_main)


































