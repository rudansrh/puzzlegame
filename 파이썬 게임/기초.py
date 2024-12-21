import pygame

pygame.init()

#화면 크기 설정정
screen_width = 800
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("퍼즐게임")

#타일
tile1 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림1.png")
tile2 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림2.png")
tile3 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림3.png")
tile4 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림4.png")
tile5 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림5.png")
tile6 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림6.png")
tile7 = pygame.image.load("C:\\Users\\USER\\Desktop\\파이썬 게임\\이미지 저장\\그림7.png")
tiles = [None,tile1,tile2,tile3,tile4,tile5,tile6,tile7]

#색 설정
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
bgcolor = (255, 255, 200)

#맵 정하기
stage1 = [[1,1],[2,3],[2,3]]
map = stage1
map_x = len(map[0])
map_y = len(map)

for i in range(1,len(tiles)):
    # 타일 크기 계산
    tile_width = screen_width // map_x * 0.7  # 가로 타일 크기
    tile_height = screen_height // map_y * 0.7  # 세로 타일 크기
    tile_size = min(tile_width, tile_height)  # 정사각형 크기로 설정

    # 이미지를 타일 크기에 맞게 조정
    tiles[i] = pygame.transform.scale(tiles[i], (int(tile_size)*0.9, int(tile_size)))

# 중앙에 배치하기 위한 시작 좌표 계산
total_width = tile_size * map_x
total_height = tile_size * map_y
start_x = (screen_width - total_width) // 2
start_y = (screen_height - total_height) // 2

tilepos = []
for i in range(map_y):
    for j in range(map_x):
        x = start_x + j * tile_size
        y = start_y + i * tile_size
        tilepos.append(pygame.Rect(x,y,tile_size,tile_size))

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
    screen.fill(bgcolor)
    
    # 타일 이미지 그리기
    for i in range(map_y):
        for j in range(map_x):
            x = start_x + j * tile_size
            y = start_y + i * tile_size
            if map[i][j] != 0:
                screen.blit(tiles[map[i][j]], (x, y))
            
    pygame.display.flip()
    
    
pygame.quit()