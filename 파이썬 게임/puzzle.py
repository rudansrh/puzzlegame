from collections import deque

def showmap(smap):
    for i in range(len(smap)):
        for j in range(len(smap[i])):
            print(smap[i][j], end = " ")
        print()

def checkmap(grid, start, des):
    minimum = []
    # 방향: 북, 동, 남, 서 (시계 방향)
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    n, m = len(grid), len(grid[0])  # grid 크기
    sx, sy = start[0],start[1]
    dx, dy = des[0], des[1]
    queue = deque([[sx, sy, 0, [0,0]]])  # (x, y, 회전 수, 이전 방향)
    
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
            
stage1 = [[1,1],[2,3],[3,2]]

map = stage1
checking = len(map)*len(map[0])
for i in range(len(map)): #맵 외각 설정
    map[i].insert(0,0)
    map[i].append(0)
map.insert(0,[0 for _ in range(len(map[0]))])
map.append([0 for _ in range(len(map[0]))])

running = True
nowcheck = 0
checkpoint = []
checkthing = 0
while running:
    showmap(map)
    if nowcheck == 1:
        print(checkpoint)
    try:
        x,y = input().split()
        x = int(x)
        y = int(y)
        test = 1/map[x][y]
    except:
        print("error")
        continue
    nowcheck += 1
    if nowcheck == 1: #처음 선택시 초기화
        checkpoint = [x,y]
        checkthing = map[x][y]
    elif nowcheck == 2 and checkthing != map[x][y]: #다른 아이템 선택시 초기화
        nowcheck -= 1
        checkpoint = [x,y]
        checkthing = map[x][y]
    elif nowcheck == 2 and checkthing == map[x][y]:
        cmap = [] #확인용 맵
        s=[x,y]
        e=[checkpoint[0], checkpoint[1]]
        for i in range(len(map)):
            cmap.append([])
            a = 0
            for j in range(len(map[0])):
                if map[i][j] == 0:
                    a = 4
                else: 
                    a = -1
                cmap[i].append(a)
        cmap[x][y] = 4
        cmap[checkpoint[0]][checkpoint[1]] = 4
        mini = checkmap(cmap,s,e)
        if len(mini) == 0:
            print("실패")
        elif min(mini) <= 3:
            map[x][y] = 0
            map[checkpoint[0]][checkpoint[1]] = 0
            checking -= 2
        else :
            print("실패")
        nowcheck = 0
        checkpoint = []
        checkthing = 0
        if checking == 0:
            print("성공")
            break