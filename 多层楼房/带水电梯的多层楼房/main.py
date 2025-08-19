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
        p(base, W - 1 + over, 1, D - 1 + over),
        FillOperation.REPLACE)

# --- embed ceiling lights ---
def embed_lights_on_plane(base2, y_plane):
    for x in range(2, W - 2, 5):
        for z in range(2, D - 2, 5):
            blocks.place(AIR, p(base2, x, y_plane, z))
            blocks.place(SEA_LANTERN, p(base2, x, y_plane, z))

# ========================
# Water elevator
# ========================
def build_one_elevator(base2, sx, sz, is_up, side_open):
    y_bottom = -1
    y_top = FLOORS * FLOOR_H

    # glass shell
    blocks.fill(GLASS,
        p(base2, sx - 1, 0, sz - 1),
        p(base2, sx + 1, y_top, sz + 1),
        FillOperation.REPLACE)

    # core water
    blocks.fill(AIR, p(base2, sx, 0, sz), p(base2, sx, y_top, sz), FillOperation.REPLACE)
    blocks.fill(WATER, p(base2, sx, 0, sz), p(base2, sx, y_top - 1, sz), FillOperation.REPLACE)

    # base
    if is_up:
        blocks.place(SOUL_SAND, p(base2, sx, y_bottom, sz))
    else:
        blocks.place(MAGMA_BLOCK, p(base2, sx, y_bottom, sz))

    # doors
    for level in range(FLOORS):
        y0 = level * FLOOR_H
        y1 = y0 + 1
        y2 = y0 + 2

        if side_open == "S":
            door_pos = p(base2, sx, y1, sz + 1)
            above = p(base2, sx, y2, sz + 1)
        elif side_open == "N":
            door_pos = p(base2, sx, y1, sz - 1)
            above = p(base2, sx, y2, sz - 1)
        elif side_open == "E":
            door_pos = p(base2, sx + 1, y1, sz)
            above = p(base2, sx + 1, y2, sz)
        else:
            door_pos = p(base2, sx - 1, y1, sz)
            above = p(base2, sx - 1, y2, sz)

        blocks.place(AIR, above)
        blocks.place(AIR, door_pos)
        blocks.place(OAK_DOOR, door_pos)

def build_water_elevators(base2):
    build_one_elevator(base2, 3, 3, True, "S")
    build_one_elevator(base2, 5, 3, False, "S")

# ========================
# Grand entrance
# ========================
def build_grand_entrance(base2):
    GATE_W = 8
    GATE_H = 5
    GATE_THICK = 2

    cx = W // 2
    x1 = cx - GATE_W // 2
    x2 = cx + GATE_W // 2 - 1
    y1 = 1
    y2 = y1 + GATE_H - 1
    zf = 0

    blocks.fill(AIR,
        p(base2, x1, y1, zf),
        p(base2, x2, y2, zf + (GATE_THICK - 1)),
        FillOperation.REPLACE)

    # pillars and header
    blocks.fill(STONE_BRICKS, p(base2, x1 - 1, y1, zf), p(base2, x1 - 1, y2 + 1, zf + 1), FillOperation.REPLACE)
    blocks.fill(STONE_BRICKS, p(base2, x2 + 1, y1, zf), p(base2, x2 + 1, y2 + 1, zf + 1), FillOperation.REPLACE)
    blocks.fill(STONE_BRICKS, p(base2, x1 - 1, y2 + 1, zf), p(base2, x2 + 1, y2 + 1, zf + 1), FillOperation.REPLACE)

    # lanterns
    blocks.place(SEA_LANTERN, p(base2, x1 - 1, y2 + 1, zf))
    blocks.place(SEA_LANTERN, p(base2, x2 + 1, y2 + 1, zf))

def build_sloped_roof_3_layers(base2):
    y = FLOORS * FLOOR_H
    x1 = -ROOF_OVERHANG
    z1 = -ROOF_OVERHANG
    x2 = W - 1 + ROOF_OVERHANG
    z2 = D - 1 + ROOF_OVERHANG
    for i in range(3):
        if x1 > x2 or z1 > z2:
            break
        blocks.fill(PLANKS_ACACIA, p(base2, x1, y, z1), p(base2, x2, y, z2), FillOperation.REPLACE)
        y = y + 1
        x1 = x1 + 1
        z1 = z1 + 1
        x2 = x2 - 1
        z2 = z2 - 1

def build_building(base):
    build_foundation(base)
    base2 = p(base, 0, 2, 0)

    for level in range(FLOORS):
        y0 = level * FLOOR_H

        blocks.fill(PLANKS_ACACIA, p(base2, 1, y0, 1), p(base2, W - 2, y0, D - 2), FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, 0, y0, 0), p(base2, W - 1, y0 + FLOOR_H - 1, 0), FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, 0, y0, D - 1), p(base2, W - 1, y0 + FLOOR_H - 1, D - 1), FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, 0, y0, 0), p(base2, 0, y0 + FLOOR_H - 1, D - 1), FillOperation.REPLACE)
        blocks.fill(STONE_BRICKS, p(base2, W - 1, y0, 0), p(base2, W - 1, y0 + FLOOR_H - 1, D - 1), FillOperation.REPLACE)

        blocks.fill(AIR, p(base2, 1, y0 + 1, 1), p(base2, W - 2, y0 + FLOOR_H - 1, D - 2), FillOperation.REPLACE)

        if level > 0:
            blocks.fill(GLASS, p(base2, 2, y0 + 2, 0), p(base2, W - 3, y0 + 3, 0), FillOperation.REPLACE)

        if level > 0:
            embed_lights_on_plane(base2, y0)

    build_grand_entrance(base2)
    build_sloped_roof_3_layers(base2)
    embed_lights_on_plane(base2, FLOORS * FLOOR_H)
    build_water_elevators(base2)

def on_chat_build():
    base = player.position()
    build_building(base)

player.on_chat("build", on_chat_build)