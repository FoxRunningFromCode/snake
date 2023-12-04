import time
from dataclasses import dataclass
from enum import Enum
from abc import ABC
import functools

import cv2
import numpy as np


@dataclass
class GridPosition:
    x: int
    y: int

    def __add__(self, other):
        return GridPosition(x=self.x + other.x, y=self.y + other.y)


@dataclass
class Grid:
    width: int
    height: int

    def center(self):
        return GridPosition(x=self.width // 2, y=self.height // 2)


class GameResult(Enum):
    WON = 'won'
    LOST = 'lost'
    QUIT = 'quit'


class GameObject(ABC):
    def draw(self, img: np.ndarray, cell_length_px: int, coordinates_list: list[list[int]]):
        pass

    def on_key(self, key: int):
        pass

    def on_step(self) -> GameResult | None:
        pass


class GridGameLoop:
    def __init__(self, titlescreen: str, titletime: int, name: str, grid: Grid, cell_length_px: int, timestep: float,
                 game_objects: list[GameObject], coordinates_list: list[list[int]] = None,):
        self.name = name
        self.grid = grid
        self.cell_length_px = cell_length_px
        self.timestep = timestep
        self.game_objects = game_objects
        self.coordinates_list = coordinates_list if coordinates_list is not None else []
        self.title = titlescreen
        self.titletime = titletime
        self.starttime = time.time()
        
    
        
    
        
        
                
    def run(self):
        time_last_step = time.time()
        while True:
            # draw current state
            img_height = self.grid.height * self.cell_length_px
            img_width = self.grid.width * self.cell_length_px
            img = np.zeros(shape=(img_height, img_width, 3), dtype=np.float32)
            for object in self.game_objects:
                object.draw(img, cell_length_px=self.cell_length_px, block_list=self.coordinates_list)
                
            #draw title during start:
            if (self.starttime + self.titletime > time.time()):
                org = (50,50)
                color = (1.0,0,0)
                cv2.putText(img,self.title,org,cv2.FONT_HERSHEY_SIMPLEX,0.5, color,1, cv2.LINE_AA)
                
            
                
                
            cv2.imshow(self.name, img)

            # pass key input to game objects and control timing
            while time.time() - time_last_step < self.timestep:
                key = cv2.waitKey(1)
                if key == ord('q'):
                    return GameResult.QUIT
                for object in self.game_objects:
                    object.on_key(key)
            time_last_step = time.time()
            
            # step
            for object in self.game_objects:
                result = object.on_step()
                if isinstance(result, GameResult):
                    return result
