from collections import namedtuple
import pygame


BOARD_LENGTH = 64
OFFSET = 8
IMAGES = ("grass", "road_4way", "road_eastnorth", "road_eastsouth", "road_hor",
          "road_northeastsouth", "road_ver", "road_westeastsouth",
          "road_westnortheast", "road_westnorth", "road_westsouthnorth",
          "road_westsouth")

DIRECTIONS = namedtuple('DIRECTIONS',
                        ['North', 'South', 'East', 'West'])(0, 1, 2, 3)


class Tile(object):
    def __init__(self, kind="empty", img="grass"):
        self.kind = kind
        self.img = img


def init_images(tiles_used):
    images = {}
    for tile in tiles_used:
        images[tile] = pygame.image.load("res/" + tile + "_tile.png").convert()
    return images


def make_board():
    spots = [[] for _ in xrange(BOARD_LENGTH)]
    for row in spots:
        for _ in xrange(BOARD_LENGTH):
            row.append(Tile())
    return spots


def display_board(screen, board, images):
    for x, row in enumerate(board):
        for y, tile in enumerate(row):
            screen.blit(images[tile.img], (x * OFFSET, y * OFFSET))
    pygame.display.update()


in_board = lambda px, py: 0 <= px < BOARD_LENGTH and 0 <= py < BOARD_LENGTH


def validate_points(points):
    return [point for point in points if in_board(*point)]


def flush_events(pygame_events):
    for event in pygame_events.get():
        if event.type == pygame.QUIT:
            return 1
    return 0


def validate_roads(points, board):
    valid_roads = []
    if points:
        for point in points:
            x, y = point
            if board[x][y].kind == "road":
                valid_roads.append(point)
        return valid_roads
    else:
        return valid_roads


def adjacent_roads(pos, board):
    x, y = pos
    points = validate_points(((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)))
    return validate_roads(points, board)


def process_mouseclick(pos, board, roads):
    x, y = pos
    process_roads((x // 8, y  // 8), board, roads)


def get_directions(pos, points):
    dirs = set()
    x, y = pos
    for point in points:
        xx, yy = point
        if x == xx:
            if y - 1 == yy:
                dirs.add(DIRECTIONS.North)
            if y + 1 == yy:
                dirs.add(DIRECTIONS.South)
        if y == yy:
            if x + 1 == xx:
                dirs.add(DIRECTIONS.East)
            if x - 1 == xx:
                dirs.add(DIRECTIONS.West)
    return dirs


def pick_road_img(dirs):
    dirs_index = 0
    if DIRECTIONS.North in dirs:
        dirs_index += 8
    if DIRECTIONS.South in dirs:
        dirs_index += 4
    if DIRECTIONS.East in dirs:
        dirs_index += 2
    if DIRECTIONS.West in dirs:
        dirs_index += 1
    return dirs_index


def process_roads(pos, board, master_roads):
    roads = adjacent_roads(pos, board)
    x, y = pos
    # If there are no roads next to this one
    if len(roads) == 0:
        board[x][y] = Tile("road", "road_hor")
    else:
        dirs = get_directions(pos, roads)
        board[x][y] = master_roads[pick_road_img(dirs)]
        for road in roads:
            n_roads = adjacent_roads(road, board)
            n_dirs = get_directions(road, n_roads)
            board[road[0]][road[1]] = master_roads[pick_road_img(n_dirs)]


def init_roads():
    return (Tile("road", "road_hor"),  # None
            Tile("road", "road_hor"),  # West
            Tile("road", "road_hor"),  # East
            Tile("road", "road_hor"),  # East, west
            Tile("road", "road_ver"),  # South
            Tile("road", "road_westsouth"),  # South, west
            Tile("road", "road_eastsouth"),  # South, east
            Tile("road", "road_westeastsouth"),  # South, east, west
            Tile("road", "road_ver"),  # North
            Tile("road", "road_westnorth"),  # North, west
            Tile("road", "road_eastnorth"),  # North, east
            Tile("road", "road_westnortheast"),  # North, east, west
            Tile("road", "road_ver"),  # North, south
            Tile("road", "road_westsouthnorth"),  # North, south, west
            Tile("road", "road_northeastsouth"),  # North, south, east
            Tile("road", "road_4way"),  # North, south, east, west
            )


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET, BOARD_LENGTH *
                                      OFFSET])
    board = make_board()

    pygame.display.set_caption("SamCity")
    pygame.display.update()

    images = init_images(IMAGES)
    roads = init_roads()

    display_board(screen, board, images)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                process_mouseclick(event.pos, board, roads)
            display_board(screen, board, images)

if __name__ == "__main__":
    main()
