# Pygame Web + Shader Experiment

## Purpose

This project exists to explore two technical topics in game development:

1. Running a **Pygame game inside a web browser**.
2. Adding **shader-based rendering** to a Pygame project in a way that remains compatible with browser builds.

The goal is to understand how a Python game can be packaged for **HTML5 deployment** and what graphical techniques remain viable in that environment.

---

## Learning Goals

### 1. Compile a Pygame Game for the Browser

Investigate how a Pygame project can run inside a browser environment.

Current understanding:

- Browser execution requires **WebAssembly (WASM)**.
- Python must be compiled to WebAssembly.
- Tools such as **Pygbag** package a Pygame project and produce a browser-runnable build.

Target outcome:

- Build a Pygame project that runs directly in the browser.
- Upload and test the build on platforms such as itch.io.

---

### 2. Add Shader Support to a Pygame Game

Investigate how **GLSL shaders** can be used within a Pygame project while remaining compatible with WebAssembly builds.

Key questions:

- How to apply shaders to rendered layers.
- How to structure rendering passes in Pygame.
- Which libraries support shader pipelines while remaining compatible with browser environments.

Possible approaches being explored:

- **pygame-ce OpenGL support**
- Shader pipelines compatible with **WebGL**
- Conditional rendering paths if shaders are unavailable in the web build.

---

## Current Setup

Installed so far:

- **pygame-ce**

Reason:

- Drop-in replacement for pygame
- Better OpenGL integration
- More suitable for future WebAssembly export experiments

---

## Planned Work

- Build a minimal Pygame test project.
- Export the project to WebAssembly using **Pygbag**.
- Verify that the game runs in a browser.
- Experiment with shader rendering using OpenGL in pygame-ce.
- Test whether shader pipelines function in the WebAssembly build.
- Identify limitations between **OpenGL (desktop)** and **WebGL (browser)**.

---

## Expected Outcome

A small experimental project demonstrating:

- A Pygame game running in a browser.
- A rendering pipeline capable of applying shader effects.
- A documented workflow for building Python games that target WebAssembly.