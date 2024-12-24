import pygame
import sys
from collections import deque
import time

pygame.init()

def checkmap(grid, start, des):
    minimum = []
    # 방향: 북, 동, 남, 서 (시계 방향)
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    n, m = len(grid), len(grid[0])  # grid 크기
    sx, sy = start[0],start[1]
    dx, dy = des[0], des[1]
    queue = deque([[sx, sy, 0, [0,0]]])  # x, y, 회전 수, 이전 방향
    
    while 1:
        if len(queue) == 0:
            return minimum
        x2,y2,r,pre_rot = queue.popleft()
        grid[x2][y2] = r
        if x2 == dx and y2 == dy:
            minimum.append(r)
            continue
        for i in range(4):
            nx = x2 + directions[i][0]
            ny = y2 + directions[i][1]
            # 유효한 위치인지 확인   
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != -1 and (directions[i][0] != pre_rot[0]*-1 or directions[i][1] != pre_rot[1]*-1):
                if directions[i][0] == pre_rot[0] and directions[i][1] == pre_rot[1]:
                    if r < grid[nx][ny]:
                        queue.append([nx, ny, r, pre_rot])
                elif r+1 < grid[nx][ny]:
                    queue.append([nx, ny, r+1, [directions[i][0],directions[i][1]]])

#화면 크기 설정정
screen_width = 800
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("타일 매치")

#타일
tile1 = pygame.image.load("파이썬 게임\\이미지 저장\\그림1.png")
tile2 = pygame.image.load("파이썬 게임\\이미지 저장\\그림2.png")
tile3 = pygame.image.load("파이썬 게임\\이미지 저장\\그림3.png")
tile4 = pygame.image.load("파이썬 게임\\이미지 저장\\그림4.png")
tile5 = pygame.image.load("파이썬 게임\\이미지 저장\\그림5.png")
tile6 = pygame.image.load("파이썬 게임\\이미지 저장\\그림6.png")
tile7 = pygame.image.load("파이썬 게임\\이미지 저장\\그림7.png")
tiles = [None,tile1,tile2,tile3,tile4,tile5,tile6,tile7]
check = pygame.image.load("파이썬 게임\\이미지 저장\\check.png")

wrong = pygame.image.load("파이썬 게임\\이미지 저장\\wrong.png")
wrong = pygame.transform.scale(wrong, (800,550))

myFont = pygame.font.Font("파이썬 게임\\CookieRun Regular.ttf", 30)

#색 설정
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
bgcolor = (255, 255, 200)

stages = [[[1,1],[2,3],[2,3]], #튜토리얼1
        [[3,4,3],[1,4,1]], #튜토리얼2
        [[5,4,3],[3,4,5]] #튜토리얼3
        ,[[1,2,3,1,4,1],[6,7,3,4,4,1], #1단계
        [7,3,7,4,6,2], [7,6,3,6,2,2]]]
for m in range(len(stages)):
    map = stages[m]
    checking = len(map) * len(map[0])
    
    # 맵 외각 설정
    for i in range(len(map)):
        map[i].insert(0, 0)
        map[i].append(0)
    map.insert(0, [0 for _ in range(len(map[0]))])
    map.append([0 for _ in range(len(map[0]))])
    map_x = len(map[0])
    map_y = len(map)

    for i in range(1, len(tiles)):
        # 타일 크기 계산
        tile_width = screen_width // map_x * 0.8  # 가로 타일 크기
        tile_height = screen_height // map_y * 0.8  # 세로 타일 크기
        tile_size = min(tile_width, tile_height)  # 정사각형 크기로 설정
        # 이미지를 타일 크기에 맞게 조정
        tiles[i] = pygame.transform.scale(tiles[i], (int(tile_size) * 0.9, int(tile_size)))
        
    check = pygame.transform.scale(check, (int(tile_size) * 0.9, int(tile_size) * 0.9))

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
            tilepos.append([pygame.Rect(x, y, tile_size, tile_size), i, j])

    nowcheck = 0
    checkpos = (0, 0)
    checkpoint = []
    checkthing = 0
    stage = m-2

    clock = pygame.time.Clock()
    start_tick = pygame.time.get_ticks()
    running = True
    
    while running:
        screen.fill(bgcolor)
        clock.tick(60)
        if stage <= 0:
            stageText = myFont.render(f"튜토리얼 - {stage+3}", True,black)
            screen.blit(stageText, (325, 0))
        elif stage > 0:
            elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
            timeText = myFont.render(f"{elapsed_time}", True, green)
            stageText = myFont.render(f"stage ({stage}/{len(stages)-3})", True, black)
            screen.blit(timeText, (0, 0))
            screen.blit(stageText, (325, 0))
        
        # 타일 이미지 그리기
        for i in range(map_y):
            for j in range(map_x):
                x = start_x + j * tile_size
                y = start_y + i * tile_size
                if map[i][j] != 0:
                    screen.blit(tiles[map[i][j]], (x, y))
                if nowcheck == 1 and i == checkpoint[0] and j == checkpoint[1]:
                    screen.blit(check, (x, y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for k in range(len(tilepos)):
                    if tilepos[k][0].collidepoint(mouse_pos):
                        if map[tilepos[k][1]][tilepos[k][2]] == 0:
                            break
                        tile_x = tilepos[k][1]
                        tile_y = tilepos[k][2]
                        nowcheck += 1
                        if nowcheck == 1:  # 처음 선택시 초기화
                            checkpoint = [tile_x, tile_y]
                            checkthing = map[tile_x][tile_y]
                            break
                        elif nowcheck == 2 and (checkthing != map[tile_x][tile_y] or (checkpoint[0] == tile_x and checkpoint[1] == tile_y)):
                            nowcheck -= 1
                            checkpoint = [tile_x, tile_y]
                            checkthing = map[tile_x][tile_y]
                            break
                        elif nowcheck == 2 and checkthing == map[tile_x][tile_y]:
                            cmap = []  # 확인용 맵
                            s = [tile_x, tile_y]
                            e = [checkpoint[0], checkpoint[1]]
                            for i in range(len(map)):
                                cmap.append([])
                                a = 0
                                for j in range(len(map[0])):
                                    if map[i][j] == 0:
                                        a = 4
                                    else: 
                                        a = -1
                                    cmap[i].append(a)
                            cmap[tile_x][tile_y] = 4
                            cmap[checkpoint[0]][checkpoint[1]] = 4
                            mini = checkmap(cmap, s, e)
                            print(mini)
                            if len(mini) == 0 or min(mini) > 3:
                                screen.blit(wrong, (0, 0))
                                pygame.display.flip()
                                time.sleep(0.5)
                            else:
                                map[tile_x][tile_y] = 0
                                map[checkpoint[0]][checkpoint[1]] = 0
                                checking -= 2
                            nowcheck = 0
                            checkpoint = []
                            checkthing = 0
                            if checking == 0:
                                print("성공")
                                running = False
                            break
        pygame.display.flip()
result = elapsed_time
while 1:
    screen.fill(bgcolor)
    myFont = pygame.font.Font("파이썬 게임\\CookieRun Regular.ttf", 60)
    resultText = myFont.render(f"걸린 시간 : {result}",True, blue)
    screen.blit(resultText, (180,200))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    
pygame.quit()