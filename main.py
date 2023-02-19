
import json
import numpy as np
import cv2
from visualizer import Visualizer
import argparse

#argument parser, default is render through pygame and no output video file
parser = argparse.ArgumentParser(description="Run the Element.AI Visualizer game.")
parser.add_argument("-r", "--render", action='store_true', help="turn on pygame rendering")
parser.add_argument("-o", "--output", help="Where to output replays. Default is none and no replay is generated")
parser.add_argument("-f", "--file", help="Where to read files. Default is test.json", default="test.json")
args = parser.parse_args()

#open input json file
f = open(args.file)
data = json.load(f)

#load information about board like size
first_obs = np.array(data['observations'][0]['board']['board_state'])
map_size = first_obs.shape[0]

#initialize visualizer
py_visualizer = Visualizer(map_size)
py_visualizer.init_window()
w,h = py_visualizer.dims()

#initialize video writer
if args.output != None:
    out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'mp4v'), 5, (int(w),int(h)))

i = 0
#iterate through all observations
for obs in data['observations']:
    grid = np.array(obs['board']['board_state'])
    player_num_grid = np.array(obs['board']['players_state'])
    num_agents = len(obs.keys()) - 1

    heads = {'player_0':(-1,-1), 'player_1':(-1,-1), 'player_2':(-1,-1), 'player_3':(-1,-1)}
    #key = player_0, player_1
    for key in obs.keys():
        if key != 'board':
            heads[key] = obs[key]['head']
    #update visual scene
    rgb = py_visualizer.update_scene(grid, player_num_grid, num_agents, heads)
    #print iteration number
    i += 1
    print(i)
    #if render, update screen
    if args.render == False:
        py_visualizer.render()
    #if output file, write to output video
    if args.output != None:
        rgb = rgb.swapaxes(0, 1)
        out.write(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
#release output video
if args.output != None:
    out.release()


