# Software Shaders in Pygame

## What is a "Software Shader"?
In traditional graphics programming, a **shader** is a small program (written in GLSL/HLSL) that runs on the **GPU** (Hardware). 

A **software shader** is a simulated visual effect that runs entirely on the **CPU** using standard Python code. Instead of passing the screen to the graphics card to apply effects, you manually manipulate pixels, draw semi-transparent shapes, or use blending modes on a `pygame.Surface`.

A perfect example of a software shader is the `apply_shader_effect` function in this project, which manually draws dark lines (scanlines) and rectangles (vignette) frame by frame.

---

## Pros of Software Shaders

1. **100% Compatibility:** Because it relies only on Pygame's standard 2D drawing API, it will run on any machine, OS, or browser (via Pygbag) that supports Pygame. No WebGL or OpenGL context configuration is required.
2. **No Extra Dependencies:** You don't need `moderngl`, `PyOpenGL`, or any knowledge of the C-like GLSL language. It is pure Python.
3. **Simple to Debug:** If an effect looks wrong, you can `print()` variables or use standard Python debuggers. You cannot easily `print()` from inside a GPU shader.

---

## Cons of Software Shaders

1. **Extremely Slow (CPU Bound):** The GPU is built with thousands of cores designed to calculate millions of pixels simultaneously. The CPU processes tasks sequentially. Looping over pixels in Python (or even drawing hundreds of lines per frame) will quickly cause your framerate to plummet.
2. **WebAssembly Penalty:** When compiled to the browser via Pygbag, Python code runs slightly slower than native desktop Python. Heavy CPU math for visual effects will lag noticeably in the browser.
3. **Limited Complexity:** Advanced effects like bloom, chromatic aberration, or dynamic lighting require reading and modifying surrounding pixels. Doing this mathematically in pure Python at 60 FPS is nearly impossible for high resolutions.

---

## Better Techniques for Software Effects in Pygame

If you want to stick to CPU rendering but need better performance, here are some Pygame tricks:

### 1. Pre-rendering (Surface Caching)
Instead of calculating the effect every frame, calculate it once before the game loop starts.
*Example:* Generate the vignette and scanlines onto a transparent `pygame.Surface` during startup. Inside the game loop, just `screen.blit(cached_surface, (0, 0))`. This is hundreds of times faster than drawing the lines every frame!

### 2. Pygame Blending Modes
Pygame surfaces support special flags like `pygame.BLEND_RGBA_MULT`, `pygame.BLEND_RGBA_ADD`, and `pygame.BLEND_RGBA_SUB`. 
You can create "lighting" by blitting a white circle with fading transparency onto a dark surface using `BLEND_RGBA_ADD`.

### 3. Pygame Surfarray / NumPy
If you must manipulate raw pixels, never use nested `for` loops in Python. Use `pygame.surfarray` combined with the `numpy` library. 
NumPy performs array math in highly optimized C code. You can extract the screen pixels into a NumPy array, apply a mathematical tint or distortion to the entire array at once, and push it back to the screen. 
*(Note: NumPy is a heavy dependency for Pygbag browser builds, though it is supported!)*

---

## The Verdict for Web Games
For simple, static overlays (like a CRT grid or vignette), **Software Shaders with Pre-rendering (Caching)** are fantastic and perfectly safe for Pygbag.

However, for dynamic, time-based, or complex visual manipulations (like water ripples, glowing pulses, or chromatic aberration), **Hardware Shaders (WebGL/ModernGL)** are the only viable path to maintain 60 FPS in a web browser.
