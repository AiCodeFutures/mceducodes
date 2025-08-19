# ===== Building parameters =====
W = 20
D = 20
FLOORS = 3
FLOOR_H = 7
ROOF_OVERHANG = 3

def p(base, dx, dy, dz):
    return positions.add(base, pos(dx, dy, dz))

# --- foundation (stone bricks), 2 layers, extend 3 blocks around ---
def build_foundation(base):
    over = 3
    blocks.fill(STONE_BRICKS,
        p(base, -over, 0, -over),
        p(base, W-1+over, 1, D-1+over),
        FillOperation.REPLACE)

# --- embed ceiling lights on a given Y plane (replace plank with lantern) ---
def embed_lights_on_plane(base2, y_plane):
    for x in range(2, W-2, 5):
        for z in range(2, D-2, 5):
            blocks.place(AIR,         p(base2, x, y_plane, z))
            blocks.place(SEA_LANTERN, p(base2, x, y_plane, z))

# ========================
# Water elevator add-on
# ========================

# 生成一根 1x1 的玻璃水电梯：center=(sx,sz)，side_open 决定每层开门方向
# side_open 可选: "N" "S" "W" "E"
def build_one_elevator(base2, sx, sz, is_up, side_open):
    # 电梯立柱的高度范围
    y_bottom = -1                 # 要把底下一格替换成灵魂沙/岩浆块
    y_top    = FLOORS * FLOOR_H   # 顶到屋顶底层

    # 玻璃外筒（3x3 包围）
    blocks.fill(GLASS,
        p(base2, sx-1, 0,   sz-1),
        p(base2, sx+1, y_top, sz+1),
        FillOperation.REPLACE)

    # 清空内芯 & 注满"水源方块"
    blocks.fill(AIR,
        p(base2, sx, 0, sz),
        p(base2, sx, y_top, sz),
        FillOperation.REPLACE)

    blocks.fill(WATER,
        p(base2, sx, 0, sz),
        p(base2, sx, y_top-1, sz),
        FillOperation.REPLACE)

    # 底座：上行=灵魂沙，下行=岩浆块（要放在水列正下方一格）
    blocks.place(SOUL_SAND if is_up else MAGMA_BLOCK, p(base2, sx, y_bottom, sz))

    # 每层开门：在玻璃外圈对应方向替换为门（两格高）
    for level in range(FLOORS):
        y0 = level * FLOOR_H
        y1, y2 = y0+1, y0+2

        if side_open == "S":      # 在电梯南侧开门（z+1）
            door_pos = p(base2, sx, y1, sz+1)
            above    = p(base2, sx, y2, sz+1)
        elif side_open == "N":    # 北侧（z-1）
            door_pos = p(base2, sx, y1, sz-1)
            above    = p(base2, sx, y2, sz-1)
        elif side_open == "E":    # 东侧（x+1）
            door_pos = p(base2, sx+1, y1, sz)
            above    = p(base2, sx+1, y2, sz)
        else:                     # 西侧（x-1）
            door_pos = p(base2, sx-1, y1, sz)
            above    = p(base2, sx-1, y2, sz)

        # 门洞：把该位置两格清空，再放门（门会挡水不外流）
        blocks.place(AIR, above)
        blocks.place(AIR, door_pos)
        blocks.place(OAK_DOOR, door_pos)

# 生成一组上/下行电梯
def build_water_elevators(base2):
    # 你可以调整这两个坐标来改变电梯位置
    up_sx, up_sz   = 3, 3   # 上行（灵魂沙）
    down_sx, down_sz = 5, 3 # 下行（岩浆）
    side = "S"              # 每层朝南侧开门（改成 "E"/"W"/"N" 可变方向）

    build_one_elevator(base2, up_sx,   up_sz,   True,  side)
    build_one_elevator(base2, down_sx, down_sz, False, side)

# ========================

def build_building(base):
    # 1) 地基
    build_foundation(base)
    base2 = p(base, 0, 2, 0)  # 楼体整体抬高 2 格

    # 2) 楼层
    for level in range(FLOORS):
        y0 = level * FLOOR_H

        # 地板（与外墙留缝）
        blocks.fill(PLANKS_ACACIA,
            p(base2, 1, y0, 1),
            p(base2, W-2, y0, D-2),
            FillOperation.REPLACE)

        # 外墙：从 y0 铺到 y0+FLOOR_H-1，盖住地板边
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, 0),    p(base2, W-1, y0+FLOOR_H-1, 0),    FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, D-1),  p(base2, W-1, y0+FLOOR_H-1, D-1),  FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, 0,    y0, 0),    p(base2, 0,   y0+FLOOR_H-1, D-1),  FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, W-1, y0, 0),     p(base2, W-1, y0+FLOOR_H-1, D-1),  FillOperation.REPLACE)

        # 清内部
        blocks.fill(AIR,
            p(base2, 1, y0+1, 1),
            p(base2, W-2, y0+FLOOR_H-1, D-2),
            FillOperation.REPLACE)

        # 窗带（2 层及以上）
        if level > 0:
            blocks.fill(GLASS, p(base2, 2,     y0+2, 0),    p(base2, W-3, y0+3, 0),    FillOperation.REPLACE)
            blocks.fill(GLASS, p(base2, 2,     y0+2, D-1),  p(base2, W-3, y0+3, D-1),  FillOperation.REPLACE)
            blocks.fill(GLASS, p(base2, 0,     y0+2, 2),    p(base2, 0,   y0+3, D-3),  FillOperation.REPLACE)
            blocks.fill(GLASS, p(base2, W-1,   y0+2, 2),    p(base2, W-1, y0+3, D-3),  FillOperation.REPLACE)

        # 嵌入上一层天花灯
        if level > 0:
            embed_lights_on_plane(base2, y0)

    # 一层大门
    door_x = W // 2
    blocks.fill(AIR, p(base2, door_x, 1, 0), p(base2, door_x, 2, 0), FillOperation.REPLACE)
    blocks.place(OAK_DOOR, p(base2, door_x, 1, 0))

    # 3) 斜坡屋顶（三层）
    build_sloped_roof_3_layers(base2)
    # 顶层天花灯：嵌入屋顶底层
    embed_lights_on_plane(base2, FLOORS * FLOOR_H)

    # 4) 水电梯（上/下行）
    build_water_elevators(base2)

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