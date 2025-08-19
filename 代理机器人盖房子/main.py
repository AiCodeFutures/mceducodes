# ==== 参数 ====
W, D, H = 8, 8, 5
SLOT_STONE = 1
SLOT_GLASS = 2
SLOT_PLANK = 3  # 木板

# ==== 小工具 ====
def tp_above(p, face):
    agent.teleport(positions.add(p, pos(0, 1, 0)), face)

def clear_down_if_any():
    try:
        if agent.detect(AgentDetection.BLOCK, DOWN):
            agent.destroy(DOWN)
    except:
        agent.destroy(DOWN)

def put_down(slot):
    agent.setSlot(slot)
    agent.place(DOWN)

# 在 ORG + (x, dy, z) 精确落块（face 仅影响朝向）
def place_at(ORG, x, dy, z, slot, face):
    P = positions.add(ORG, pos(x, dy, z))
    tp_above(P, face)
    clear_down_if_any()
    put_down(slot)

# 让代理落到地面
def ensure_on_ground(max_steps=20):
    try:
        steps = 0
        while not agent.detect(AgentDetection.BLOCK, DOWN) and steps < max_steps:
            agent.move(DOWN, 1)
            steps += 1
    except:
        for _ in range(3):
            agent.move(DOWN, 1)

# ==== 主命令 ====
def on_chat_agenthouse8():
    # 把 Agent 拉到你脚边，并确保落地
    try:
        agent.teleport(player.position(), EAST)
    except:
        pass
    ensure_on_ground()
    try:
        agent.move(RIGHT, 1)  # 侧移避免和玩家重叠
    except:
        pass

    # 备料（门去掉了）
    agent.setItem(STONE_BRICKS, 64*6, SLOT_STONE)
    agent.setItem(GLASS,        64,   SLOT_GLASS)
    agent.setItem(PLANKS_OAK,   64*6, SLOT_PLANK)

    # 原点：以玩家为中心的"前左内角"，y=玩家当前 y
    base = player.position()
    ORG  = positions.add(base, pos(-W//2, 0, -D//2))   # (x:0..W-1, dy:0.., z:0..D-1)

    # 1) 地板（dy=0）
    for z in range(D):
        for x in range(W):
            place_at(ORG, x, 0, z, SLOT_STONE, EAST)

    # 2) 墙体（dy=1..H）
    #   门洞仍为左侧 x=1, dy=1..2 留空（不装门，留给你自己放）
    #   窗：前墙 z=0，右侧 x∈[W-4..W-2]，dy=2..3（比地板高一格）
    for dy in range(1, H + 1):
        # 前边（含角）
        for x in range(W):
            if (x == 1) and (dy in [1, 2]):  # 门洞留空
                continue
            slot = SLOT_GLASS if (W - 4 <= x <= W - 2 and dy in [2, 3]) else SLOT_STONE
            place_at(ORG, x, dy, 0, slot, EAST)

        # 右边（去角）
        for z in range(1, D - 1):
            place_at(ORG, W - 1, dy, z, SLOT_STONE, EAST)

        # 后边（含角）
        for x in range(W):
            place_at(ORG, x, dy, D - 1, SLOT_STONE, EAST)

        # 左边（去角）
        for z in range(1, D - 1):
            place_at(ORG, 0, dy, z, SLOT_STONE, EAST)

    # 3) 屋顶：三层木板
    # 第1层：外挑1格（x:-1..W , z:-1..D）
    for z in range(-1, D + 1):
        for x in range(-1, W + 1):
            place_at(ORG, x, H + 1, z, SLOT_PLANK, EAST)

    # 第2层：与墙齐平（x:0..W-1 , z:0..D-1）
    for z in range(D):
        for x in range(W):
            place_at(ORG, x, H + 2, z, SLOT_PLANK, EAST)

    # 第3层：内收1格（x:1..W-2 , z:1..D-2）
    for z in range(1, D - 1):
        for x in range(1, W - 1):
            place_at(ORG, x, H + 3, z, SLOT_PLANK, EAST)

player.on_chat("ah", on_chat_agenthouse8)




