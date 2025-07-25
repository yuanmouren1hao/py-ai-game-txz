import pygame
import sys

# 初始化pygame
pygame.init()

# 设置字体
def get_font(size):
    try:
        return pygame.font.SysFont('SimHei', size)  # 尝试使用中文字体
    except:
        return pygame.font.SysFont(None, size)  # 如果不可用，使用默认字体

# 游戏常量
TILE_SIZE = 60

# 加载玩家图片
try:
    player_image = pygame.image.load('player.png')
    player_image = pygame.transform.scale(player_image, (TILE_SIZE - 10, TILE_SIZE - 10))  # 调整图片大小
except pygame.error:
    player_image = None  # 如果图片加载失败，使用默认图形
SCREEN_WIDTH = 9 * TILE_SIZE
SCREEN_HEIGHT = 9 * TILE_SIZE
FPS = 60

# 颜色
BACKGROUND = (40, 40, 80)
WALL_COLOR = (100, 60, 40)
FLOOR_COLOR = (210, 200, 180)
PLAYER_COLOR = (30, 150, 200)
BOX_COLOR = (200, 150, 40)
TARGET_COLOR = (180, 80, 80)
TARGET_FILLED_COLOR = (60, 180, 100)
TEXT_COLOR = (240, 240, 240)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("推箱子游戏 (Sokoban)")
clock = pygame.time.Clock()

# 游戏元素符号
WALL = '#'
PLAYER = '@'
BOX = '$'
TARGET = '.'
FLOOR = ' '
BOX_ON_TARGET = '*'
PLAYER_ON_TARGET = '+'

# 游戏地图 (9x9)
level = [
    "#########",
    "#   #   #",
    "#   $   #",
    "#  $@#  #",
    "#   $   #",
    "# ..#   #",
    "#  .#   #",
    "#   #   #",
    "#########"
]

# 游戏状态
player_pos = None
boxes = []
targets = []
walls = []

# 移动方向向量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 初始化游戏地图
def init_game():
    global player_pos, boxes, targets, walls
    player_pos = None
    boxes = []
    targets = []
    walls = []
    
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            if cell == PLAYER or cell == PLAYER_ON_TARGET:
                player_pos = [x, y]
            if cell == BOX:
                boxes.append([x, y])
            if cell == TARGET or cell == PLAYER_ON_TARGET or cell == BOX_ON_TARGET:
                targets.append([x, y])
            if cell == WALL:
                walls.append([x, y])

# 检查位置是否是墙壁
def is_wall(pos):
    return pos in walls

# 检查位置是否是箱子
def is_box(pos):
    return pos in boxes

# 移动玩家
def move_player(direction):
    global player_pos, boxes
    
    dx, dy = direction
    new_pos = [player_pos[0] + dx, player_pos[1] + dy]
    
    # 如果前面是墙壁，不能移动
    if is_wall(new_pos):
        return
    
    # 如果前面是箱子
    if is_box(new_pos):
        # 检查箱子后面是什么
        box_new_pos = [new_pos[0] + dx, new_pos[1] + dy]
        
        # 如果箱子后面是墙壁或另一个箱子，不能移动
        if is_wall(box_new_pos) or is_box(box_new_pos):
            return
        
        # 移动箱子
        for box in boxes:
            if box == new_pos:
                box[0] += dx
                box[1] += dy
                break
    
    # 移动玩家
    player_pos[0] += dx
    player_pos[1] += dy

# 检查游戏是否胜利
def check_win():
    for box in boxes:
        if box not in targets:
            return False
    return True

# 初始化游戏
init_game()

# 绘制游戏元素
def draw_game():
    # 绘制背景
    screen.fill(BACKGROUND)
    
    # 绘制地板
    for y in range(9):
        for x in range(9):
            pygame.draw.rect(screen, FLOOR_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (190, 180, 160), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    
    # 绘制目标点
    for x, y in targets:
        pygame.draw.circle(screen, TARGET_COLOR, 
                          (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                          TILE_SIZE // 4)
    
    # 绘制墙壁
    for x, y in walls:
        pygame.draw.rect(screen, WALL_COLOR, 
                         (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (70, 40, 20), 
                         (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
        # 墙壁纹理
        for i in range(3):
            pygame.draw.line(screen, (120, 80, 50), 
                            (x * TILE_SIZE + 10 + i*15, y * TILE_SIZE + 5),
                            (x * TILE_SIZE + 10 + i*15, y * TILE_SIZE + TILE_SIZE - 5), 2)
    
    # 绘制箱子
    for x, y in boxes:
        pygame.draw.rect(screen, BOX_COLOR, 
                         (x * TILE_SIZE + 5, y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
        pygame.draw.rect(screen, (170, 120, 20), 
                         (x * TILE_SIZE + 5, y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10), 3)
        # 箱子在目标点上
        if [x, y] in targets:
            pygame.draw.circle(screen, TARGET_FILLED_COLOR, 
                              (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                              TILE_SIZE // 6)
    
    # 绘制玩家
    x, y = player_pos
    if player_image is not None:
        # 使用图片绘制玩家
        screen.blit(player_image, (x * TILE_SIZE + 5, y * TILE_SIZE + 5))
    else:
        # 如果图片加载失败，使用默认圆形
        pygame.draw.circle(screen, PLAYER_COLOR, 
                          (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                          TILE_SIZE // 3)
        
        # 玩家眼睛
        pygame.draw.circle(screen, (240, 240, 240), 
                          (x * TILE_SIZE + TILE_SIZE // 2 + 8, y * TILE_SIZE + TILE_SIZE // 2 - 8), 
                          6)
        pygame.draw.circle(screen, (30, 30, 30), 
                          (x * TILE_SIZE + TILE_SIZE // 2 + 10, y * TILE_SIZE + TILE_SIZE // 2 - 8), 
                          3)
    
    # 绘制游戏标题和说明
    font = get_font(28)
    title = font.render("推箱子游戏", True, TEXT_COLOR)
    controls = font.render("方向键移动, R重置", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
    screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 30))
    
    # 如果胜利显示胜利信息
    if check_win():
        win_font = get_font(64)
        win_text = win_font.render("胜利!", True, (100, 255, 100))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2 - win_text.get_height() // 2))

# 游戏主循环
running = True
game_won = False

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_won:
                if event.key == pygame.K_UP:
                    move_player(UP)
                elif event.key == pygame.K_DOWN:
                    move_player(DOWN)
                elif event.key == pygame.K_LEFT:
                    move_player(LEFT)
                elif event.key == pygame.K_RIGHT:
                    move_player(RIGHT)
            
            # 重置游戏
            if event.key == pygame.K_r:
                init_game()
                game_won = False
    
    # 检查游戏胜利
    game_won = check_win()
    
    # 绘制游戏
    draw_game()
    
    # 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()