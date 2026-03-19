# Pygame → WASM Test (Minimal)

## Goal
Verify that a basic Pygame app runs in the browser via WebAssembly without shaders or OpenGL.

## Approach
Strip the project to the simplest case:
- No shaders
- No OpenGL
- Only `pygame.draw` rendering
- Async loop for browser compatibility

## Test App
Snake game:
- Grid-based movement
- Keyboard input
- Score + game over state

## Key Adjustments

### Async Game Loop
```python
async def main():
while running:
...
await asyncio.sleep(0)
```

### CPU Rendering Only
```python
screen.fill(...)
pygame.draw.rect(...)
pygame.display.flip()
```

### Fixed-Time Movement
- Movement controlled by timer (`move_delay`)
- Independent of FPS

## Success Criteria
- Game renders in browser
- Input works
- No freezing
- No runtime errors

## Failure Indicators
- Freeze → missing async yield
- No render → WASM/canvas issue
- No input → event handling issue
- Crash → unsupported Pygame feature

## Next Step
If this works:
→ Reintroduce shaders / advanced rendering

### Full test code 
```python
import pygame
import asyncio
import random
import sys

pygame.init()

TILE_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (46, 204, 113)
FOOD_COLOR = (231, 76, 60)
TEXT_COLOR = (255, 255, 255)

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 28)


def spawn_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


def reset_game():
    snake = [(10, 10), (9, 10), (8, 10)]
    dx, dy = 1, 0
    food = spawn_food(snake)
    score = 0
    return snake, dx, dy, food, score


async def main():
    snake, dx, dy, food, score = reset_game()

    running = True
    game_over = False
    move_timer = 0
    move_delay = 100

    while running:
        dt = clock.tick(60)
        move_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    snake, dx, dy, food, score = reset_game()
                    game_over = False
                    move_timer = 0
                else:
                    if event.key == pygame.K_UP and dy != 1:
                        dx, dy = 0, -1
                    elif event.key == pygame.K_DOWN and dy != -1:
                        dx, dy = 0, 1
                    elif event.key == pygame.K_LEFT and dx != 1:
                        dx, dy = -1, 0
                    elif event.key == pygame.K_RIGHT and dx != -1:
                        dx, dy = 1, 0

        if not game_over and move_timer >= move_delay:
            move_timer = 0

            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                    new_head in snake):
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)
                    move_delay = max(50, 100 - (score // 5) * 10)
                else:
                    snake.pop()

        # Render directly to screen — no OpenGL, no textures, no shaders
        screen.fill(BG_COLOR)

        pygame.draw.rect(screen, FOOD_COLOR,
                         (food[0] * TILE_SIZE, food[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for i, segment in enumerate(snake):
            color = (100, 230, 150) if i == 0 else SNAKE_COLOR
            pygame.draw.rect(screen, color,
                             (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        score_surf = small_font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (5, 5))

        if game_over:
            go_surf = font.render("GAME OVER", True, FOOD_COLOR)
            restart_surf = small_font.render("Press any key to restart", True, TEXT_COLOR)
            screen.blit(go_surf, go_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
```