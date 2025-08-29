# y = 2..3
# 9 -> 5 层（9,7,5,3,1）

def on_on_chat():
    global width, length, height, FLOOR_LOG, WALL_PLANK, CORNER_STONE, WINDOW_PANE, ROOF_PLANK, y, door_x, win_y_bottom, win_left_x, ridge_x, levels, i
    win_z = 0
    # 原点视为西南角，朝南
    agent.teleport(pos(0, 0, 0), SOUTH)
    builder.teleport_to(agent.get_position())
    builder.face(SOUTH)
    builder.set_origin()
    builder.mark()
    # 尺寸
    width = 9
    # X：0..8
    length = 7
    # Z：0..6
    height = 5
    # 墙体高度
    # 方块
    FLOOR_LOG = PLANKS_OAK
    # 地板：原木
    WALL_PLANK = STONE_BRICKS
    # 墙体：砖（或木板，随你设置）
    CORNER_STONE = LOG_OAK
    # 四角立柱
    WINDOW_PANE = LIGHT_GRAY_STAINED_GLASS
    # 窗
    ROOF_PLANK = SPRUCE_WOOD_STAIRS
    # 屋顶
    # ---- 地板 ----
    builder.teleport_to_origin()
    builder.mark()
    # (0,0,0)
    builder.shift(width - 1, 0, length - 1)
    builder.fill(FLOOR_LOG, FillOperation.REPLACE)
    # ---- 墙体 ----
    y = 1
    while y < height + 1:
        builder.teleport_to_origin()
        builder.shift(0, y, 0)
        builder.mark()
        builder.shift(0, 0, length - 1)
        builder.line(WALL_PLANK)
        builder.mark()
        builder.shift(width - 1, 0, 0)
        builder.line(WALL_PLANK)
        builder.mark()
        builder.shift(0, 0, 0 - (length - 1))
        builder.line(WALL_PLANK)
        builder.mark()
        builder.shift(0 - (width - 1), 0, 0)
        builder.line(WALL_PLANK)
        y += 1
    # ---- 四角立柱 ----
    for dx in [0, width - 1]:
        for dz in [0, length - 1]:
            builder.teleport_to_origin()
            builder.shift(dx, 0, dz)
            builder.mark()
            builder.shift(0, height - 1, 0)
            # 到 y=4
            builder.line(CORNER_STONE)
    # ---- 门：南面中间 2 格高 ----
    door_x = Math.idiv(width, 2) + 1
    # 4
    builder.teleport_to_origin()
    builder.shift(door_x, 1, 0)
    builder.place(AIR)
    builder.shift(0, 1, 0)
    builder.place(AIR)
    # ---- 南面窗：左侧 2x2，底边 y=2（更靠上，贴近标记）----
    win_y_bottom = 2
    # 南面墙
    win_left_x = 2
    # 覆盖 x = 1, 2
    # 第1行（y = 2）
    builder.teleport_to_origin()
    builder.shift(win_left_x, win_y_bottom, win_z)
    builder.place(WINDOW_PANE)
    builder.shift(1, 0, 0)
    builder.place(WINDOW_PANE)
    # 第2行（y = 3）
    builder.teleport_to_origin()
    builder.shift(win_left_x, win_y_bottom + 1, win_z)
    builder.place(WINDOW_PANE)
    builder.shift(1, 0, 0)
    builder.place(WINDOW_PANE)
    # ---- 屋顶：人字形；第一层四周外挑 1 格 ----
    ridge_x = Math.idiv(width, 2)
    # 屋脊 x
    levels = Math.idiv(width + 1, 2)
    while i <= levels - 1:
        w = width - 2 * i
        # 9,7,5,3,1
        half = Math.idiv(w - 1, 2)
        y = height + i
        # 从 y=5 开始
        x_start = ridge_x - half
        x_end = ridge_x + half
        z_start = 0
        z_end = length - 1
        # 第一层外挑 1 格（四周）
        if i == 0:
            x_start += 0 - 1
            x_end += 1
            z_start += 0 - 1
            z_end += 1
        x = x_start
        while x < x_end + 1:
            builder.teleport_to_origin()
            builder.shift(x, y, z_start)
            # 该层南端起点
            builder.mark()
            builder.shift(0, 0, z_end - z_start)
            # 北端终点
            builder.line(ROOF_PLANK)
            x += 1
        i += 1
player.on_chat("house", on_on_chat)

i = 0
levels = 0
ridge_x = 0
win_left_x = 0
win_y_bottom = 0
door_x = 0
y = 0
ROOF_PLANK = 0
WINDOW_PANE = 0
CORNER_STONE = 0
WALL_PLANK = 0
height = 0
length = 0
width = 0
FLOOR_LOG = 0