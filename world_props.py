from math import atan2, cos, degrees, radians, sin
from ursina import BoxCollider, Entity, Text, Vec3, color, destroy, lerp
from ursina.shaders import basic_lighting_shader


def _part(parent, scale, pos=(0, 0, 0), rot=(0, 0, 0), col=color.white, collider=None, lit=True, model='cube'):
    """Helper compacto para construir piezas 3D."""
    kwargs = {
        'parent': parent,
        'model': model,
        'scale': scale,
        'position': pos,
        'rotation': rot,
        'color': col,
    }
    if collider:
        kwargs['collider'] = collider
    if lit:
        kwargs['shader'] = basic_lighting_shader
    return Entity(**kwargs)


def _label(parent, text, y=2.5, col=color.white, tags_list=None, scale=7.5):
    t = Text(parent=parent, text=text, origin=(0, 0), y=y, scale=scale, color=col)
    if tags_list is not None:
        tags_list.append(t)
    return t


# ==========================================
# 1. ESCENARIO BASE (CASAS, FUEGO Y CIELO)
# ==========================================
def build_house(pos, rot_y=0, wall_col=color.smoke, roof_col=color.brown):
    root = Entity(position=pos, rotation_y=rot_y)
    _part(root, (6.5, 4.0, 5.5), (0, 2.0, 0), col=wall_col, collider='box')
    _part(root, (7.1, 0.35, 3.6), (0, 4.65, -1.55), rot=(28, 0, 0), col=roof_col, collider='box')
    _part(root, (7.1, 0.35, 3.6), (0, 4.65, 1.55), rot=(-28, 0, 0), col=roof_col, collider='box')
    _part(root, (6.4, 1.2, 1.8), (0, 4.4, 0), col=wall_col)
    _part(root, (1.2, 2.3, 0.15), (0, 1.15, 2.78), col=color.rgb32(105, 60, 28), lit=False)
    _part(root, (1.1, 1.0, 0.15), (-1.9, 2.2, 2.78), col=color.cyan, lit=False)
    _part(root, (1.1, 1.0, 0.15), (1.9, 2.2, 2.78), col=color.cyan, lit=False)
    _part(root, (1.4, 1.0, 0.15), (0, 2.2, -2.78), col=color.cyan, lit=False)
    return root


def build_smiling_sun(pos):
    sun = Entity(position=pos, rotation=(16, 24, 0))
    _part(sun, (7.0, 7.0, 2.5), (0, 0, 0), col=color.gold, lit=False)
    for ang in range(0, 360, 45):
        _part(sun, (1.4, 2.4, 1.2), (sin(radians(ang)) * 5.2, cos(radians(ang)) * 5.2, 0), rot=(0, 0, -ang), col=color.yellow, lit=False)
    _part(sun, (2.2, 1.2, 0.4), (-1.5, 0.8, -1.35), col=color.black, lit=False)
    _part(sun, (2.2, 1.2, 0.4), (1.5, 0.8, -1.35), col=color.black, lit=False)
    _part(sun, (1.0, 0.35, 0.4), (0, 1.0, -1.35), col=color.black, lit=False)
    _part(sun, (0.6, 0.25, 0.45), (-1.9, 1.1, -1.40), col=color.white, lit=False)
    _part(sun, (0.6, 0.25, 0.45), (1.1, 1.1, -1.40), col=color.white, lit=False)
    _part(sun, (2.8, 0.45, 0.4), (0, -1.4, -1.35), col=color.black, lit=False)
    _part(sun, (0.55, 0.55, 0.4), (-1.55, -1.05, -1.35), col=color.black, lit=False)
    _part(sun, (0.55, 0.55, 0.4), (1.55, -1.05, -1.35), col=color.black, lit=False)
    return sun


def build_happy_cloud(pos, rot_y=0):
    cloud = Entity(position=pos, rotation_y=rot_y)
    _part(cloud, (6.5, 2.0, 3.2), (0, 0, 0), col=color.white, lit=False)
    _part(cloud, (3.6, 2.4, 2.8), (-1.4, 0.9, 0), col=color.white, lit=False)
    _part(cloud, (3.2, 2.0, 2.6), (1.5, 0.7, 0), col=color.white, lit=False)
    for side_z, face_dir in ((-1.65, -1), (1.65, 1)):
        _part(cloud, (0.35, 0.35, 0.1), (-0.9, 0.2, side_z), col=color.black, lit=False)
        _part(cloud, (0.35, 0.35, 0.1), (0.9, 0.2, side_z), col=color.black, lit=False)
        _part(cloud, (1.2, 0.22, 0.1), (0, -0.35, side_z), col=color.black, lit=False)
        _part(cloud, (0.45, 0.25, 0.1), (-1.4, -0.1, side_z + 0.02 * face_dir), col=color.pink, lit=False)
        _part(cloud, (0.45, 0.25, 0.1), (1.4, -0.1, side_z + 0.02 * face_dir), col=color.pink, lit=False)
    return cloud


def build_burning_plane():
    plane = Entity(position=(0, 19, 0))
    _part(plane, (1.1, 1.0, 5.4), (0, 0, 0), col=color.smoke, lit=False)
    _part(plane, (6.6, 0.18, 1.5), (0, 0.0, 0.3), col=color.light_gray, lit=False)
    _part(plane, (2.2, 0.15, 0.9), (0, 0.2, -2.3), col=color.light_gray, lit=False)
    _part(plane, (0.18, 1.2, 0.9), (0, 0.7, -2.3), col=color.red, lit=False)
    _part(plane, (0.9, 0.5, 1.2), (0, 0.55, 0.8), col=color.cyan, lit=False)
    flames = [
        _part(plane, (0.9, 0.9, 1.6), (0, 0.2, -2.9), col=color.orange, lit=False),
        _part(plane, (0.7, 0.7, 1.2), (-1.4, 0.1, -0.6), col=color.red, lit=False),
        _part(plane, (0.7, 0.7, 1.2), (1.4, 0.1, -0.6), col=color.yellow, lit=False),
    ]
    return plane, flames


def build_camp_fire(pos):
    fire = Entity(position=pos)
    _part(fire, (1.1, 0.22, 0.25), (0, 0.11, 0), rot=(0, 35, 0), col=color.brown)
    _part(fire, (1.1, 0.22, 0.25), (0, 0.11, 0), rot=(0, -35, 0), col=color.brown)
    f1 = _part(fire, (0.55, 1.15, 0.55), (0, 0.65, 0), col=color.orange, lit=False)
    f2 = _part(fire, (0.36, 0.85, 0.36), (0.14, 0.55, 0.10), col=color.red, lit=False)
    f3 = _part(fire, (0.30, 0.70, 0.30), (-0.12, 0.50, -0.10), col=color.yellow, lit=False)
    return (f1, f2, f3)


# ==========================================
# 2. TÓTEMS REPRESENTATIVOS DE EASTER EGGS
# ==========================================
def _make_totem(egg_id, pos, tags):
    totem = Entity(position=pos)
    totem.collider = BoxCollider(totem, size=(1.35, 1.35, 1.35))
    totem.easter_egg_id = egg_id

    if egg_id == 'steve':
        _part(totem, (1.05, 1.05, 1.05), col=color.brown)
        _part(totem, (1.08, 0.30, 1.08), (0, 0.40, 0), col=color.green)
        _label(totem, '?', y=1.1, col=color.cyan, tags_list=tags, scale=6.5)
    elif egg_id == 'goku':
        _part(totem, (0.95, 0.95, 0.95), col=color.orange, model='sphere', lit=False)
        _part(totem, (0.28, 0.28, 0.28), (0, 0, 0.42), col=color.red, lit=False)
        _label(totem, 'ESFERA 4*', y=1.0, col=color.gold, tags_list=tags, scale=5.5)
    elif egg_id == 'naruto':
        _part(totem, (0.42, 1.10, 0.42), rot=(0, 0, 35), col=color.red)
        _part(totem, (0.46, 0.28, 0.46), rot=(0, 0, 35), col=color.gold, lit=False)
        _part(totem, (0.36, 1.24, 0.36), rot=(0, 0, 35), col=color.smoke)
        _label(totem, 'PERGAMINO', y=1.05, col=color.orange, tags_list=tags, scale=5.5)
    elif egg_id == 'pikachu':
        _part(totem, (0.92, 0.46, 0.92), (0, 0.23, 0), col=color.red, model='sphere', lit=False)
        _part(totem, (0.92, 0.46, 0.92), (0, -0.23, 0), col=color.white, model='sphere', lit=False)
        _part(totem, (0.96, 0.14, 0.96), (0, 0, 0), col=color.black, lit=False)
        _part(totem, (0.26, 0.26, 0.26), (0, 0, 0.45), col=color.white, model='sphere', lit=False)
        _label(totem, 'POKEBOLA', y=1.0, col=color.yellow, tags_list=tags, scale=5.5)
    elif egg_id == 'charizard':
        _part(totem, (0.65, 1.15, 0.65), rot=(15, 20, 15), col=color.orange, lit=False)
        _part(totem, (0.42, 0.75, 0.42), (0, 0.2, 0), rot=(-15, 0, -20), col=color.red, lit=False)
        _label(totem, 'PIEDRA FUEGO', y=1.1, col=color.orange, tags_list=tags, scale=5.5)
    elif egg_id == 'dinosaurio':
        _part(totem, (0.90, 1.18, 0.90), col=color.smoke, model='sphere')
        _part(totem, (0.30, 0.30, 0.30), (0.32, 0.2, 0.32), col=color.green, model='sphere')
        _part(totem, (0.28, 0.28, 0.28), (-0.30, -0.15, 0.34), col=color.green, model='sphere')
        _label(totem, 'HUEVO DINO', y=1.1, col=color.lime, tags_list=tags, scale=5.5)
    elif egg_id == 'gato':
        _part(totem, (0.76, 0.76, 0.76), col=color.magenta, model='sphere')
        _part(totem, (0.94, 0.14, 0.16), (0, 0.42, 0), col=color.azure)
        _part(totem, (0.18, 0.34, 0.28), (-0.46, 0.05, 0), col=color.azure)
        _part(totem, (0.18, 0.34, 0.28), (0.46, 0.05, 0), col=color.azure)
        _label(totem, 'OVILLO :3', y=1.05, col=color.cyan, tags_list=tags, scale=5.5)
    elif egg_id == 'joker':
        _part(totem, (0.85, 1.15, 0.10), rot=(0, 0, -12), col=color.red, lit=False)
        _part(totem, (0.65, 0.22, 0.12), (0, 0.18, 0), rot=(0, 0, -12), col=color.black, lit=False)
        _part(totem, (0.55, 0.14, 0.14), (0, -0.18, 0), rot=(0, 0, -12), col=color.white, lit=False)
        _label(totem, 'CALLING CARD', y=1.1, col=color.red, tags_list=tags, scale=5.5)
    elif egg_id == 'lamborghini':
        _part(totem, (0.88, 1.02, 0.16), col=color.black)
        _part(totem, (0.62, 0.72, 0.20), col=color.gold, lit=False)
        _label(totem, 'LOGO TORO', y=1.05, col=color.yellow, tags_list=tags, scale=5.5)
    elif egg_id == 'jetta':
        _part(totem, (0.95, 0.95, 0.18), col=color.azure, model='sphere', lit=False)
        _part(totem, (0.58, 0.58, 0.22), col=color.white, lit=False)
        _label(totem, 'EMBLEMA VW', y=1.05, col=color.azure, tags_list=tags, scale=5.5)
    elif egg_id == 'frontier':
        _part(totem, (0.95, 0.95, 0.42), col=color.black)
        _part(totem, (0.55, 0.55, 0.46), col=color.red, lit=False)
        _label(totem, 'LLANTA 4X4', y=1.05, col=color.salmon, tags_list=tags, scale=5.5)

    return totem


# ==========================================
# 3. CONSTRUCTORES DE PERSONAJES Y AUTOS
# ==========================================
def _mark_ally_hitboxes(root, msg, col=color.cyan):
    for child in root.children:
        if child.collider:
            child.ally_dialogue = (msg, col)


def _add_wheels(root, xs, zs, r=0.45, w=0.28):
    for wx in xs:
        for wz in zs:
            _part(root, (w, r * 2, r * 2), (wx, r, wz), col=color.black)
            _part(root, (w + 0.03, r, r), (wx, r, wz), col=color.light_gray, lit=False)


def build_steve(pos, rot_y, tags):
    skin = color.rgb32(205, 158, 118)
    hair = color.rgb32(65, 40, 20)
    shirt = color.rgb32(0, 165, 175)
    pants = color.rgb32(55, 55, 160)

    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    leg_l = _part(root, (0.34, 0.78, 0.34), (-0.18, 0.39, 0), col=pants)
    _part(leg_l, (1.02, 0.22, 1.04), (0, -0.40, 0), col=color.gray, lit=False)
    leg_r = _part(root, (0.34, 0.78, 0.34), (0.18, 0.39, 0), col=pants)
    _part(leg_r, (1.02, 0.22, 1.04), (0, -0.40, 0), col=color.gray, lit=False)

    _part(root, (0.72, 0.82, 0.38), (0, 1.18, 0), col=shirt, collider='box')
    head = _part(root, (0.56, 0.56, 0.56), (0, 1.87, 0), col=skin, collider='box')
    _part(head, (1.04, 0.26, 1.04), (0, 0.40, 0), col=hair, lit=False)
    _part(head, (1.04, 0.65, 0.30), (0, 0.15, -0.38), col=hair, lit=False)
    _part(head, (0.22, 0.12, 0.06), (-0.18, 0.05, 0.50), col=color.white, lit=False)
    _part(head, (0.11, 0.12, 0.08), (-0.14, 0.05, 0.51), col=color.blue, lit=False)
    _part(head, (0.22, 0.12, 0.06), (0.18, 0.05, 0.50), col=color.white, lit=False)
    _part(head, (0.11, 0.12, 0.08), (0.14, 0.05, 0.51), col=color.blue, lit=False)
    _part(head, (0.42, 0.16, 0.06), (0, -0.26, 0.50), col=hair, lit=False)

    arm_l = _part(root, (0.26, 0.74, 0.26), (-0.50, 1.20, 0), col=skin)
    _part(arm_l, (1.05, 0.38, 1.05), (0, 0.33, 0), col=shirt, lit=False)

    arm_r = Entity(parent=root, position=(0.50, 1.48, 0))
    _part(arm_r, (0.26, 0.74, 0.26), (0, -0.28, 0), col=skin)
    _part(arm_r, (0.28, 0.28, 0.28), (0, -0.04, 0), col=shirt)
    pick = Entity(parent=arm_r, position=(0, -0.58, 0.30), rotation_x=35)
    _part(pick, (0.08, 0.08, 0.65), col=color.brown)
    _part(pick, (0.68, 0.10, 0.10), (0, 0.04, 0.28), col=color.cyan)
    _part(pick, (0.14, 0.14, 0.12), (-0.32, -0.02, 0.22), col=color.turquoise, lit=False)
    _part(pick, (0.14, 0.14, 0.12), (0.32, -0.02, 0.22), col=color.turquoise, lit=False)

    _label(root, 'STEVE', y=2.55, col=color.cyan, tags_list=tags)
    _mark_ally_hitboxes(root, 'Steve: Ey! Estamos en el mismo equipo!', color.cyan)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r, 'arm': arm_r}
    return root


def build_goku(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    skin, gi, sash = color.peach, color.orange, color.blue
    leg_l = _part(root, (0.32, 0.75, 0.32), (-0.18, 0.38, 0), col=gi)
    leg_r = _part(root, (0.32, 0.75, 0.32), (0.18, 0.38, 0), col=gi)
    _part(leg_l, (1.06, 0.28, 1.12), (0, -0.34, 0), col=sash, lit=False)
    _part(leg_r, (1.06, 0.28, 1.12), (0, -0.34, 0), col=sash, lit=False)
    _part(root, (0.72, 0.82, 0.38), (0, 1.16, 0), col=gi, collider='box')
    _part(root, (0.75, 0.18, 0.42), (0, 0.85, 0), col=sash)
    _part(root, (0.52, 0.52, 0.52), (0, 1.84, 0), col=skin)
    for sx, sy, sz, rx, rz in [
        (0, 0.42, 0, 0, 0), (-0.26, 0.34, 0, 0, 28), (0.26, 0.34, 0, 0, -28),
        (0, 0.34, -0.24, -30, 0), (-0.18, 0.38, 0.16, 20, 18), (0.18, 0.38, 0.16, 20, -18),
    ]:
        _part(root, (0.22, 0.45, 0.22), (sx, 1.84 + sy, sz), rot=(rx, 0, rz), col=color.gold, lit=False)
    arm_r = Entity(parent=root, position=(0, 1.25, 0.18))
    _part(arm_r, (0.22, 0.22, 0.65), (-0.32, 0, 0.14), rot=(0, 18, 0), col=skin)
    _part(arm_r, (0.22, 0.22, 0.65), (0.32, 0, 0.14), rot=(0, -18, 0), col=skin)
    kame = _part(arm_r, 0.45, (0, 0, 0.54), col=color.cyan, model='sphere', lit=False)
    _label(root, 'GOKU (SSJ)', y=2.7, col=color.gold, tags_list=tags)
    _mark_ally_hitboxes(root, 'Goku: Jaja! Ese ataque no me hace nada!', color.gold)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r, 'arm': arm_r, 'orb': kame}
    return root


def build_naruto(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    skin, orange_c, dark_c = color.peach, color.orange, color.rgb32(30, 30, 35)
    leg_l = _part(root, (0.30, 0.74, 0.30), (-0.17, 0.37, 0), col=orange_c)
    leg_r = _part(root, (0.30, 0.74, 0.30), (0.17, 0.37, 0), col=orange_c)
    _part(root, (0.68, 0.80, 0.36), (0, 1.14, 0), col=orange_c, collider='box')
    _part(root, (0.70, 0.35, 0.38), (0, 1.34, 0), col=dark_c)
    _part(root, (0.50, 0.50, 0.50), (0, 1.82, 0), col=skin)
    _part(root, (0.53, 0.14, 0.53), (0, 1.94, 0), col=dark_c)
    _part(root, (0.30, 0.10, 0.06), (0, 1.94, 0.26), col=color.light_gray, lit=False)
    for sx, rz in [(-0.2, 22), (0, 0), (0.2, -22)]:
        _part(root, (0.20, 0.32, 0.22), (sx, 2.16, 0), rot=(0, 0, rz), col=color.yellow)
    _part(root, (0.22, 0.22, 0.65), (-0.45, 1.18, 0.08), col=orange_c)
    arm_r = Entity(parent=root, position=(0.45, 1.25, 0))
    _part(arm_r, (0.22, 0.22, 0.65), (0, 0, 0.28), col=orange_c)
    rasengan = _part(arm_r, 0.40, (0, 0, 0.72), col=color.azure, model='sphere', lit=False)
    _label(root, 'NARUTO', y=2.6, col=color.orange, tags_list=tags)
    _mark_ally_hitboxes(root, 'Naruto: De veras! Somos aliados!', color.orange)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r, 'arm': arm_r, 'spin_orb': rasengan}
    return root


def build_pikachu(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    yel = color.yellow
    _part(root, (0.68, 0.78, 0.58), (0, 0.52, 0), col=yel, collider='box')
    _part(root, (0.58, 0.54, 0.54), (0, 1.14, 0.04), col=yel)
    _part(root, (0.14, 0.45, 0.14), (-0.22, 1.56, 0), rot=(0, 0, 18), col=yel)
    _part(root, (0.14, 0.18, 0.14), (-0.30, 1.78, 0), rot=(0, 0, 18), col=color.black)
    _part(root, (0.14, 0.45, 0.14), (0.22, 1.56, 0), rot=(0, 0, -18), col=yel)
    _part(root, (0.14, 0.18, 0.14), (0.30, 1.78, 0), rot=(0, 0, -18), col=color.black)
    _part(root, (0.10, 0.10, 0.05), (-0.15, 1.18, 0.30), col=color.black, lit=False)
    _part(root, (0.10, 0.10, 0.05), (0.15, 1.18, 0.30), col=color.black, lit=False)
    _part(root, (0.14, 0.12, 0.05), (-0.22, 1.04, 0.29), col=color.red, lit=False)
    _part(root, (0.14, 0.12, 0.05), (0.22, 1.04, 0.29), col=color.red, lit=False)
    _part(root, (0.10, 0.50, 0.16), (0, 0.62, -0.38), rot=(-35, 0, 0), col=color.brown)
    _part(root, (0.10, 0.60, 0.24), (0, 1.02, -0.58), rot=(-20, 0, 0), col=yel)
    _label(root, 'PIKACHU', y=2.15, col=color.yellow, tags_list=tags)
    _mark_ally_hitboxes(root, 'Pikachu: Pika-pika!', color.yellow)
    root.anim_parts = {}
    return root


def build_charizard(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    org, crm, wing_c = color.orange, color.peach, color.turquoise
    _part(root, (1.25, 1.55, 1.05), (0, 1.1, 0), col=org, collider='box')
    _part(root, (0.85, 1.25, 0.15), (0, 1.05, 0.50), col=crm)
    leg_l = _part(root, (0.45, 0.65, 0.55), (-0.42, 0.32, 0), col=org)
    leg_r = _part(root, (0.45, 0.65, 0.55), (0.42, 0.32, 0), col=org)
    _part(root, (0.58, 0.80, 0.58), (0, 2.10, 0.15), rot=(14, 0, 0), col=org)
    _part(root, (0.68, 0.55, 0.92), (0, 2.52, 0.42), col=org)
    _part(root, (0.12, 0.40, 0.12), (-0.22, 2.86, 0.10), rot=(-25, 0, 12), col=org)
    _part(root, (0.12, 0.40, 0.12), (0.22, 2.86, 0.10), rot=(-25, 0, -12), col=org)
    _part(root, (0.10, 0.10, 0.08), (-0.24, 2.60, 0.88), col=color.white, lit=False)
    _part(root, (0.10, 0.10, 0.08), (0.24, 2.60, 0.88), col=color.white, lit=False)
    _part(root, (1.80, 1.35, 0.10), (-1.45, 1.95, -0.35), rot=(15, -22, 18), col=wing_c)
    _part(root, (1.80, 1.35, 0.10), (1.45, 1.95, -0.35), rot=(15, 22, -18), col=wing_c)
    _part(root, (0.35, 0.35, 1.55), (0, 0.55, -1.15), rot=(-18, 0, 0), col=org)
    tail_flame = _part(root, (0.38, 0.52, 0.38), (0, 0.95, -1.92), col=color.yellow, lit=False)
    _label(root, 'CHARIZARD', y=3.35, col=color.orange, tags_list=tags)
    _mark_ally_hitboxes(root, 'Charizard: Grrr! (es aliado)', color.orange)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r, 'flame': tail_flame}
    return root


def build_dinosaur(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    dino_c, belly = color.rgb32(55, 145, 65), color.olive
    leg_l = _part(root, (0.65, 1.45, 0.80), (-0.62, 0.72, 0), col=dino_c)
    leg_r = _part(root, (0.65, 1.45, 0.80), (0.62, 0.72, 0), col=dino_c)
    _part(root, (1.45, 1.50, 2.30), (0, 1.85, 0.20), rot=(-15, 0, 0), col=dino_c, collider='box')
    _part(root, (1.05, 0.90, 0.25), (0, 1.65, 1.25), rot=(-15, 0, 0), col=belly)
    _part(root, (0.70, 0.70, 2.40), (0, 1.65, -1.90), rot=(12, 0, 0), col=dino_c)
    _part(root, (1.05, 0.95, 1.55), (0, 2.95, 1.55), col=dino_c)
    _part(root, (0.90, 0.28, 1.25), (0, 2.35, 1.60), col=dino_c)
    _part(root, (0.78, 0.16, 0.14), (0, 2.52, 2.25), col=color.white, lit=False)
    _part(root, (0.16, 0.16, 0.10), (-0.50, 3.10, 1.80), col=color.yellow, lit=False)
    _part(root, (0.16, 0.16, 0.10), (0.50, 3.10, 1.80), col=color.yellow, lit=False)
    _part(root, (0.20, 0.20, 0.45), (-0.75, 1.95, 1.25), rot=(25, 0, 0), col=dino_c)
    _part(root, (0.20, 0.20, 0.45), (0.75, 1.95, 1.25), rot=(25, 0, 0), col=dino_c)
    _label(root, 'DINOSAURIO', y=3.8, col=color.lime, tags_list=tags)
    _mark_ally_hitboxes(root, 'T-Rex: ROAR! (ahora es tu mascota)', color.lime)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r}
    return root


def build_joker_p5(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    coat = color.rgb32(22, 22, 28)
    leg_l = _part(root, (0.28, 0.75, 0.28), (-0.16, 0.37, 0), col=coat)
    leg_r = _part(root, (0.28, 0.75, 0.28), (0.16, 0.37, 0), col=coat)
    _part(root, (0.72, 1.05, 0.40), (0, 1.05, 0), col=coat, collider='box')
    _part(root, (0.34, 0.45, 0.42), (0, 1.25, 0.02), col=color.dark_gray)
    _part(root, (0.20, 0.55, 0.20), (-0.48, 1.15, 0.08), rot=(15, 0, -10), col=coat)
    _part(root, (0.22, 0.22, 0.22), (-0.50, 0.84, 0.15), col=color.red, lit=False)
    arm_r = Entity(parent=root, position=(0.48, 1.40, 0))
    _part(arm_r, (0.20, 0.55, 0.20), (0, -0.25, 0.08), rot=(15, 0, 10), col=coat)
    _part(arm_r, (0.22, 0.22, 0.22), (0.02, -0.56, 0.15), col=color.red, lit=False)
    _part(root, (0.48, 0.50, 0.48), (0, 1.82, 0), col=color.peach)
    _part(root, (0.56, 0.26, 0.56), (0, 2.02, -0.04), col=color.black)
    _part(root, (0.46, 0.18, 0.12), (0, 1.86, 0.24), col=color.white, lit=False)
    _part(root, (0.10, 0.07, 0.13), (-0.12, 1.86, 0.25), col=color.black, lit=False)
    _part(root, (0.10, 0.07, 0.13), (0.12, 1.86, 0.25), col=color.black, lit=False)
    _label(root, 'JOKER (P5)', y=2.55, col=color.red, tags_list=tags)
    _mark_ally_hitboxes(root, 'Joker: Looking cool!', color.red)
    root.anim_parts = {'leg_l': leg_l, 'leg_r': leg_r, 'arm': arm_r}
    return root


def build_autistic_cat(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    fur = color.smoke
    _part(root, (1.8, 0.06, 1.8), (0, 0.03, 0), col=color.turquoise, lit=False)
    _part(root, (0.62, 0.60, 0.80), (0, 0.36, 0), col=fur, collider='box')
    head = Entity(parent=root, position=(0, 0.82, 0.26))
    _part(head, (0.54, 0.48, 0.50), (0, 0, 0), col=fur)
    _part(head, (0.16, 0.20, 0.14), (-0.18, 0.30, 0), col=fur)
    _part(head, (0.16, 0.20, 0.14), (0.18, 0.30, 0), col=fur)
    _part(head, (0.09, 0.12, 0.15), (-0.18, 0.29, 0.02), col=color.pink, lit=False)
    _part(head, (0.09, 0.12, 0.15), (0.18, 0.29, 0.02), col=color.pink, lit=False)
    _part(head, (0.62, 0.08, 0.10), (0, 0.27, 0), col=color.azure)
    _part(head, (0.12, 0.24, 0.22), (-0.31, 0.02, 0), col=color.azure)
    _part(head, (0.12, 0.24, 0.22), (0.31, 0.02, 0), col=color.azure)
    _part(head, (0.08, 0.08, 0.05), (-0.13, 0.05, 0.26), col=color.black, lit=False)
    _part(head, (0.08, 0.08, 0.05), (0.13, 0.05, 0.26), col=color.black, lit=False)
    _part(head, (0.08, 0.05, 0.05), (0, -0.04, 0.26), col=color.pink, lit=False)
    tail = _part(root, (0.12, 0.12, 0.58), (0, 0.35, -0.58), rot=(28, 0, 0), col=fur)
    toy = _part(root, 0.26, (0, 1.35, 1.0), col=color.magenta, model='sphere', lit=False)
    _label(root, 'GATO AUTISTA :3', y=1.85, col=color.cyan, tags_list=tags)
    _mark_ally_hitboxes(root, 'Gato: *ronroneo tranquilo*', color.cyan)
    root.anim_parts = {'cat_head': head, 'cat_tail': tail, 'cat_toy': toy}
    return root


def build_lamborghini(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    body_col = color.yellow
    _part(root, (2.2, 0.55, 4.8), (0, 0.55, 0), col=body_col, collider='box')
    _part(root, (2.15, 0.30, 1.4), (0, 0.45, 2.2), rot=(12, 0, 0), col=body_col)
    _part(root, (1.85, 0.45, 2.1), (0, 1.00, -0.15), col=color.rgb32(25, 28, 35))
    _part(root, (2.25, 0.10, 0.45), (0, 1.15, -2.25), col=color.black)
    _part(root, (0.12, 0.35, 0.25), (-0.75, 0.95, -2.25), col=color.black)
    _part(root, (0.12, 0.35, 0.25), (0.75, 0.95, -2.25), col=color.black)
    _part(root, (0.45, 0.15, 0.1), (-0.7, 0.62, 2.45), col=color.white, lit=False)
    _part(root, (0.45, 0.15, 0.1), (0.7, 0.62, 2.45), col=color.white, lit=False)
    _part(root, (0.55, 0.14, 0.1), (-0.65, 0.68, -2.42), col=color.red, lit=False)
    _part(root, (0.55, 0.14, 0.1), (0.65, 0.68, -2.42), col=color.red, lit=False)
    _add_wheels(root, (-1.1, 1.1), (1.45, -1.45), r=0.42)
    _label(root, 'LAMBORGHINI', y=2.0, col=color.yellow, tags_list=tags)
    root.anim_parts = {}
    return root


def build_vw_jetta(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    body_col = color.rgb32(35, 95, 185)
    _part(root, (2.0, 0.68, 4.6), (0, 0.68, 0), col=body_col, collider='box')
    _part(root, (1.82, 0.62, 2.2), (0, 1.30, -0.15), col=body_col)
    _part(root, (1.76, 0.46, 2.05), (0, 1.32, -0.15), col=color.rgb32(35, 45, 60), lit=False)
    _part(root, (1.2, 0.28, 0.1), (0, 0.68, 2.32), col=color.black)
    _part(root, (0.28, 0.28, 0.12), (0, 0.68, 2.34), col=color.light_gray, lit=False)
    _part(root, (0.38, 0.20, 0.1), (-0.72, 0.72, 2.32), col=color.white, lit=False)
    _part(root, (0.38, 0.20, 0.1), (0.72, 0.72, 2.32), col=color.white, lit=False)
    _add_wheels(root, (-1.02, 1.02), (1.38, -1.38), r=0.38)
    _label(root, 'VW JETTA', y=2.2, col=color.azure, tags_list=tags)
    root.anim_parts = {}
    return root


def build_nissan_frontier(pos, rot_y, tags):
    root = Entity(position=(pos[0], 0, pos[2]), rotation_y=rot_y)
    body_col = color.rgb32(195, 35, 35)
    _part(root, (2.25, 0.75, 5.2), (0, 0.85, 0), col=body_col, collider='box')
    _part(root, (2.30, 0.28, 0.25), (0, 0.52, 2.65), col=color.dark_gray)
    _part(root, (2.10, 0.85, 2.1), (0, 1.62, 0.55), col=body_col)
    _part(root, (2.02, 0.62, 1.95), (0, 1.64, 0.55), col=color.rgb32(30, 38, 48), lit=False)
    _part(root, (1.95, 0.15, 2.0), (0, 1.18, -1.55), col=color.black)
    _part(root, (0.42, 0.24, 0.1), (-0.75, 0.95, 2.62), col=color.white, lit=False)
    _part(root, (0.42, 0.24, 0.1), (0.75, 0.95, 2.62), col=color.white, lit=False)
    _add_wheels(root, (-1.15, 1.15), (1.65, -1.65), r=0.50, w=0.34)
    _label(root, 'NISSAN FRONTIER', y=2.6, col=color.salmon, tags_list=tags)
    root.anim_parts = {}
    return root


# ==========================================
# 4. GESTOR UNIFICADO DEL MAPA Y EASTER EGGS
# ==========================================
EASTER_EGG_DEFS = [
    {'id': 'steve', 'name': 'Steve de Minecraft', 'col': color.cyan, 'pos': (32, 0.75, 32), 'rot_y': -135, 'builder': build_steve, 'ally': True, 'speed': 6.0, 'dmg': 45, 'cd': 0.80, 'range': 2.3},
    {'id': 'goku', 'name': 'Goku (SSJ)', 'col': color.gold, 'pos': (-8, 0.75, 24), 'rot_y': 165, 'builder': build_goku, 'ally': True, 'speed': 6.8, 'dmg': 45, 'cd': 0.90, 'range': 3.2},
    {'id': 'naruto', 'name': 'Naruto', 'col': color.orange, 'pos': (8, 0.75, 24), 'rot_y': -165, 'builder': build_naruto, 'ally': True, 'speed': 6.6, 'dmg': 40, 'cd': 0.85, 'range': 2.5},
    {'id': 'pikachu', 'name': 'Pikachu', 'col': color.yellow, 'pos': (-6, 0.70, 12), 'rot_y': 145, 'builder': build_pikachu, 'ally': True, 'speed': 6.4, 'dmg': 32, 'cd': 0.80, 'range': 2.8},
    {'id': 'charizard', 'name': 'Charizard', 'col': color.orange, 'pos': (-22, 0.80, -18), 'rot_y': 45, 'builder': build_charizard, 'ally': True, 'speed': 5.4, 'dmg': 50, 'cd': 1.15, 'range': 3.2},
    {'id': 'dinosaurio', 'name': 'Dinosaurio T-Rex', 'col': color.lime, 'pos': (25, 0.85, -7), 'rot_y': -85, 'builder': build_dinosaur, 'ally': True, 'speed': 5.2, 'dmg': 55, 'cd': 1.20, 'range': 3.4},
    {'id': 'joker', 'name': 'Joker (Persona 5)', 'col': color.red, 'pos': (24, 0.80, 16), 'rot_y': -135, 'builder': build_joker_p5, 'ally': True, 'speed': 6.4, 'dmg': 42, 'cd': 0.80, 'range': 2.5},
    {'id': 'gato', 'name': 'Gato Autista :3', 'col': color.cyan, 'pos': (6, 0.70, -10), 'rot_y': -30, 'builder': build_autistic_cat, 'ally': False},
    {'id': 'lamborghini', 'name': 'Lamborghini', 'col': color.yellow, 'pos': (16, 0.80, 8), 'rot_y': -35, 'builder': build_lamborghini, 'ally': False},
    {'id': 'jetta', 'name': 'VW Jetta', 'col': color.azure, 'pos': (-18, 0.80, 14), 'rot_y': 40, 'builder': build_vw_jetta, 'ally': False},
    {'id': 'frontier', 'name': 'Nissan Frontier', 'col': color.salmon, 'pos': (18, 0.80, -22), 'rot_y': -125, 'builder': build_nissan_frontier, 'ally': False},
]


def build_world_decor():
    """Construye el escenario base y coloca los tótems representativos de los 11 Easter Eggs."""
    tags = []

    # Casas alrededor del escenario
    build_house((-29, 0, 27), rot_y=140, wall_col=color.smoke, roof_col=color.brown)
    build_house((27, 0, -29), rot_y=-40, wall_col=color.peach, roof_col=color.red)
    build_house((-29, 0, -27), rot_y=45, wall_col=color.light_gray, roof_col=color.dark_gray)

    # Fuego en el campo
    fires = []
    for fpos in [(-12, 0, 4), (13, 0, 22), (-24, 0, -4), (6, 0, -26), (29, 0, 4)]:
        fires.append(build_camp_fire(fpos))

    # Cielo: Sol sonriente con lentes, nubes felices y avión en llamas
    sun = build_smiling_sun((22, 32, 46))
    clouds = [
        build_happy_cloud((-24, 24, 30), rot_y=20),
        build_happy_cloud((0, 26, -32), rot_y=180),
        build_happy_cloud((30, 23, 8), rot_y=-80),
        build_happy_cloud((-28, 25, -18), rot_y=60),
    ]
    plane, plane_flames = build_burning_plane()

    # Tótems iniciales de Easter Eggs
    eggs = {}
    for spec in EASTER_EGG_DEFS:
        totem = _make_totem(spec['id'], spec['pos'], tags)
        eggs[spec['id']] = {
            **spec,
            'totem': totem,
            'entity': None,
            'activated': False,
            'attack_cd': 0.0,
            'swing_t': 0.0,
            'walk_phase': 0.0,
        }

    return {
        't': 0.0,
        'tags': tags,
        'fires': fires,
        'sun': sun,
        'clouds': clouds,
        'plane': plane,
        'plane_flames': plane_flames,
        'eggs': eggs,
        'found_count': 0,
        'total_eggs': len(EASTER_EGG_DEFS),
    }


def activate_easter_egg(decor, egg_id, spawn_effect_fn, show_banner_fn, custom_pos=None):
    """Activa un Easter Egg al disparar a su tótem y lo añade al mapa sin quitar los demás."""
    egg = decor['eggs'].get(egg_id)
    if egg is None or egg['activated']:
        return False

    egg['activated'] = True
    decor['found_count'] += 1

    spawn_pos = custom_pos if custom_pos is not None else egg['pos']
    if egg['totem'] is not None:
        # Limpiar etiqueta asociada si existe
        for child in list(egg['totem'].children):
            if child in decor['tags']:
                decor['tags'].remove(child)
        spawn_effect_fn(Vec3(egg['totem'].world_position), col=egg['col'], size=0.45, life=0.4)
        destroy(egg['totem'])
        egg['totem'] = None

    egg['entity'] = egg['builder'](spawn_pos, egg['rot_y'], decor['tags'])
    show_banner_fn(
        f"EASTER EGG ({decor['found_count']}/{decor['total_eggs']}): {egg['name']} aparecio!",
        egg['col'],
        duration=2.8,
    )
    return True


def reset_easter_eggs(decor):
    """Elimina los personajes/vehículos invocados y restaura todos los tótems."""
    for egg in decor['eggs'].values():
        if egg['entity'] is not None:
            for child in list(egg['entity'].children):
                if child in decor['tags']:
                    decor['tags'].remove(child)
            destroy(egg['entity'])
            egg['entity'] = None
        if egg['totem'] is not None:
            for child in list(egg['totem'].children):
                if child in decor['tags']:
                    decor['tags'].remove(child)
            destroy(egg['totem'])
        egg['totem'] = _make_totem(egg['id'], egg['pos'], decor['tags'])
        egg['activated'] = False
        egg['attack_cd'] = 0.0
        egg['swing_t'] = 0.0
        egg['walk_phase'] = 0.0
    decor['found_count'] = 0


def _update_ally_egg(egg, player, zombies, damage_zombie_fn, arena_half, dt):
    ent = egg['entity']
    if ent is None:
        return
    parts = getattr(ent, 'anim_parts', {})
    egg['attack_cd'] = max(0.0, egg['attack_cd'] - dt)
    egg['swing_t'] = max(0.0, egg['swing_t'] - dt)

    # Buscar zombie más cercano o seguir al jugador a distancia amigable
    target = None
    best_d2 = 999999.0
    for z in zombies:
        d2 = (z.x - ent.x) ** 2 + (z.z - ent.z) ** 2
        if d2 < best_d2:
            best_d2 = d2
            target = z

    if target is not None:
        dx, dz = target.x - ent.x, target.z - ent.z
        dist = (dx * dx + dz * dz) ** 0.5
        stop_dist = egg['range'] * 0.8
        speed = egg['speed']
    else:
        dx, dz = player.x - ent.x, player.z - ent.z
        dist = (dx * dx + dz * dz) ** 0.5
        stop_dist = 4.0
        speed = egg['speed'] * 0.85

    if dist > 0.01:
        ent.rotation_y = degrees(atan2(dx, dz))

    if dist > stop_dist:
        move_dir = Vec3(dx / dist, 0, dz / dist)
        ent.position += move_dir * speed * dt
        egg['walk_phase'] += dt * 11.0
        swing = sin(egg['walk_phase']) * 30.0
        if 'leg_l' in parts:
            parts['leg_l'].rotation_x = swing
            parts['leg_r'].rotation_x = -swing
    else:
        if 'leg_l' in parts:
            parts['leg_l'].rotation_x = lerp(parts['leg_l'].rotation_x, 0.0, min(1.0, dt * 12))
            parts['leg_r'].rotation_x = lerp(parts['leg_r'].rotation_x, 0.0, min(1.0, dt * 12))

    ent.x = max(-arena_half + 1.5, min(arena_half - 1.5, ent.x))
    ent.z = max(-arena_half + 1.5, min(arena_half - 1.5, ent.z))

    if target is not None and dist <= egg['range'] and egg['attack_cd'] <= 0.0:
        egg['attack_cd'] = egg['cd']
        egg['swing_t'] = 0.22
        if 'arm' in parts:
            parts['arm'].rotation_x = 70
        damage_zombie_fn(target, egg['dmg'], False, target.world_position + Vec3(0, 1.1, 0), is_melee=True)

    if 'arm' in parts and egg['swing_t'] <= 0.0:
        parts['arm'].rotation_x = lerp(parts['arm'].rotation_x, 0.0, min(1.0, dt * 14))


def update_world_decor(decor, player, zombies, damage_zombie_fn, arena_half, dt, freeze_allies=False):
    """Anima escenario, tótems flotantes, Easter Eggs activos y aliados."""
    decor['t'] += dt
    t = decor['t']

    for tag in decor['tags']:
        tag.world_rotation_y = player.rotation_y

    # Sol, nubes y avión en llamas
    decor['sun'].rotation_z = sin(t * 0.8) * 6.0
    for idx, cl in enumerate(decor['clouds']):
        cl.y += sin(t * 1.1 + idx) * dt * 0.35
        cl.x += cos(t * 0.25 + idx * 1.5) * dt * 0.6

    orbit_ang = t * 0.45
    px, pz = sin(orbit_ang) * 24.0, cos(orbit_ang) * 24.0
    nx, nz = sin(orbit_ang + 0.05) * 24.0, cos(orbit_ang + 0.05) * 24.0
    plane = decor['plane']
    plane.position = Vec3(px, 19.0 + sin(t * 2.0) * 0.8, pz)
    plane.rotation_y = degrees(atan2(nx - px, nz - pz))
    plane.rotation_z = -18.0
    for idx, fl in enumerate(decor['plane_flames']):
        s = 0.8 + abs(sin(t * 18.0 + idx)) * 0.7
        fl.scale = Vec3(0.8 * s, 0.8 * s, 1.4 * s)

    # Fuego en el campo
    for f_idx, (f1, f2, f3) in enumerate(decor['fires']):
        s1 = 0.85 + abs(sin(t * 11.0 + f_idx)) * 0.45
        s2 = 0.80 + abs(cos(t * 14.0 + f_idx * 2)) * 0.50
        f1.scale_y = 1.15 * s1
        f2.scale_y = 0.85 * s2
        f3.scale_y = 0.70 * s1

    # Tótems flotantes y personajes/vehículos activos
    for idx, egg in enumerate(decor['eggs'].values()):
        if not egg['activated'] and egg['totem'] is not None:
            egg['totem'].rotation_y += 55 * dt
            egg['totem'].y = egg['pos'][1] + sin(t * 2.8 + idx) * 0.14
            continue

        ent = egg['entity']
        if ent is None:
            continue

        parts = getattr(ent, 'anim_parts', {})
        if 'orb' in parts:
            parts['orb'].scale = 0.42 + abs(sin(t * 6.0)) * 0.14
        if 'spin_orb' in parts:
            parts['spin_orb'].rotation_y += 320 * dt
        if 'flame' in parts:
            parts['flame'].scale_y = 0.45 + abs(sin(t * 14.0)) * 0.25
        if 'cat_head' in parts:
            parts['cat_head'].rotation_y = sin(t * 1.4) * 14.0
            parts['cat_tail'].rotation_y = sin(t * 2.8) * 25.0
            parts['cat_toy'].y = 1.35 + sin(t * 2.5) * 0.14
            parts['cat_toy'].rotation_y += 90 * dt

        if egg['ally'] and not freeze_allies:
            _update_ally_egg(egg, player, zombies, damage_zombie_fn, arena_half, dt)
