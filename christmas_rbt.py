import turtle
import random
import time
import math
import os

# --- 0. 音乐播放模块 (新增) ---
def play_bgm():
    """尝试播放MP3音乐，如果失败则静默运行，防止报错"""
    try:
        import pygame
        pygame.mixer.init()
        # 假设音乐文件名为 music.mp3
        music_file = "05 첫 눈（The First Snow）.mp3"
        
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5) # 音量 0.5
            pygame.mixer.music.play(-1) # -1 表示无限循环
            print(f"♪ Music playing: {music_file}")
        else:
            print(f"Warning: '{music_file}' not found. Running without music.")
    except ImportError:
        print("Error: 'pygame' module not installed. Run 'pip install pygame' for music.")
    except Exception as e:
        print(f"Music error: {e}")

# --- 1. 配置区域 ---
BG_COLOR = "#0F1020"     # 深邃夜空
TINSEL_COLOR = "#FFD700" # 金色
RED_NODE_FILL = "#DC143C"    # 猩红
BLACK_NODE_FILL = "#111111"  # 纯黑
MAX_OPEN_GIFTS = 3
FONT_MAIN = ("Verdana", 16, "bold")
FONT_TITLE = ("Times New Roman", 30, "bold italic")
FONT_WISH = ("Courier New", 14, "bold") 

# --- 2. 极客许愿池 ---
WISH_POOL = [
    "Perfect Black-Height Balance",      
    "O(log n) Success Speed",            
    "Zero Segmentation Faults",          
    "Root Access to Happiness",          
    "No Rebalancing Needed",             
    "Offer = True; Salary++",            
    "Optimization: 100% Completed",      
    "Bug-Free New Year",                 
    "High Availability Friendship",      
    "Garbage Collection: Bad Luck",      
    "Steady State Reached",              
    "Connection Keep-Alive"              
]
random.shuffle(WISH_POOL)

screen = turtle.Screen()
screen.setup(width=1000, height=800)
screen.bgcolor(BG_COLOR)
screen.title("Christmas RBT: Music & Random Santa")
screen.tracer(0) 

# --- 3. 画笔初始化 ---
def create_turtle(color, speed=0):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(speed)
    t.color(color)
    return t

main_t = create_turtle("white")    # 树
snow_t = create_turtle("white")    # 雪
santa_t = create_turtle("red")     # 圣诞老人
ui_t = create_turtle("#FFD700")    # UI
status_t = create_turtle("white")  # 状态栏
effect_t = create_turtle("cyan")   # 特效

gift_hitboxes = []
gifts_opened_count = 0
game_started = False 

# --- 4. 绘图辅助函数 ---
def jump_to(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_star(t, x, y, size, color):
    jump_to(t, x - size/2, y + size/5)
    t.color(color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

def draw_gift_box(t, x, y, box_size=26):
    half = box_size / 2
    jump_to(t, x - half, y - half)
    t.color("#FF4500") 
    t.begin_fill()
    for _ in range(4):
        t.forward(box_size)
        t.left(90)
    t.end_fill()
    t.color("#FFD700"); t.pensize(3)
    jump_to(t, x, y - half); t.setheading(90); t.forward(box_size)
    jump_to(t, x - half, y); t.setheading(0); t.forward(box_size)
    jump_to(t, x, y + half)
    t.begin_fill(); t.circle(4); t.end_fill()

# --- 5. 随机轨迹圣诞老人 (含四腿动画) ---

santa_params = {
    'x': -600, 'amp': 50, 'freq': 100, 'y_base': 250, 'active': False
}

def randomize_santa_path():
    """每次调用都会生成完全不同的随机轨迹参数"""
    santa_params['x'] = -600
    # 随机波浪高度 (30到100像素之间)
    santa_params['amp'] = random.randint(30, 100)      
    # 随机波浪频率 (越小越密集)
    santa_params['freq'] = random.randint(70, 160)    
    # 随机基准高度 (天上不同高度飞过)
    santa_params['y_base'] = random.randint(100, 350) 
    santa_params['active'] = True

def draw_fancy_santa(t, x, y, tilt_angle):
    t.setheading(tilt_angle)
    # 步态动画计算
    walk_cycle = x * 0.2
    leg_swing_1 = 25 * math.sin(walk_cycle) 
    leg_swing_2 = 25 * math.sin(walk_cycle + math.pi) 
    
    deer_x, deer_y = x + 70, y + 10
    
    # 驯鹿后腿
    t.pensize(3); t.color("#5C4033") 
    jump_to(t, deer_x - 5, deer_y); t.setheading(tilt_angle - 90 + leg_swing_2); t.forward(18); t.backward(3)
    jump_to(t, deer_x + 8, deer_y); t.setheading(tilt_angle - 90 + leg_swing_1); t.forward(18); t.backward(3)

    # 驯鹿身
    jump_to(t, deer_x, deer_y); t.color("#8B4513"); t.begin_fill(); t.circle(12); t.end_fill() 

    # 驯鹿前腿
    t.color("#8B4513")
    jump_to(t, deer_x - 5, deer_y); t.setheading(tilt_angle - 90 + leg_swing_1); t.forward(18)
    jump_to(t, deer_x + 8, deer_y); t.setheading(tilt_angle - 90 + leg_swing_2); t.forward(18)

    # 头与角
    jump_to(t, deer_x + 22, deer_y + 22); t.begin_fill(); t.circle(8); t.end_fill() 
    jump_to(t, deer_x + 28, deer_y + 20); t.color("red"); t.dot(6) 
    t.color("#D2691E"); t.pensize(2)
    start = (deer_x + 22, deer_y + 28)
    jump_to(t, *start); t.setheading(tilt_angle + 60); t.forward(12)
    jump_to(t, *start); t.setheading(tilt_angle + 110); t.forward(10)

    # 雪橇
    sleigh_x, sleigh_y = x - 40, y
    t.color("#B22222"); jump_to(t, sleigh_x - 10, sleigh_y)
    t.begin_fill(); t.setheading(tilt_angle)
    t.forward(50); t.left(120); t.forward(30); t.left(60); t.forward(35); t.left(60); t.forward(30); t.end_fill()
    t.color("#C0C0C0"); t.pensize(3); jump_to(t, sleigh_x - 20, sleigh_y - 10)
    t.setheading(tilt_angle); t.forward(70); t.circle(10, 90)

    # 缰绳 (修复连接点)
    t.color("#FFD700"); t.pensize(1)
    jump_to(t, sleigh_x + 20, sleigh_y + 20) 
    t.goto(deer_x + 10, deer_y + 10)         

    # 圣诞老人
    seat_x, seat_y = sleigh_x + 10, sleigh_y + 15
    jump_to(t, seat_x, seat_y); t.color("red"); t.begin_fill(); t.circle(14); t.end_fill()
    jump_to(t, seat_x, seat_y + 18); t.color("white"); t.begin_fill(); t.circle(10); t.end_fill()
    jump_to(t, seat_x - 5, seat_y + 28); t.color("red"); t.begin_fill(); t.setheading(tilt_angle + 10)
    t.forward(20); t.right(100); t.forward(20); t.right(160); t.forward(10); t.end_fill()

# --- 6. 动画系统 ---

snowflakes = [{'x': random.randint(-500, 500), 'y': random.randint(-400, 400), 
               'speed': random.randint(2, 5), 'size': random.randint(2, 5)} for _ in range(100)]

def update_snow():
    snow_t.clear(); snow_t.penup()
    for flake in snowflakes:
        flake['y'] -= flake['speed']
        flake['x'] += math.sin(flake['y'] * 0.05) * 0.5 
        if flake['y'] < -400:
            flake['y'] = random.randint(400, 420); flake['x'] = random.randint(-500, 500)
        snow_t.goto(flake['x'], flake['y']); snow_t.dot(flake['size'])
    screen.update()
    screen.ontimer(update_snow, 50)

def update_santa():
    if not santa_params['active']: return
    
    if santa_params['x'] > 600:
        santa_params['active'] = False
        return 
    
    santa_t.clear()
    santa_params['x'] += 8
    
    # 使用随机生成的 amp 和 freq 计算轨迹
    offset_y = santa_params['amp'] * math.sin(santa_params['x'] / santa_params['freq'])
    current_y = santa_params['y_base'] + offset_y
    tilt = -20 * math.cos(santa_params['x'] / santa_params['freq'])
    
    draw_fancy_santa(santa_t, santa_params['x'], current_y, tilt)
    screen.update()
    screen.ontimer(update_santa, 50)

# --- 7. 红黑树逻辑 ---
def draw_tree_recursive(node, x, y, h_gap, v_gap):
    if node is None:
        draw_gift_box(main_t, x, y)
        box_pad = 20
        gift_hitboxes.append((x - box_pad, y - box_pad, x + box_pad, y + box_pad))
        screen.update()
        return

    color, left, right = node[0], node[1], node[2]
    next_y = y - v_gap
    next_h_gap = h_gap / 2
    
    main_t.pensize(2); main_t.color(TINSEL_COLOR)
    jump_to(main_t, x, y); main_t.goto(x - h_gap, next_y + 15)
    jump_to(main_t, x, y); main_t.goto(x + h_gap, next_y + 15)
    screen.update()
    
    draw_tree_recursive(left, x - h_gap, next_y, next_h_gap, v_gap)
    draw_tree_recursive(right, x + h_gap, next_y, next_h_gap, v_gap)

    if color == 'Root':
        draw_star(main_t, x, y, 60, TINSEL_COLOR)
    else:
        fill_c = RED_NODE_FILL if color == 'R' else BLACK_NODE_FILL
        border_c = "#FF6347" if color == 'R' else "#555555"
        jump_to(main_t, x, y - 20); main_t.color(border_c, fill_c)
        main_t.begin_fill(); main_t.circle(20); main_t.end_fill()

# --- 8. 交互与UI ---
def update_status_bar(text, color=TINSEL_COLOR):
    status_t.clear(); jump_to(status_t, 0, 340)
    status_t.color(color); status_t.write(text, align="center", font=FONT_MAIN)

def show_popup_wish(x, y, text):
    effect_t.penup(); effect_t.goto(x, y)
    for _ in range(12):
        effect_t.color(random.choice(["#FF00FF", "#00FFFF", "#FFFF00"]))
        effect_t.forward(40); effect_t.backward(40); effect_t.left(30)
    
    ui_t.clear()
    jump_to(ui_t, -220, 30); ui_t.color("gold", "#222222")
    ui_t.begin_fill()
    for _ in range(2):
        ui_t.forward(440); ui_t.right(90); ui_t.forward(100); ui_t.right(90)
    ui_t.end_fill()
    
    jump_to(ui_t, 0, -40); ui_t.color("#00FF00") 
    ui_t.write(text, align="center", font=FONT_WISH)

def trigger_final_celebration():
    ui_t.clear()
    update_status_bar("All Gifts Opened! Happy Holidays!", "#00FF7F")
    
    jump_to(ui_t, 0, -100); ui_t.color(TINSEL_COLOR)
    ui_t.write("Merry Christmas!", align="center", font=FONT_TITLE)
    jump_to(ui_t, 0, -150); ui_t.color("white")
    ui_t.write("May your tree always be balanced.", align="center", font=("Verdana", 14, "italic"))

    randomize_santa_path() # 生成随机轨迹
    screen.ontimer(update_santa, 100)

def on_click(x, y):
    global gifts_opened_count
    if not game_started: return
    if gifts_opened_count >= MAX_OPEN_GIFTS: return

    hit_index = -1
    for i, box in enumerate(gift_hitboxes):
        if box[0] <= x <= box[2] and box[1] <= y <= box[3]:
            hit_index = i; break
    
    if hit_index != -1:
        gift_hitboxes.pop(hit_index)
        gifts_opened_count += 1
        wish = WISH_POOL.pop() if WISH_POOL else "Stack Overflow"
        show_popup_wish(0, 0, wish)
        
        left = MAX_OPEN_GIFTS - gifts_opened_count
        if left > 0:
            update_status_bar(f"Unwrap {left} more gifts from the tree!")
        else:
            screen.ontimer(trigger_final_celebration, 1500)

def start_gift_phase():
    global game_started
    game_started = True
    update_status_bar(f"Mission: Find & Click {MAX_OPEN_GIFTS} Gifts on the Tree!")
    ui_t.clear()

# --- 9. 主程序 ---
# --- 修正后的红黑树结构 ---
# 结构: [颜色, 左子树, 右子树]
# 'B' 代表黑色节点, 'R' 代表红色节点

# 第3层: 红色节点，它们下面挂着礼物 (None)
L3_node = ['R', None, None]

# 第2层: 黑色节点，每个黑节点下有两个红节点
L2_node = ['B', L3_node, L3_node]

# 第1层: 红色节点，每个红节点下有两个黑节点
L1_node = ['R', L2_node, L2_node]

# 第0层: 根节点 (Root 视为黑)
mock_rbt = ['Root', L1_node, L1_node]

def main():
    play_bgm() # 播放音乐
    update_snow()
    draw_tree_recursive(mock_rbt, 0, 250, 260, 90)
    
    jump_to(ui_t, 0, 0); ui_t.color(TINSEL_COLOR)
    ui_t.write("Merry Christmas!", align="center", font=FONT_TITLE)
    jump_to(ui_t, 0, -40); ui_t.color("white")
    ui_t.write("Red-Black Tree Edition", align="center", font=("Verdana", 12, "normal"))
    
    screen.ontimer(start_gift_phase, 3000)
    screen.onclick(on_click)
    turtle.mainloop()

if __name__ == "__main__":
    main()