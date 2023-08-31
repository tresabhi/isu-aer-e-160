import os
import keyboard
import time
import math

RESOLUTION_X = 64
RESOLUTION_Y = 48
FRAME_RATE = 30

GROUND_LEVEL = 36
GRAVITY = -900

PLAYER_WIDTH = 2
PLAYER_HEIGHT = 4
PLAYER_MIN_Y = GROUND_LEVEL - PLAYER_HEIGHT
PLAYER_MAX_X = RESOLUTION_X - PLAYER_WIDTH - 2
playerX = 16
playerY = PLAYER_MIN_Y
playerVelocity = 0

tiles = {
  0: '  ',
  1: '░░',
  2: '▒▒',
  3: '▓▓',
  4: '██',
}

currentTime = time.time()
lastTime = currentTime
deltaTime = 0

def fragment(x: int, y: int):
  if x == 0 or y == 0 or x == RESOLUTION_X - 1 or y == RESOLUTION_Y - 1: return 1
  if y > GROUND_LEVEL:
    return 2 if 3 * math.sin(x + 8 * currentTime) > (y - (RESOLUTION_Y + GROUND_LEVEL) / 2) else 1 
  if x >= playerX and x <= playerX + PLAYER_WIDTH and y >= playerY and y <= playerY + PLAYER_HEIGHT: return 4
  
  return 0

def render():
  os.system('cls')
  frame = ''

  for y in range(RESOLUTION_Y):
    frame += '\n'

    for x in range(RESOLUTION_X):
      frame += tiles[fragment(x, y)]
    
  print(frame)

def physics():
  global playerY, playerVelocity

  # minus velocity because upside down y axis
  playerY = min(playerY - (playerVelocity * deltaTime + 0.5 * GRAVITY * (deltaTime ** 2)), PLAYER_MIN_Y)
  playerVelocity += GRAVITY * deltaTime

  if (playerY == PLAYER_MIN_Y): playerVelocity = 0

def inputs():
    global playerX, playerY, playerVelocity

    if playerY == PLAYER_MIN_Y and keyboard.is_pressed('w'): playerVelocity += 200
    if keyboard.is_pressed('s'): playerVelocity -= 1000 * deltaTime
    if keyboard.is_pressed('a'): playerX -= round(100 * deltaTime)
    if keyboard.is_pressed('d'): playerX += round(100 * deltaTime)

    playerX = min(max(playerX, 1), PLAYER_MAX_X)

while True:
  time.sleep(1 / FRAME_RATE)

  lastTime = currentTime
  currentTime = time.time()
  deltaTime = currentTime - lastTime

  inputs()
  physics()
  render()
