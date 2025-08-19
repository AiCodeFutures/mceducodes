# ===== Building parameters =====
W = 20           # width (x)
D = 20           # depth (z)
FLOORS = 3       # number of floors
FLOOR_H = 7      # height of each floor (y)
ROOF_OVERHANG = 3

def p(base, dx, dy, dz):
    return positions.add(base, pos(dx, dy, dz))

# --- stone-brick foundation, 2 layers, extend 3 blocks around ---
def build_foundation(base):
    over = 3
    blocks.fill(STONE_BRICKS,
        p(base, -over, 0, -over),
        p(base, W-1+over, 1, D-1+over),
        FillOperation.REPLACE)

# --- embed ceiling lights on a given Y plane (replace plank with lantern) ---
def embed_lights_on_plane(base2, y_plane):
    # 从墙内缩 2 格，步长 5，先"挖掉"再放灯，确保嵌入
    for x in range(2, W-2, 5):
        for z in range(2, D-2, 5):
            blocks.place(AIR,        p(base2, x, y_plane, z))
            blocks.place(SEA_LANTERN, p(base2, x, y_plane, z))

def build_building(base):
    # 1) 地基（石砖，地上两层，四周外扩 3 格）
    build_foundation(base)

    # 楼体抬高 2 格，建在地基上
    base2 = p(base, 0, 2, 0)

    # 2) 各楼层
    for level in range(FLOORS):
        y0 = level * FLOOR_H

        # 地板（金合欢木板，内缩 1 格，不贴外墙）
        blocks.fill(PLANKS_ACACIA,
            p(base2, 1, y0, 1),
            p(base2, W-2, y0, D-2),
            FillOperation.REPLACE)

        # ⚠️ 关键修正：外墙自 y0 开始铺（不是 y0+1），盖住地板层的外圈
        # 前墙 z=0
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, 0),
                                   p(base2, W-1, y0+FLOOR_H-1, 0),
                                   FillOperation.REPLACE)
        # 后墙 z=D-1
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, D-1),
                                   p(base2, W-1, y0+FLOOR_H-1, D-1),
                                   FillOperation.REPLACE)
        # 左墙 x=0
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, 0),
                                   p(base2, 0,   y0+FLOOR_H-1, D-1),
                                   FillOperation.REPLACE)
        # 右墙 x=W-1
        blocks.fill(STONE_BRICKS, p(base2, W-1, y0, 0),
                                   p(base2, W-1, y0+FLOOR_H-1, D-1),
                                   FillOperation.REPLACE)

        # 内部清空（不影响外墙）
        blocks.fill(AIR,
            p(base2, 1, y0+1, 1),
            p(base2, W-2, y0+FLOOR_H-1, D-2),
            FillOperation.REPLACE)

        # 窗带（从第二层起；y0+2..y0+3）——仅"替换"为玻璃，不留空
        if level > 0:
            blocks.fill(GLASS, p(base2, 2,     y0+2, 0),    p(base2, W-3, y0+3, 0),    FillOperation.REPLACE)   # 前
            blocks.fill(GLASS, p(base2, 2,     y0+2, D-1),  p(base2, W-3, y0+3, D-1),  FillOperation.REPLACE)   # 后
            blocks.fill(GLASS, p(base2, 0,     y0+2, 2),    p(base2, 0,   y0+3, D-3),  FillOperation.REPLACE)   # 左
            blocks.fill(GLASS, p(base2, W-1,   y0+2, 2),    p(base2, W-1, y0+3, D-3),  FillOperation.REPLACE)   # 右

        # —— 嵌入"上一层"的天花板灯 ——
        # 当前 level 的地板 y = y0，正好是"上一层 (level-1) 的天花板平面"
        if level > 0:
            embed_lights_on_plane(base2, y0)

    # 一层大门（前墙中点）
    door_x = W // 2
    blocks.fill(AIR, p(base2, door_x, 1, 0), p(base2, door_x, 2, 0), FillOperation.REPLACE)
    blocks.place(OAK_DOOR, p(base2, door_x, 1, 0))

    # 3) 斜坡屋顶（3 层，金合欢木板）
    build_sloped_roof_3_layers(base2)

    # 顶层天花板灯：嵌入屋顶最底层（y = FLOORS*FLOOR_H）
    top_ceiling_y = FLOORS * FLOOR_H
    embed_lights_on_plane(base2, top_ceiling_y)

def build_sloped_roof_3_layers(base2):
    y = FLOORS * FLOOR_H
    x1, z1 = -ROOF_OVERHANG, -ROOF_OVERHANG
    x2, z2 = W - 1 + ROOF_OVERHANG, D - 1 + ROOF_OVERHANG
    for _ in range(3):
        if x1 > x2 or z1 > z2: break
        blocks.fill(PLANKS_ACACIA, p(base2, x1, y, z1), p(base2, x2, y, z2), FillOperation.REPLACE)
        y += 1; x1 += 1; z1 += 1; x2 -= 1; z2 -= 1

def on_chat_build():
    base = player.position()
    build_building(base)

player.on_chat("build", on_chat_build)