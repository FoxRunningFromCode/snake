import numpy as np
import cv2

import grid_game as gg
import vis
import functools



class SnakeGame(gg.GameObject):
    def __init__(self,apple_multiplier: bool, applegoal: int, grid: gg.Grid, snake_head_pos: gg.GridPosition,
                 apple_pos: gg.GridPosition, snake_body_pos: list[gg.GridPosition] = [],
                 block_list: list[list[int]] = [], timestep_callback=None):
        # game state
        #print(block_list)
        self.grid_game = None
        self.apple_goal = applegoal
        self.timestep_callback = timestep_callback
        self.score = 0
        self.snake_head_pos = snake_head_pos
        self.snake_body_pos = snake_body_pos
        self.snake_direction = gg.GridPosition(1, 0)
        self.apple_pos = apple_pos
        self.apple_multiplier = apple_multiplier
        
        self.timestep_callback = timestep_callback

        self.grid = grid        
        self.key_directions = {
            ord('w'): gg.GridPosition(0, -1), 
            ord('a'): gg.GridPosition(-1, 0), 
            ord('s'): gg.GridPosition(0, 1), 
            ord('d'): gg.GridPosition(1, 0), 
        }
        self.block_list = block_list  # Initialize an empty block list

    def draw(self, img: np.ndarray, cell_length_px: int, block_list: list[list[int]]):
        # draw apple
        vis.draw_circle(img=img, pos=self.apple_pos, color=vis.RED,
                        cell_length_px=cell_length_px, fill=True)
        # draw snake 
        vis.draw_circle(
            img=img, pos=self.snake_head_pos, color=vis.GREEN, 
            cell_length_px=cell_length_px, fill=True,
        )
        
        
        # draw wall squares at the list of coordinates.
        for pos in self.block_list:
            x, y = pos
            vis.draw_square(
                img=img, top_left=(x * cell_length_px, y * cell_length_px),
                side_length=cell_length_px, color=vis.GREY, fill=True,
            )
            
        for pos in self.snake_body_pos:
            vis.draw_circle(
                img=img, pos=pos, color=vis.GREEN, 
                cell_length_px=cell_length_px, fill=False,
            )

        # draw score
        img_height = img.shape[0]
        cv2.putText(
            img=img, text=f'score: {self.score} / {self.apple_goal}', color=vis.WHITE,
            org=(12, img_height - 12),  # bottom left, 12 px from corner
            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.,
        )
        
        

    def on_key(self, key: int):
        if key in self.key_directions:
            self.snake_direction = self.key_directions[key]

    def on_step(self):
        new_head_pos = self.snake_head_pos + self.snake_direction
    
        # check borders
        x, y = new_head_pos.x, new_head_pos.y
        if x < 0 or y < 0 or self.grid.width <= x or self.grid.height <= y:
            return gg.GameResult.LOST
        
        # check self collision
        for body_part_pos in self.snake_body_pos:
            if body_part_pos == new_head_pos:
                return gg.GameResult.LOST


    
            # eating apple and body movement
        new_body = [*self.snake_body_pos, self.snake_head_pos]
        occupied_positions = set((pos.x, pos.y) for pos in new_body) | set(tuple(pos) for pos in self.block_list)

        if new_head_pos == self.apple_pos or (new_head_pos.x, new_head_pos.y) in occupied_positions:
            # Generate a new random apple position that is not occupied
            while True:
                apple_x, apple_y = list(np.random.randint(low=(0, 0), high=(self.grid.width, self.grid.height)))
                
                if tuple(list[apple_x, apple_y]) not in occupied_positions:
                    break
            self.apple_pos = gg.GridPosition(x=apple_x, y=apple_y)
            self.score += 1
            #change speed by 20% each time an apple is eaten.
            if(self.apple_multiplier):
                self.grid_game.timestep *= 0.8
                
            
            

        else:
            new_body = new_body[1:]
            
            
            
        #check for wall collision
        for wall_pos in self.block_list:
            if (x, y) == tuple(wall_pos):
                return gg.GameResult.LOST

        #print("snakehead at:")
        #print(self.snake_head_pos)
        #print("apple pos: ")
        #print(self.apple_pos)
        #print("all occupied spaces: ")
        #print(occupied_positions)

        # update snake state
        self.snake_body_pos = new_body
        self.snake_head_pos = new_head_pos

        # check for winning
        if self.score == self.apple_goal:
            return gg.GameResult.WON

