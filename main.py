import pygame
import asyncio
import moderngl
import random
from array import array
import sys

# 1. Initialization and Constants
pygame.init()
TILE_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Add flags to the screen so the game is aware that there is a double buffer (though openGL)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
# Adding pygame.SRCALPHA ensures the surface is 32-bit (4 color channels) which matches our texture component size
display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Async Snake")
clock = pygame.time.Clock()

ctx = moderngl.create_context()

# This part defines a full-screen quad in OpenGL Normalized Device Coordinates (NDC).
# Coordinates in OpenGL are relative to the center of the screen (-1 to 1, Y goes up),
# while in Pygame, the origin (0, 0) is at the top left and Y goes down.
quad_buffer = ctx.buffer(data=array('f',[
    # position {x, y}, uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,    # topleft
    1.0, 1.0, 1.0, 0.0,     # topright
    -1.0, -1.0, 0.0, 1.0,   # bottomleft
    1.0, -1.0, 1.0, 1.0     # bottomright

]))

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 textcoord;
out vec2 uvs;

void main() {
    uvs = textcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main(){
    f_color = vec4(texture(tex, uvs).r, 0.0, 0.0, 1.0);

}
'''

# Compiles and links the vertex and fragment shaders into an OpenGL program
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# Creates a Vertex Array Object (VAO) that maps the buffer data to the shader attributes ('vert' and 'textcoord', which are both 2 floats)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'textcoord')])

# Create the texture once outside the loop to avoid severe performance issues
frame_tex = ctx.texture(display.get_size(), 4)
frame_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
frame_tex.swizzle = 'BGRA' # Swap color channels to fit between pygame and openGL

# Colors
BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (46, 204, 113)
FOOD_COLOR = (231, 76, 60)

async def main():
    # Game State Variables
    snake = [(10, 10), (9, 10), (8, 10)] # List of (x, y) grid coordinates
    dx, dy = 1, 0 # Current direction
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    running = True
  
    move_timer = 0
    move_delay = 100

    while running:
        dt = clock.tick(60) 
        move_timer += dt

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0

        # 3. Game Logic Update
        if move_timer >= move_delay:
            move_timer = 0
            
            # Calculate new head position
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # Check for collisions (walls or self)
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake):
                print("Game Over!")
                running = False 
                continue

            # Move snake forward
            snake.insert(0, new_head)

            # Check if food is eaten
            if new_head == food:
                # Spawn new food, keep tail (snake grows)
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            else:
                # Remove tail if no food eaten (maintains length)
                snake.pop() 

        # 4. Rendering
        display.fill(BG_COLOR)
        
        # Draw Food
        pygame.draw.rect(display, FOOD_COLOR, (food[0] * TILE_SIZE, food[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Draw Snake
        for segment in snake:
            pygame.draw.rect(display, SNAKE_COLOR, (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Clear OpenGL context
        ctx.clear(0.0, 0.0, 0.0)
        
        # Update the existing texture with the new frame data
        frame_tex.write(display.get_view('1'))
        frame_tex.use(0)
        program['tex'] = 0
        render_object.render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()

        # 5. Yield to Browser
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())