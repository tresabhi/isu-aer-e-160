import os
import keyboard

RESOLUTION_X = 64
RESOLUTION_Y = 48

GROUND_LEVEL = 36
GRAVITY = -0.1

PLAYER_WIDTH = 2
PLAYER_HEIGHT = 4
PLAYER_MIN_Y = GROUND_LEVEL - PLAYER_HEIGHT
PLAYER_MAX_X = RESOLUTION_X - PLAYER_WIDTH - 2
playerX = 16
playerY = PLAYER_MIN_Y
playerVelocity = 0

FULL_TILE = '██'
FULL_TILE_LIGHT = '░░'
FULL_TILE_MEDIUM = '▒▒'
FULL_TILE_DARK = '▓▓'

def fragment(x: int, y: int):
  if x == 0 or y == 0 or x == RESOLUTION_X - 1 or y == RESOLUTION_Y - 1: return FULL_TILE_LIGHT
  if y > GROUND_LEVEL: return FULL_TILE_MEDIUM
  if x >= playerX and x <= playerX + PLAYER_WIDTH and y >= playerY and y <= playerY + PLAYER_HEIGHT: return FULL_TILE
  
  return '  '

def render():
  os.system('cls')
  
  for y in range(RESOLUTION_Y):
    row = ''

    for x in range(RESOLUTION_X):
      row += fragment(x, y)
    
    print(row)

def physics():
  global playerY, playerVelocity

  # minus velocity because upside down y axis
  playerY = min(playerY - playerVelocity, PLAYER_MIN_Y)
  playerVelocity += GRAVITY

  if (playerY == PLAYER_MIN_Y): playerVelocity = 0

def inputs():
    global playerX, playerY, playerVelocity

    if playerY == PLAYER_MIN_Y and keyboard.is_pressed('w'): playerVelocity += 2
    if keyboard.is_pressed('s'): playerVelocity -= 1
    if keyboard.is_pressed('a'): playerX -= 1
    if keyboard.is_pressed('d'): playerX += 1

    playerX = min(max(playerX, 1), PLAYER_MAX_X)

while True:
  inputs()
  physics()
  render()
