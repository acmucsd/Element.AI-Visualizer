
# pygame.surfarray as surfarray
from pygame.examples.arraydemo import surfdemo_show
import sys
import json
import numpy as np

from visualizer import Visualizer

f = open('test.json')
data = json.load(f)

first_obs = np.array(data['observations'][0]['board']['board_state'])
map_size = first_obs.shape[0]
py_visualizer = Visualizer(map_size)
py_visualizer.init_window()
for obs in data['observations']:

    grid = np.array(obs['board']['board_state'])
    player_num_grid = np.array(obs['board']['players_state'])
    num_agents = len(obs.keys()) - 1

    heads = []
    for key in obs.keys():
        if key != 'board':
            heads.append(obs[key]['head'])

    py_visualizer.update_scene(grid, player_num_grid, num_agents, heads)
    py_visualizer.render()
