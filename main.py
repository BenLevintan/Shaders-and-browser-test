import pygame
import asyncio
import random
import sys

# 1. Initialization and Constants
pygame.init()
TILE_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Async Snake")
clock = pygame.time.Clock()

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
    
    # Timer to control snake speed independently of frame rate
    move_timer = 0
    move_delay = 100 # Snake moves every 100 milliseconds

    while running:
        dt = clock.tick(60) # Run loop at 60 FPS
        move_timer += dt

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Prevent snake from reversing into itself
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
        screen.fill(BG_COLOR)
        
        # Draw Food
        pygame.draw.rect(screen, FOOD_COLOR, (food[0] * TILE_SIZE, food[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Draw Snake
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()

        # 5. Yield to Browser
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())