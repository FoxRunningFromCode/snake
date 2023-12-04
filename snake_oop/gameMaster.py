import grid_game as gg
import snake_game as sg
import time
import json
import os
import graphics_manager

#This program manages the entire program sequence of a game of snake.

def start(levels):
    
    graphics_manager.show_start_screen() # Display the welcome screen
    
    
    for i in range(1,levels+1):
        
        data = load_settings(i)
        
        graphics_manager.show_inbetween_level(i,2) #show what level youve reached.
        
        grid = gg.Grid(width=data['width'], height=data['height'])
        snake_game = sg.SnakeGame(
            data['apple_speed_enable'],
            data['appleGoal'],
            grid=grid,
            snake_head_pos=grid.center(),
            apple_pos=gg.GridPosition(13, 5),
            block_list=data['block_list'],
            
            )
    
        grid_game = gg.GridGameLoop(
            data['title'],data['titleTime'],name='Snake', grid=grid, timestep=data['timestep'], cell_length_px=30,
            game_objects=[snake_game],
            )
        snake_game.grid_game = grid_game
        
        result = grid_game.run()
        
        
        if ((result == gg.GameResult.LOST) or (result == gg.GameResult.QUIT)):
            break
            
    if result == gg.GameResult.WON:
        graphics_manager.show_ending('win',4)
        print('You won!')
    elif result == gg.GameResult.LOST:
        graphics_manager.show_ending('lost',3)
        print('You lost :(')
    elif result == gg.GameResult.QUIT:
        graphics_manager.show_ending('bye',2)
        print('Bye')
        
        
        
        
        #This part loads the config files from the json settings files. If there is none it just defaults to some values. 
        #That means i have programmed 3 levels but iof you set it to 5 levels it should auto generate some identical games to fill out the rest.
def load_settings(level_number):
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)
    
    # Construct the full file path
    file_path = os.path.join(script_directory, f'level_{level_number}_settings.json')
    
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        settings_data = json.load(file)

    # Extract values from the loaded JSON
    width = settings_data.get('width', 20)
    height = settings_data.get('height', 20)
    timestep = settings_data.get('timestep', 0.25)
    block_list = settings_data.get('block_list', [])
    apple_speed_enabled = settings_data.get('apple_speed_enabled', False)
    titletext = settings_data.get('title', "")
    titleTime = settings_data.get('titletime', 0)
    goal = settings_data.get('goal', 10)
    

    # Return the extracted values as a dictionary
    return {
        'width': width,
        'height': height,
        'timestep': timestep,
        'block_list': block_list,
        'apple_speed_enable': apple_speed_enabled,
        'title': titletext,
        'titleTime': titleTime,
        'appleGoal': goal
    }