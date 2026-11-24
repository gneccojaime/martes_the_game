from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from math import atan2, degrees, sin, cos, radians
import random as rng
from world_props import build_world_decor, update_world_decor, activate_easter_egg, reset_easter_eggs

# ==========================================
# 1. INICIALIZACIÓN DE LA APLICACIÓN
# ==========================================
app = Ursina()

window.title = "Sandbox Zombies 3D - Campana AK-47"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# ==========================================
# 2. ENTORNO: CIELO, LUCES Y ARENA
# ==========================================
Sky(color=color.rgb32(110, 178, 242))
DirectionalLight(y=12, z=-6, shadows=False)

ARENA_HALF = 40

ground = Entity(
    model='plane',
    collider='box',
    scale=ARENA_HALF * 2 + 4,
    texture='grass',
    texture_scale=(40, 40),
    shader=basic_lighting_shader,
)

# Muros perimetrales
wall_specs = [
    ((0, 2.5, ARENA_HALF), (ARENA_HALF * 2, 5, 2)),
    ((0, 2.5, -ARENA_HALF), (ARENA_HALF * 2, 5, 2)),
    ((ARENA_HALF, 2.5, 0), (2, 5, ARENA_HALF * 2)),
    ((-ARENA_HALF, 2.5, 0), (2, 5, ARENA_HALF * 2)),
]
for pos, sc in wall_specs:
    Entity(
        model='cube',
        collider='box',
        position=pos,
        scale=sc,
        color=color.dark_gray,
        texture='white_cube',
        texture_scale=(max(1, int(sc[0] / 2)), max(1, int(sc[2] / 2))),
        shader=basic_lighting_shader,
    )

# Obstáculos y coberturas en el sandbox
cover_specs = [
    ((-10, 1, 10), (3, 2, 3), color.gray),
    ((10, 1, 14), (4, 2, 2.5), color.gray),
    ((-14, 1, -10), (3, 2, 4), color.gray),
    ((12, 1, -12), (3.5, 2, 3.5), color.gray),
    ((0, 1.25, 20), (6, 2.5, 2), color.brown),
    ((0, 1.25, -20), (6, 2.5, 2), color.brown),
    ((-22, 1.25, 2), (2, 2.5, 6), color.brown),
    ((22, 1.25, -2), (2, 2.5, 6), color.brown),
]
for pos, sc, col in cover_specs:
    Entity(
        model='cube',
        collider='box',
        position=pos,
        scale=sc,
        color=col,
        texture='white_cube',
        texture_scale=(2, 2),
        shader=basic_lighting_shader,
    )

# ==========================================
# 3. JUGADOR, VISTA 3ª PERSONA Y ARMAS (AK-47 + MELEE)
# ==========================================
player = FirstPersonController(
    position=(0, 0.5, 0),
    speed=8,
    mouse_sensitivity=Vec2(40, 40),
)

# Modelo del jugador visible en 3ª persona (sin colliders para no bloquear disparos)
player_visual = Entity(parent=player, enabled=False)
Entity(parent=player_visual, model='cube', color=color.azure, scale=(0.72, 0.85, 0.42), y=1.08, shader=basic_lighting_shader)
Entity(parent=player_visual, model='cube', color=color.dark_gray, scale=(0.76, 0.50, 0.46), y=1.12, shader=basic_lighting_shader)
tp_head = Entity(parent=player_visual, model='cube', color=color.peach, scale=(0.48, 0.48, 0.48), y=1.76, shader=basic_lighting_shader)
Entity(parent=tp_head, model='cube', color=color.black, scale=(0.82, 0.25, 0.15), position=(0, 0.12, 0.48))
tp_leg_l = Entity(parent=player_visual, model='cube', color=color.dark_gray, scale=(0.28, 0.72, 0.30), position=(-0.19, 0.36, 0), shader=basic_lighting_shader)
tp_leg_r = Entity(parent=player_visual, model='cube', color=color.dark_gray, scale=(0.28, 0.72, 0.30), position=(0.19, 0.36, 0), shader=basic_lighting_shader)

tp_arm_pivot = Entity(parent=player_visual, position=(0.48, 1.32, 0.12))
Entity(parent=tp_arm_pivot, model='cube', color=color.azure, scale=(0.22, 0.22, 0.62), position=(0, 0, 0.24), shader=basic_lighting_shader)
tp_ak = Entity(parent=tp_arm_pivot, position=(0, -0.02, 0.58))
Entity(parent=tp_ak, model='cube', color=color.dark_gray, scale=(0.08, 0.10, 0.52), shader=basic_lighting_shader)
Entity(parent=tp_ak, model='cube', color=color.brown, scale=(0.07, 0.08, 0.25), position=(0, -0.02, -0.22), shader=basic_lighting_shader)
Entity(parent=tp_ak, model='cube', color=color.dark_gray, scale=(0.05, 0.18, 0.08), position=(0, -0.12, 0.08), rotation_x=-18, shader=basic_lighting_shader)

tp_melee = Entity(parent=tp_arm_pivot, position=(0, 0.05, 0.56), enabled=False)
Entity(parent=tp_melee, model='cube', color=color.brown, scale=(0.05, 0.05, 0.20), rotation_x=65, shader=basic_lighting_shader)
Entity(parent=tp_melee, model='cube', color=color.light_gray, scale=(0.025, 0.09, 0.52), position=(0, 0.22, 0.14), rotation_x=65, shader=basic_lighting_shader)

# --- Vista 1ª persona: AK-47 ---
AK_REST_POS = Vec3(0.38, -0.30, 0.58)
ak_pivot = Entity(parent=camera, position=AK_REST_POS, rotation=(0, 0, 0))

# Cuerpo metálico y cañón del AK-47 (sin colliders para no bloquear disparos)
Entity(parent=ak_pivot, model='cube', color=color.dark_gray, scale=(0.08, 0.11, 0.42), shader=basic_lighting_shader)
Entity(parent=ak_pivot, model='cube', color=color.black, scale=(0.032, 0.032, 0.42), position=(0, 0.025, 0.38), shader=basic_lighting_shader)
Entity(parent=ak_pivot, model='cube', color=color.black, scale=(0.024, 0.024, 0.22), position=(0, 0.055, 0.25), shader=basic_lighting_shader)
# Guardamanos, culata y empuñadura de madera
Entity(parent=ak_pivot, model='cube', color=color.brown, scale=(0.072, 0.075, 0.22), position=(0, 0.005, 0.25), shader=basic_lighting_shader)
Entity(parent=ak_pivot, model='cube', color=color.brown, scale=(0.065, 0.11, 0.28), position=(0, -0.02, -0.30), shader=basic_lighting_shader)
Entity(parent=ak_pivot, model='cube', color=color.brown, scale=(0.055, 0.13, 0.07), position=(0, -0.10, -0.09), rotation_x=16, shader=basic_lighting_shader)
# Cargador curvo característico
Entity(parent=ak_pivot, model='cube', color=color.dark_gray, scale=(0.052, 0.15, 0.085), position=(0, -0.12, 0.07), rotation_x=-14, shader=basic_lighting_shader)
Entity(parent=ak_pivot, model='cube', color=color.dark_gray, scale=(0.050, 0.13, 0.080), position=(0, -0.23, 0.105), rotation_x=-26, shader=basic_lighting_shader)
# Mira delantera
Entity(parent=ak_pivot, model='cube', color=color.black, scale=(0.015, 0.04, 0.015), position=(0, 0.055, 0.56))

muzzle_flash = Entity(
    parent=ak_pivot,
    model='sphere',
    color=color.yellow,
    scale=0.095,
    position=(0, 0.025, 0.62),
    enabled=False,
)

# --- Vista 1ª persona: Machete Táctico (Melee) ---
MELEE_REST_POS = Vec3(0.42, -0.32, 0.56)
MELEE_REST_ROT = Vec3(10, -18, 12)
melee_pivot = Entity(parent=camera, position=MELEE_REST_POS, rotation=MELEE_REST_ROT, enabled=False)
Entity(parent=melee_pivot, model='cube', color=color.brown, scale=(0.045, 0.16, 0.055), position=(0, -0.05, 0), shader=basic_lighting_shader)
Entity(parent=melee_pivot, model='cube', color=color.dark_gray, scale=(0.085, 0.025, 0.085), position=(0, 0.04, 0), shader=basic_lighting_shader)
Entity(parent=melee_pivot, model='cube', color=color.light_gray, scale=(0.022, 0.44, 0.075), position=(0, 0.27, 0.01), shader=basic_lighting_shader)
Entity(parent=melee_pivot, model='cube', color=color.smoke, scale=(0.012, 0.44, 0.02), position=(0, 0.27, 0.045))

# ==========================================
# 4. ESTADO DEL JUEGO Y LISTAS
# ==========================================
MAG_SIZE = 30
START_RESERVE = 120
FIRE_INTERVAL = 0.11
RELOAD_DURATION = 1.35
MELEE_COOLDOWN = 0.42
MELEE_RANGE = 3.4

zombies = []
pickups = []
effects = []

state = {
    'hp': 100,
    'max_hp': 100,
    'weapon': 'ak47',
    'third_person': False,
    'walk_phase': 0.0,
    'ammo_mag': MAG_SIZE,
    'ammo_reserve': START_RESERVE,
    'reloading': False,
    'reload_timer': 0.0,
    'fire_timer': 0.0,
    'melee_timer': 0.0,
    'swing_timer': 0.0,
    'flash_timer': 0.0,
    'wave': 1,
    'wave_pending': False,
    'wave_delay': 0.0,
    'kills': 0,
    'score': 0,
    'game_over': False,
    'paused': False,
    'banner_timer': None,
    'damage_alpha': 0.0,
}

# ==========================================
# 5. HUD, OVERLAYS Y MENÚ DE PAUSA
# ==========================================
damage_overlay = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2.2, 1.4),
    color=color.rgba(1, 0, 0, 0),
    z=1,
)

hud_stats = Text(text='', position=(-0.85, 0.46), scale=1.1, color=color.white)
hud_ammo = Text(text='', position=(-0.85, 0.41), scale=1.05, color=color.yellow)
hud_controls = Text(
    text='WASD: Mover | Shift: Correr | Clic Izq: Atacar | 1/2 o Q: Arma | R: Recargar | V: 1a/3a Persona | Esc/P: Pausa',
    position=(-0.85, -0.45),
    scale=0.72,
    color=color.smoke,
)
banner_text = Text(text='', origin=(0, 0), position=(0, 0.34), scale=1.35, color=color.white)

# Menú de pausa
pause_menu = Entity(parent=camera.ui, enabled=False, z=-2)
Entity(parent=pause_menu, model='quad', scale=(2.2, 1.4), color=color.rgba(0, 0, 0, 0.65), z=0.1)
Entity(parent=pause_menu, model='quad', scale=(0.56, 0.56), color=color.rgb32(28, 34, 48), z=0.05)
Text(parent=pause_menu, text='PAUSA', origin=(0, 0), position=(0, 0.19), scale=2.2, color=color.yellow, z=-0.02)
Text(parent=pause_menu, text='Presiona Esc o P para continuar', origin=(0, 0), position=(0, 0.12), scale=0.85, color=color.light_gray, z=-0.02)


def set_paused(paused):
    """Activa o desactiva el menú de pausa y libera/bloquea el ratón."""
    state['paused'] = paused
    pause_menu.enabled = paused
    player.enabled = not paused
    if not paused:
        state['fire_timer'] = 0.2
        state['melee_timer'] = 0.2


btn_resume = Button(
    parent=pause_menu,
    text='Reanudar',
    color=color.azure,
    scale=(0.38, 0.08),
    position=(0, 0.03),
    z=-0.02,
    on_click=lambda: set_paused(False),
)
btn_restart = Button(
    parent=pause_menu,
    text='Reiniciar Partida',
    color=color.orange,
    scale=(0.38, 0.08),
    position=(0, -0.07),
    z=-0.02,
)
btn_quit = Button(
    parent=pause_menu,
    text='Salir del Juego',
    color=color.red,
    scale=(0.38, 0.08),
    position=(0, -0.17),
    z=-0.02,
    on_click=application.quit,
)


def show_banner(msg, msg_color=color.white, duration=2.0):
    banner_text.text = msg
    banner_text.color = msg_color
    banner_text.enabled = True
    state['banner_timer'] = duration


def spawn_effect(pos, col=color.light_gray, size=0.14, life=0.18):
    fx = Entity(model='cube', position=pos, scale=size, color=col)
    fx.life = life
    effects.append(fx)


def spawn_pickup(pos, kind=None):
    if kind is None:
        kind = 'medkit' if rng.random() < 0.4 else 'ammo'
    col = color.lime if kind == 'medkit' else color.gold
    box = Entity(
        model='cube',
        position=(pos.x, 0.45, pos.z),
        scale=(0.65, 0.65, 0.65),
        color=col,
        shader=basic_lighting_shader,
    )
    box.kind = kind
    pickups.append(box)


def create_zombie(kind='normal'):
    """Genera un zombie en el borde del sandbox según el tipo."""
    angle = rng.uniform(0, 360)
    dist = rng.uniform(24, 36)
    sx = max(-36, min(36, sin(radians(angle)) * dist))
    sz = max(-36, min(36, cos(radians(angle)) * dist))

    if kind == 'runner':
        max_hp, spd, scale_mult, body_col, head_col, dmg, pts = (
            70, 5.2, 0.92, color.orange, color.peach, 12, 120
        )
    elif kind == 'tank':
        max_hp, spd, scale_mult, body_col, head_col, dmg, pts = (
            240, 2.3, 1.35, color.violet, color.magenta, 25, 250
        )
    else:
        max_hp, spd, scale_mult, body_col, head_col, dmg, pts = (
            100, 3.3, 1.0, color.olive, color.lime, 15, 100
        )

    root = Entity(position=(sx, 0, sz), scale=scale_mult)
    root.hp = max_hp
    root.max_hp = max_hp
    root.speed = spd
    root.damage = dmg
    root.points = pts
    root.attack_cooldown = 0.0
    root.hit_flash = 0.0
    root.base_body_col = body_col
    root.base_head_col = head_col
    root.strafe_dir = rng.choice((-1, 1))

    # Hitboxes principales (cuerpo y cabeza)
    root.body = Entity(
        parent=root,
        model='cube',
        collider='box',
        scale=(0.85, 1.35, 0.55),
        y=0.675,
        color=body_col,
        shader=basic_lighting_shader,
    )
    root.body.owner = root
    root.body.is_head = False

    root.head = Entity(
        parent=root,
        model='cube',
        collider='box',
        scale=(0.55, 0.55, 0.55),
        y=1.65,
        color=head_col,
        shader=basic_lighting_shader,
    )
    root.head.owner = root
    root.head.is_head = True

    # Brazos y ojos (solo visuales, sin collider)
    Entity(parent=root, model='cube', color=body_col, scale=(0.24, 0.24, 0.85), position=(-0.54, 1.15, 0.42), shader=basic_lighting_shader)
    Entity(parent=root, model='cube', color=body_col, scale=(0.24, 0.24, 0.85), position=(0.54, 1.15, 0.42), shader=basic_lighting_shader)
    Entity(parent=root.head, model='cube', color=color.red, scale=(0.18, 0.18, 0.08), position=(-0.22, 0.1, 0.51))
    Entity(parent=root.head, model='cube', color=color.red, scale=(0.18, 0.18, 0.08), position=(0.22, 0.1, 0.51))

    # Barra de vida sobre la cabeza
    root.hp_bg = Entity(parent=root, model='cube', color=color.black, scale=(0.95, 0.11, 0.04), y=2.25)
    root.hp_fill = Entity(parent=root.hp_bg, model='cube', color=color.red, scale=(0.96, 0.78, 1.2), z=-0.4)

    zombies.append(root)
    return root


def start_wave(wave_num):
    """Genera los zombies de la oleada indicada."""
    state['wave'] = wave_num
    state['wave_pending'] = False
    total = 4 + wave_num * 2

    for _ in range(total):
        roll = rng.random()
        if wave_num >= 3 and roll < 0.22:
            kind = 'tank'
        elif wave_num >= 2 and roll < 0.52:
            kind = 'runner'
        else:
            kind = 'normal'
        create_zombie(kind)

    show_banner(f'OLEADA {wave_num} - {total} Zombies!', color.yellow, duration=2.5)


def damage_zombie(zombie, amount, is_headshot, hit_point, is_melee=False):
    zombie.hp -= amount
    spawn_effect(hit_point, col=color.yellow if is_headshot else color.red, size=0.18 if is_headshot else 0.13)

    if zombie.hp <= 0:
        state['kills'] += 1
        bonus = (50 if is_headshot else 0) + (25 if is_melee else 0)
        state['score'] += zombie.points + bonus
        if is_headshot:
            show_banner('HEADSHOT!', color.yellow, duration=0.8)
        elif is_melee:
            show_banner('BAJA MELEE! +25', color.cyan, duration=0.8)
        drop_chance = 0.50 if is_melee else 0.35
        if rng.random() < drop_chance:
            spawn_pickup(zombie.world_position)
        zombies.remove(zombie)
        destroy(zombie)
    else:
        ratio = max(0.01, zombie.hp / zombie.max_hp)
        zombie.hp_fill.scale_x = 0.96 * ratio
        zombie.hp_fill.x = -0.48 * (1 - ratio)
        zombie.hit_flash = 0.08
        zombie.body.color = color.white
        zombie.head.color = color.white


def sync_weapon_models():
    """Muestra el modelo de arma activo según vista (1ª o 3ª persona)."""
    is_ak = state['weapon'] == 'ak47'
    tp = state['third_person']
    player_visual.enabled = tp
    ak_pivot.enabled = is_ak and not tp
    melee_pivot.enabled = (not is_ak) and not tp
    tp_ak.enabled = is_ak
    tp_melee.enabled = not is_ak


def equip_weapon(weapon_name):
    if state['weapon'] == weapon_name:
        return
    state['weapon'] = weapon_name
    state['reloading'] = False
    muzzle_flash.enabled = False
    sync_weapon_models()
    label = 'AK-47 [1]' if weapon_name == 'ak47' else 'Machete Melee [2]'
    show_banner(f'Equipado: {label}', color.white, duration=1.0)


def toggle_view():
    state['third_person'] = not state['third_person']
    if not state['third_person']:
        camera.position = Vec3(0, 0, 0)
    sync_weapon_models()
    show_banner(
        'Vista: 3a Persona' if state['third_person'] else 'Vista: 1a Persona',
        color.cyan,
        duration=1.2,
    )


def get_aim_ray_origin():
    """Origen de disparo: en 3ª persona parte a la altura del jugador para no golpear detrás."""
    if not state['third_person']:
        return camera.world_position
    return camera.world_position + camera.forward * max(0.0, abs(camera.z) - 0.15)


def start_reload():
    if (
        state['weapon'] != 'ak47'
        or state['reloading']
        or state['ammo_mag'] >= MAG_SIZE
        or state['ammo_reserve'] <= 0
    ):
        return
    state['reloading'] = True
    state['reload_timer'] = RELOAD_DURATION
    show_banner('Recargando...', color.cyan, duration=RELOAD_DURATION)


def fire_ak47():
    if state['reloading'] or state['fire_timer'] > 0.0:
        return
    if state['ammo_mag'] <= 0:
        if state['ammo_reserve'] > 0:
            start_reload()
        else:
            state['fire_timer'] = 0.25
            show_banner('Sin municion! Usa Machete [2] o busca cajas', color.red, duration=1.2)
        return

    state['ammo_mag'] -= 1
    state['fire_timer'] = FIRE_INTERVAL

    # Retroceso visual del AK-47 y fogonazo
    ak_pivot.z = AK_REST_POS.z - 0.085
    ak_pivot.rotation_x = 6.0
    player.camera_pivot.rotation_x = clamp(player.camera_pivot.rotation_x - 0.65, -90, 90)
    if not state['third_person']:
        muzzle_flash.enabled = True
        state['flash_timer'] = 0.045

    hit = raycast(
        get_aim_ray_origin(),
        camera.forward,
        distance=100,
        ignore=[player],
    )
    if hit.hit:
        if hasattr(hit.entity, 'easter_egg_id'):
            activate_easter_egg(world_decor, hit.entity.easter_egg_id, spawn_effect, show_banner)
            return
        if hasattr(hit.entity, 'ally_dialogue'):
            msg, col = hit.entity.ally_dialogue
            spawn_effect(hit.world_point, col=col, size=0.14, life=0.2)
            show_banner(msg, col, duration=1.2)
            return
        owner = getattr(hit.entity, 'owner', None)
        if owner is not None and owner in zombies:
            is_head = getattr(hit.entity, 'is_head', False)
            dmg = 100 if is_head else 35
            damage_zombie(owner, dmg, is_head, hit.world_point)
        else:
            spawn_effect(hit.world_point, col=color.light_gray, size=0.10, life=0.18)


def swing_melee():
    """Ataque cuerpo a cuerpo con el machete: arco frontal y empuje."""
    if state['melee_timer'] > 0.0:
        return
    state['melee_timer'] = MELEE_COOLDOWN
    state['swing_timer'] = 0.20

    # Animación inmediata del tajo
    melee_pivot.position = Vec3(0.08, -0.22, 0.72)
    melee_pivot.rotation = Vec3(58, 35, 65)
    tp_arm_pivot.rotation_x = 55

    ray_origin = get_aim_ray_origin()
    hit = raycast(ray_origin, camera.forward, distance=MELEE_RANGE, ignore=[player])
    if hit.hit:
        if hasattr(hit.entity, 'easter_egg_id'):
            activate_easter_egg(world_decor, hit.entity.easter_egg_id, spawn_effect, show_banner)
            return
        if hasattr(hit.entity, 'ally_dialogue'):
            msg, col = hit.entity.ally_dialogue
            show_banner(msg, col, duration=1.2)
            return
        owner = getattr(hit.entity, 'owner', None)
        if owner is not None and owner in zombies:
            is_head = getattr(hit.entity, 'is_head', False)
            dmg = 120 if is_head else 65
            knock = Vec3(camera.forward.x, 0, camera.forward.z)
            if knock.length() > 0.01:
                owner.position += knock.normalized() * 1.4
            damage_zombie(owner, dmg, is_head, hit.world_point, is_melee=True)
            return
        spawn_effect(hit.world_point, col=color.light_gray, size=0.10, life=0.15)

    # Si no dio el rayo fino central, buscamos el zombie más cercano en arco frontal
    fwd_xz = Vec3(camera.forward.x, 0, camera.forward.z)
    if fwd_xz.length() < 0.01:
        return
    fwd_xz = fwd_xz.normalized()

    best_target = None
    best_dist = MELEE_RANGE + 0.1
    for z in zombies:
        to_z = Vec3(z.x - player.x, 0, z.z - player.z)
        d = to_z.length()
        if 0.01 < d <= MELEE_RANGE and abs(z.y - player.y) < 2.2:
            if to_z.normalized().dot(fwd_xz) > 0.35 and d < best_dist:
                best_dist = d
                best_target = z

    if best_target is not None:
        knock = Vec3(best_target.x - player.x, 0, best_target.z - player.z).normalized()
        best_target.position += knock * 1.4
        damage_zombie(best_target, 65, False, best_target.world_position + Vec3(0, 1.2, 0), is_melee=True)


def reset_game():
    if state['paused']:
        set_paused(False)

    for z in zombies:
        destroy(z)
    zombies.clear()

    for p in pickups:
        destroy(p)
    pickups.clear()

    for fx in effects:
        destroy(fx)
    effects.clear()

    reset_easter_eggs(world_decor)

    player.position = Vec3(0, 0.5, 0)
    player.air_time = 0
    player.grounded = False

    state['hp'] = state['max_hp']
    state['weapon'] = 'ak47'
    state['ammo_mag'] = MAG_SIZE
    state['ammo_reserve'] = START_RESERVE
    state['reloading'] = False
    state['reload_timer'] = 0.0
    state['fire_timer'] = 0.0
    state['melee_timer'] = 0.0
    state['swing_timer'] = 0.0
    state['flash_timer'] = 0.0
    state['kills'] = 0
    state['score'] = 0
    state['game_over'] = False
    state['damage_alpha'] = 0.0
    damage_overlay.color = color.rgba(1, 0, 0, 0)
    sync_weapon_models()

    start_wave(1)


btn_restart.on_click = reset_game


def update_hud():
    hp_color = color.lime if state['hp'] > 50 else (color.yellow if state['hp'] > 25 else color.red)
    hud_stats.color = hp_color
    view_str = '3a Persona' if state['third_person'] else '1a Persona'
    stats_str = (
        f"Salud: {state['hp']}/{state['max_hp']}  |  "
        f"Oleada: {state['wave']}  |  "
        f"Zombies: {len(zombies)}  |  "
        f"Bajas: {state['kills']}  |  "
        f"Puntos: {state['score']}  |  {view_str}"
    )
    if hud_stats.text != stats_str:
        hud_stats.text = stats_str

    if state['weapon'] == 'melee':
        ammo_str = 'Arma [2]: Machete (Melee)  |  Sin limite'
        hud_ammo.color = color.cyan
    else:
        hud_ammo.color = color.yellow
        ammo_str = (
            f"Arma [1]: AK-47  |  Recargando... ({state['ammo_reserve']})"
            if state['reloading']
            else f"Arma [1]: AK-47  |  {state['ammo_mag']} / {state['ammo_reserve']}"
        )
    if hud_ammo.text != ammo_str:
        hud_ammo.text = ammo_str


def update_third_person_camera(dt):
    """Posiciona la cámara sobre el hombro evitando atravesar muros y anima al personaje."""
    if state['third_person']:
        local_offset = Vec3(0.75, 0.45, -4.2)
        world_offset = (
            player.camera_pivot.right * local_offset.x
            + player.camera_pivot.up * local_offset.y
            + player.camera_pivot.forward * local_offset.z
        )
        dist = world_offset.length()
        cam_ray = raycast(
            player.camera_pivot.world_position,
            world_offset.normalized(),
            distance=dist,
            ignore=[player],
        )
        scale_factor = max(0.25, (cam_ray.distance - 0.3) / dist) if cam_ray.hit else 1.0
        camera.position = local_offset * scale_factor

        moving = any(held_keys[k] for k in ('w', 'a', 's', 'd'))
        if moving:
            state['walk_phase'] += dt * (13.0 if held_keys['left shift'] else 9.5)
            swing = sin(state['walk_phase']) * 28.0
            tp_leg_l.rotation_x = swing
            tp_leg_r.rotation_x = -swing
        else:
            tp_leg_l.rotation_x = lerp(tp_leg_l.rotation_x, 0.0, min(1.0, dt * 12))
            tp_leg_r.rotation_x = lerp(tp_leg_r.rotation_x, 0.0, min(1.0, dt * 12))

        tp_arm_pivot.rotation_x = lerp(tp_arm_pivot.rotation_x, 0.0, min(1.0, dt * 12))


# ==========================================
# 6. CICLO PRINCIPAL Y ENTRADAS
# ==========================================
def update():
    if state['paused']:
        return

    dt = time.dt

    if state['banner_timer'] is not None:
        state['banner_timer'] -= dt
        if state['banner_timer'] <= 0:
            banner_text.enabled = False
            state['banner_timer'] = None

    # Desvanecer overlay rojo de daño
    if state['damage_alpha'] > 0:
        state['damage_alpha'] = max(0.0, state['damage_alpha'] - dt * 1.4)
        damage_overlay.color = color.rgba(1, 0, 0, state['damage_alpha'])

    # Actualizar partículas de impacto
    for fx in list(effects):
        fx.life -= dt
        if fx.life <= 0:
            effects.remove(fx)
            destroy(fx)

    if state['game_over']:
        player.speed = 0
        update_hud()
        return

    # Velocidad del jugador y límites del arena
    player.speed = 11.5 if held_keys['left shift'] else 8
    player.x = clamp(player.x, -ARENA_HALF + 1.5, ARENA_HALF - 1.5)
    player.z = clamp(player.z, -ARENA_HALF + 1.5, ARENA_HALF - 1.5)
    if player.y < -5:
        player.position = Vec3(0, 1, 0)

    # Temporizadores de armas
    state['fire_timer'] = max(0.0, state['fire_timer'] - dt)
    state['melee_timer'] = max(0.0, state['melee_timer'] - dt)
    state['swing_timer'] = max(0.0, state['swing_timer'] - dt)
    if state['flash_timer'] > 0:
        state['flash_timer'] -= dt
        if state['flash_timer'] <= 0:
            muzzle_flash.enabled = False

    if state['reloading']:
        state['reload_timer'] -= dt
        if state['reload_timer'] <= 0:
            needed = MAG_SIZE - state['ammo_mag']
            taken = min(needed, state['ammo_reserve'])
            state['ammo_mag'] += taken
            state['ammo_reserve'] -= taken
            state['reloading'] = False

    # Disparo continuo con AK-47 o tajo con Machete
    if mouse.left:
        if state['weapon'] == 'ak47':
            fire_ak47()
        else:
            swing_melee()

    # Recuperación suave de los viewmodels en 1ª persona y cámara en 3ª persona
    target_tilt = -32.0 if state['reloading'] else 0.0
    ak_pivot.z = lerp(ak_pivot.z, AK_REST_POS.z, min(1.0, dt * 15))
    ak_pivot.rotation_x = lerp(ak_pivot.rotation_x, target_tilt, min(1.0, dt * 12))

    if state['swing_timer'] <= 0.0:
        melee_pivot.position = lerp(melee_pivot.position, MELEE_REST_POS, min(1.0, dt * 14))
        melee_pivot.rotation = lerp(melee_pivot.rotation, MELEE_REST_ROT, min(1.0, dt * 14))

    update_third_person_camera(dt)
    update_world_decor(world_decor, player, zombies, damage_zombie, ARENA_HALF, dt, freeze_allies=state['game_over'])

    # Recoger cajas de suministros
    for box in list(pickups):
        box.rotation_y += 90 * dt
        dx = player.x - box.x
        dz = player.z - box.z
        if dx * dx + dz * dz < 3.2:
            if box.kind == 'medkit':
                state['hp'] = min(state['max_hp'], state['hp'] + 25)
                show_banner('+25 Salud!', color.lime, duration=1.2)
            else:
                state['ammo_reserve'] += 45
                show_banner('+45 Balas AK-47!', color.gold, duration=1.2)
            pickups.remove(box)
            destroy(box)

    # Actualizar zombies
    for z in zombies:
        z.attack_cooldown = max(0.0, z.attack_cooldown - dt)
        if z.hit_flash > 0.0:
            z.hit_flash -= dt
            if z.hit_flash <= 0.0:
                z.body.color = z.base_body_col
                z.head.color = z.base_head_col
        z.hp_bg.world_rotation_y = player.rotation_y

        dx = player.x - z.x
        dz = player.z - z.z
        dist_sq = dx * dx + dz * dz
        dist = dist_sq ** 0.5

        if dist > 0.01:
            z.rotation_y = degrees(atan2(dx, dz))
            move_dir = Vec3(dx / dist, 0, dz / dist)

            if dist > 1.5:
                front_ray = raycast(
                    z.world_position + Vec3(0, 0.8, 0),
                    move_dir,
                    distance=0.9,
                    ignore=[z, z.body, z.head],
                )
                if front_ray.hit and getattr(front_ray.entity, 'owner', None) is None:
                    side = Vec3(-move_dir.z * z.strafe_dir, 0, move_dir.x * z.strafe_dir)
                    z.position += side * z.speed * dt
                else:
                    z.position += move_dir * z.speed * dt

        # Separación suave entre zombies para evitar apilamiento
        for other in zombies:
            if other is z:
                continue
            ox = z.x - other.x
            oz = z.z - other.z
            d2 = ox * ox + oz * oz
            if 0.001 < d2 < 1.3:
                d = d2 ** 0.5
                z.x += (ox / d) * dt * 2.0
                z.z += (oz / d) * dt * 2.0

        z.x = clamp(z.x, -ARENA_HALF + 1.5, ARENA_HALF - 1.5)
        z.z = clamp(z.z, -ARENA_HALF + 1.5, ARENA_HALF - 1.5)

        # Ataque cuerpo a cuerpo al jugador
        if dist < 1.85 and abs(player.y - z.y) < 1.8 and z.attack_cooldown <= 0.0:
            z.attack_cooldown = 1.0
            state['hp'] = max(0, state['hp'] - z.damage)
            state['damage_alpha'] = 0.42
            if state['hp'] <= 0:
                state['game_over'] = True
                show_banner(
                    f"GAME OVER - Oleada {state['wave']} | Bajas: {state['kills']} (Presiona T para reiniciar)",
                    color.red,
                    duration=None,
                )
                break

    # Transición entre oleadas
    if not state['game_over'] and len(zombies) == 0:
        if not state['wave_pending']:
            state['wave_pending'] = True
            state['wave_delay'] = 2.8
            show_banner(f"Oleada {state['wave']} superada! Siguiente oleada...", color.cyan, duration=2.5)
        else:
            state['wave_delay'] -= dt
            if state['wave_delay'] <= 0:
                start_wave(state['wave'] + 1)

    update_hud()


def input(key):
    if key in ('escape', 'p'):
        if state['game_over'] and key == 'escape':
            application.quit()
        elif not state['game_over']:
            set_paused(not state['paused'])
    elif state['paused']:
        return
    elif key == 'v' and not state['game_over']:
        toggle_view()
    elif key == 'm' and not state['game_over']:
        activate_steve_easter_egg(player.world_position + camera.forward * 3.5)
    elif key == '1' and not state['game_over']:
        equip_weapon('ak47')
    elif key == '2' and not state['game_over']:
        equip_weapon('melee')
    elif key in ('q', 'scroll up', 'scroll down') and not state['game_over']:
        equip_weapon('melee' if state['weapon'] == 'ak47' else 'ak47')
    elif key == 'left mouse down' and not state['game_over']:
        if state['weapon'] == 'ak47':
            fire_ak47()
        else:
            swing_melee()
    elif key == 'r' and not state['game_over']:
        start_reload()
    elif key == 't':
        reset_game()


world_decor = build_world_decor()
sync_weapon_models()
start_wave(1)

if __name__ == '__main__':
    app.run()
