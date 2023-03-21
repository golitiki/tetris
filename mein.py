import pygame 
import random
import copy

pygame.init()

I_max = 11
J_max = 21

screen_x = 300
screen_y = 600

screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

dx = (screen_x)/(I_max - 1)
dy = screen_y/(J_max - 1)

fps = 60
grid = []

for i in range(0, I_max):
    grid.append([])
    for j in range(0, J_max):
        grid[i].append([1])
        
for i in range(0, I_max):
    for j in range(0, J_max):
        grid[i][j].append(pygame.Rect(i*dx, j*dy, dx, dy))
        grid[i][j].append(pygame.Color("Gray"))
        
detalis = [
    [[-2,0],[-1,0],[0,0],[1,0]],
    [[-1,1],[-1,0],[0,0],[1,0]],
    [[1,1],[-1,0],[0,0],[1,0]],
    [[-1,1],[0,1],[0,0],[-1,0]],
    [[1,0],[1,1],[0,0],[-1,0]],
    [[0,1],[-1,0],[0,0],[1,0]],
    [[-1,1],[0,1],[0,0],[1,0]],
]

det = [[],[],[],[],[],[],[]]
for i in range(0, len(detalis)):
    for j in range(0,4):
        det[i].append(pygame.Rect(detalis[i][j][0]*dx + dx*(I_max//2), detalis[i][j][1]*dy, dx, dy))       

detalis = pygame.Rect(0, 0, dx, dy)
det_choice = copy.deepcopy(random.choice(det))
count = 0

game = True
rotate = False
while game:
    delta_x = 0
    delta_y = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_x = -1
            elif event.key == pygame.K_RIGHT:
                delta_x = 1
            elif event.key == pygame.K_UP:
                rotate = True
                
    key = pygame.key.get_pressed()
    
    if key[pygame.K_DOWN]:
        count = 31 * fps
                
    screen.fill(pygame.Color(0,0,0))
    
    for i in range(0, I_max):
        for j in range(0, J_max):
            pygame.draw.rect(screen,grid[i][j][2],grid[i][j][1],grid[i][j][0])

    for i in range(4):
        if ((det_choice[i].x + delta_x * dx < 0) or (det_choice[i].x + delta_x * dx >= (screen_x))):
            delta_x = 0
        if ((det_choice[i].y + dy >= screen_y) or (grid[int(det_choice[i].x//dx)][int(det_choice[i].y//dy) + 1][0] == 0)):
            delta_y = 0
            for i in range(4):
                x = int(det_choice[i].x // dx)
                y = int(det_choice[i].y // dy)
                grid[x][y][0] = 0
                grid[x][y][2] = pygame.Color(random.randint(0,255),255,255)
            detail_x = 0
            detail_y = 0
            det_choice = copy.deepcopy(random.choice(det))

    for i in range(4):
        det_choice[i].x += delta_x*dx
        
    count += fps
    if count > 30 * fps:
        for i in range(4):
            det_choice[i].y += delta_y*dy
        count = 0

    for i in range(4):
        detalis.x = det_choice[i].x
        detalis.y = det_choice[i].y
        pygame.draw.rect(screen,pygame.Color(255,255,255), detalis)
        
    c = det_choice[2]
    if rotate == True:
        for i in range(4):
            x = det_choice[i].y - c.y
            y = det_choice[i].x - c.x
            
            det_choice[i].x = c.x - x
            det_choice[i].y = c.y + y
        rotate = False
    
    for j in range(J_max -1, -1, -1):
        count_cells = 0
        for i in range(0, I_max):
            if grid[i][j][0] == 0:
                count_cells += 1
            elif grid[i][j][0] == 1:
                break
        if count_cells == (I_max - 1):
            for l in range(0, I_max):
                grid[l][0][0] = 1
            for k in range(j, -1, -1):
                for l in range(0, I_max):
                    grid[l][k][0] = grid[l][k-1][0]
                        
    pygame.display.flip()
    clock.tick(fps)              