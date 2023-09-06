import os
import keyboard
import time
import math

RESOLUTION_X = 64
RESOLUTION_Y = 48
FRAME_RATE = 30


PLAYER_WIDTH = 2
PLAYER_HEIGHT = 4
GRAVITY = -2 ** 6
PLAYER_ACCELERATION_Y = 2 ** 9
PLAYER_ACCELERATION_X = 2 ** 7
player = {
    'x': 0,
    'y': 0,
    'xVelocity': 0,
    'yVelocity': 0,
    'isOnSurface': False
}

tiles = [
    '  ',
    '░░',
    '▒▒',
    '▓▓',
    '██',
]

boxes = [
    {
        'x1': -16,
        'y1': -16,
        'x2': 16,
        'y2': 0,
        'value': 2
    },
    {
        'x1': -3,
        'y1': -2,
        'x2': 3,
        'y2': 10,
        'value': 1
    }
]

currentTime = time.time()
lastTime = currentTime
deltaTime = 0


def fragment(x: int, y: int):
  # screen border
  if x == 0 or y == 0 or x == RESOLUTION_X - 1 or y == RESOLUTION_Y - 1:
    return 1

  # player
  if x - 1 <= RESOLUTION_X / 2 <= x + PLAYER_WIDTH - 1 and y + 1 <= RESOLUTION_Y / 2 <= y + 1 + PLAYER_HEIGHT:
    return 3

  # boxes
  for box in boxes:
    if box['x1'] - player['x'] <= x - RESOLUTION_X / 2 <= box['x2'] - player['x'] and box['y1'] - player['y'] <= -y + RESOLUTION_Y / 2 <= box['y2'] - player['y']:
      return box['value']

  return 0


def render():
  os.system('cls')
  frame = ''

  for y in range(RESOLUTION_Y):
    frame += '\n'

    for x in range(RESOLUTION_X):
      frame += tiles[fragment(x, y)]

  print(f"{frame}\n\n{player['xVelocity']} {player['yVelocity']}")


def physics():
  global player, boxes

  player['isOnSurface'] = False

  for box in boxes:
    minX = min(box['x1'], box['x2'])
    maxX = max(box['x1'], box['x2'])
    minY = min(box['y1'], box['y2'])
    maxY = max(box['y1'], box['y2'])

    if player['yVelocity'] <= 0:
      bottomLeftX = player['x'] - PLAYER_WIDTH / 2
      bottomRightX = player['x'] + PLAYER_WIDTH / 2
      bottomY = player['y']

      # falling down check at the bottom of the player
      if (minX <= bottomLeftX <= maxX or minX <= bottomRightX <= maxX) and minY <= bottomY <= maxY:
        player['y'] = maxY
        player['isOnSurface'] = True

    if player['xVelocity'] > 0:
      rightX = maxX
      topRightY = player['y'] + PLAYER_HEIGHT
      bottomRightY = player['y']

      # if (minY <= topRightY <= maxY or minY <= bottomRightY <= maxY) and minX <= rightX <= maxX:
      #   player['x'] = minX


def inputs():
  global player

  if player['isOnSurface']:
    player['yVelocity'] = 0
  else:
    player['yVelocity'] += GRAVITY * deltaTime

  if player['isOnSurface'] and keyboard.is_pressed('w'):
    player['yVelocity'] += PLAYER_ACCELERATION_Y * deltaTime
  if keyboard.is_pressed('s'):
    player['yVelocity'] -= PLAYER_ACCELERATION_Y * deltaTime
  if keyboard.is_pressed('a'):
    player['xVelocity'] -= PLAYER_ACCELERATION_X * deltaTime
  if keyboard.is_pressed('d'):
    player['xVelocity'] += PLAYER_ACCELERATION_X * deltaTime

  player['x'] += player['xVelocity'] * deltaTime
  player['y'] += player['yVelocity'] * \
      deltaTime + 0.5 * GRAVITY * deltaTime ** 2

  player['xVelocity'] *= 0.8


while True:
  time.sleep(1 / FRAME_RATE)

  lastTime = currentTime
  currentTime = time.time()
  deltaTime = currentTime - lastTime

  inputs()
  physics()
  render()
