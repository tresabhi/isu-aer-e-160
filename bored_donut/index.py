import math
import os

SIZE = 35
OUTER_RADIUS = int(SIZE / 2)
INNER_RADIUS = int(OUTER_RADIUS / 4)

index = 0

while True:
  os.system('cls')

  for y in range(int(-SIZE / 2), int(SIZE / 2)):
    row = ''

    for x in range(int(-SIZE / 2), int(SIZE / 2)):
      hypot = math.hypot(y, x * math.sin(index * math.pi / 180))
      row += '##' if hypot <= OUTER_RADIUS and hypot >= INNER_RADIUS else '  '

    print(row)

  index += 1
