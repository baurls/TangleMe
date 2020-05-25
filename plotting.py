#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 05:08:57 2020

@author: Lukas Baur
"""

import global_code
import matplotlib.pyplot as plt 


def save_img(path):
    plt.savefig(path, bbox_inches='tight')

def plot_board(board, board_name, iteration, show_fig=True):
    m,n = board.shape
    scale = 25
    plt.matshow(board, cmap='jet')
    save_img(global_code.IMG_OUTPUT_PATH + str(board_name) + '_' + str(iteration))
