from math import sin
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

# ==========================================
# 1. INICIALIZACIÓN DE LA APLICACIÓN
# ==========================================
app = Ursina()

window.title = "Sandbox Parkour 3D - Etapa 1"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# ==========================================
# 2. ENTORNO: CIELO Y LUCES
# ==========================================
sky = Sky(color=color.azure)
DirectionalLight(y=10, z=-5, shadows=False)

# ==========================================
# 3. COLECCIONES Y CONSTRUCTORES DE ETAPA
# ==========================================
stage_entities = []
moving_platforms = []
blinking_platforms = []
checkpoints = []
jump_pads = []
speed_pads = []
hazards = []
goal_refs = {'platform': None, 'trophy': None}

start_pos = Vec3(0, 0.5, 0)


def register_entity(entity):
    stage_entities.append(entity)
    return entity


def make_platform(x, top_y, z, scale=(4, 1, 4), plat_color=color.light_gray, **kwargs):
    """Crea una plataforma cúbica alineando su cara superior exactamente a `top_y`."""
    sy = scale[1]
    ent = Entity(
        model='cube',
        collider='box',
        position=(x, top_y - sy / 2, z),
        scale=scale,
        color=plat_color,
        texture='white_cube',
        texture_scale=(max(1, int(scale[0])), max(1, int(scale[2]))),
        shader=basic_lighting_shader,
        **kwargs,
    )
    return register_entity(ent)


def make_moving_platform(
    x, top_y, z, scale=(3.5, 1, 3.5), axis='x', amplitude=4.0, speed=1.4, plat_color=color.cyan
):
    """Crea una plataforma móvil oscilante en X, Y o Z."""
    plat = make_platform(x, top_y, z, scale=scale, plat_color=plat_color)
    plat.origin_pos = Vec3(plat.position)
    plat.axis = axis
    plat.amplitude = amplitude
    plat.speed = speed
    plat._phase = 0.0
    plat.delta = Vec3(0, 0, 0)
    moving_platforms.append(plat)
    return plat


def make_blinking_platform(
    x, top_y, z, scale=(3.2, 1, 3.2), phase_offset=0.0, base_color=color.yellow
):
    """Crea una plataforma temporal que avisa parpadeando antes de desaparecer."""
    plat = make_platform(x, top_y, z, scale=scale, plat_color=base_color)
    plat.base_color = base_color
    plat.phase_offset = phase_offset
    plat._timer = phase_offset
    blinking_platforms.append(plat)
    return plat


def make_checkpoint(index, x, top_y, z, scale=(6, 1, 5)):
    """Crea una plataforma de checkpoint con un pilar indicador lateral."""
    plat = make_platform(x, top_y, z, scale=scale, plat_color=color.orange)
    plat.checkpoint_index = index
    plat.respawn_pos = Vec3(x, top_y + 0.5, z)
    plat.activated = False

    beacon = Entity(
        parent=plat,
        model='cube',
        color=color.orange,
        scale=(0.08, 2.2, 0.08),
        position=(0.42, 1.5, 0),
        shader=basic_lighting_shader,
    )
    plat.beacon = beacon
    checkpoints.append(plat)
    return plat


def make_jump_pad(x, top_y, z, scale=(3, 0.4, 3), boost=5.8):
    """Crea un trampolín que impulsa al jugador hacia arriba al pisarlo."""
    pad = make_platform(x, top_y, z, scale=scale, plat_color=color.lime)
    pad.boost = boost
    jump_pads.append(pad)
    return pad


def make_speed_pad(x, top_y, z, scale=(3.2, 0.25, 4.0), speed_value=15.5, duration=2.5):
    """Crea una placa turbo que aumenta la velocidad al pisarla."""
    pad = make_platform(x, top_y, z, scale=scale, plat_color=color.turquoise)
    pad.speed_value = speed_value
    pad.boost_duration = duration
    speed_pads.append(pad)
    return pad


def make_hazard(x, y, z, scale=(4.3, 0.55, 0.6), axis='z', amplitude=2.2, speed=2.0, phase=0.0):
    """Crea una barra láser móvil que devuelve al jugador al checkpoint si lo toca."""
    bar = Entity(
        model='cube',
        position=(x, y, z),
        scale=scale,
        color=color.red,
        shader=basic_lighting_shader,
    )
    bar.origin_pos = Vec3(bar.position)
    bar.axis = axis
    bar.amplitude = amplitude
    bar.speed = speed
    bar._phase = phase
    hazards.append(bar)
    return register_entity(bar)


def make_goal(x, top_y, z, scale=(7, 1, 7)):
    """Crea la plataforma de meta y su trofeo giratorio."""
    goal = make_platform(x, top_y, z, scale=scale, plat_color=color.gold)
    trophy = Entity(
        model='cube',
        color=color.yellow,
        position=(x, top_y + 2.0, z),
        scale=(1.2, 1.2, 1.2),
        rotation=(25, 45, 0),
        shader=basic_lighting_shader,
    )
    register_entity(trophy)
    goal_refs['platform'] = goal
    goal_refs['trophy'] = trophy
    return goal


# ==========================================
# 4. DEFINICIÓN DE ETAPAS
# ==========================================
def build_stage_1():
    """Etapa 1: Circuito diurno clásico."""
    sky.color = color.azure
    window.title = "Sandbox Parkour 3D - Etapa 1"

    make_platform(0, 0, 0, scale=(8, 1, 8), plat_color=color.gray)

    # Tramo 1: Saltos básicos ascendentes
    make_platform(0, 0.5, 8.5, scale=(4, 1, 4), plat_color=color.azure)
    make_platform(2.5, 1.2, 14.5, scale=(3.5, 1, 3.5), plat_color=color.azure)
    make_platform(-1.5, 2.0, 20.0, scale=(3.5, 1, 3.5), plat_color=color.azure)
    make_platform(-1.5, 2.8, 26.0, scale=(3, 1, 3), plat_color=color.azure)

    make_checkpoint(1, 0, 3.2, 32.5)

    # Tramo 2: Vigas estrechas en zigzag
    make_platform(4.5, 3.6, 38.0, scale=(2.2, 1, 4), plat_color=color.violet)
    make_platform(-1.0, 4.2, 43.0, scale=(2.2, 1, 4), plat_color=color.violet)
    make_platform(3.5, 4.8, 48.0, scale=(2.2, 1, 3.5), plat_color=color.violet)

    # Tramo 3: Plataformas móviles
    make_moving_platform(0, 4.8, 54.0, scale=(3.5, 1, 3.5), axis='x', amplitude=4.0, speed=1.4)
    make_moving_platform(0, 5.3, 62.0, scale=(3.5, 1, 3.5), axis='z', amplitude=2.5, speed=1.5)

    make_checkpoint(2, 0, 5.8, 70.5)

    # Tramo 4: Trampolín y salto largo
    make_jump_pad(0, 6.2, 75.5, scale=(3, 0.4, 3), boost=5.8)
    make_platform(0, 9.5, 82.5, scale=(5, 1, 5), plat_color=color.magenta)
    make_platform(0, 9.5, 91.0, scale=(4, 1, 4), plat_color=color.magenta)

    # Tramo 5: Escalada final
    make_platform(4.5, 10.5, 95.5, scale=(3.2, 1, 3.2), plat_color=color.peach)
    make_platform(4.5, 11.6, 101.0, scale=(3.2, 1, 3.2), plat_color=color.peach)
    make_platform(0, 12.6, 106.5, scale=(3.2, 1, 3.2), plat_color=color.peach)

    make_goal(0, 13.2, 114.0, scale=(7, 1, 7))


def build_stage_2():
    """Etapa 2: Circuito nocturno con plataformas parpadeantes, láseres, ascensor y turbo."""
    sky.color = color.rgb32(20, 28, 58)
    window.title = "Sandbox Parkour 3D - Etapa 2 (Desafio Nocturno)"

    make_platform(0, 0, 0, scale=(8, 1, 8), plat_color=color.dark_gray)

    # Tramo 1: Plataformas que parpadean y desaparecen
    make_blinking_platform(0, 0.4, 7.5, scale=(3.5, 1, 3.5), phase_offset=0.0)
    make_blinking_platform(-2.5, 1.0, 13.0, scale=(3.2, 1, 3.2), phase_offset=2.0)
    make_blinking_platform(2.5, 1.6, 18.5, scale=(3.2, 1, 3.2), phase_offset=0.0)
    make_blinking_platform(0, 2.2, 24.5, scale=(3.2, 1, 3.2), phase_offset=2.0)

    make_checkpoint(1, 0, 2.6, 30.5)

    # Tramo 2: Puente con barredoras láser (saltar por encima)
    make_platform(0, 2.6, 42.5, scale=(4.5, 1, 16), plat_color=color.rgb32(60, 70, 110))
    make_hazard(0, 3.0, 38.5, scale=(4.3, 0.55, 0.6), axis='z', amplitude=2.2, speed=2.1, phase=0.0)
    make_hazard(0, 3.0, 46.5, scale=(4.3, 0.55, 0.6), axis='z', amplitude=2.2, speed=2.1, phase=3.14)

    # Tramo 3: Ascensor vertical y plataforma móvil rápida
    make_moving_platform(
        0, 3.0, 54.5, scale=(4, 1, 4), axis='y', amplitude=2.6, speed=1.3, plat_color=color.turquoise
    )
    make_platform(0, 5.8, 61.5, scale=(4, 1, 4), plat_color=color.violet)
    make_moving_platform(0, 6.2, 68.0, scale=(3.5, 1, 3.5), axis='x', amplitude=4.5, speed=1.6)

    make_checkpoint(2, 0, 6.6, 75.5)

    # Tramo 4: Placa Turbo + salto largo + doble trampolín aéreo
    make_platform(0, 6.6, 82.0, scale=(3.6, 1, 5.0), plat_color=color.azure)
    make_speed_pad(0, 6.8, 82.0, scale=(3.0, 0.25, 4.0), speed_value=15.5, duration=2.5)
    make_platform(0, 7.0, 91.0, scale=(4, 1, 4), plat_color=color.magenta)

    make_jump_pad(0, 7.3, 96.5, scale=(3.2, 0.4, 3.2), boost=6.0)
    make_platform(0, 10.8, 103.5, scale=(4, 1, 4), plat_color=color.peach)
    make_jump_pad(0, 11.1, 108.5, scale=(3.2, 0.4, 3.2), boost=6.2)

    make_goal(0, 14.8, 116.5, scale=(8, 1, 8))


STAGES = {
    1: build_stage_1,
    2: build_stage_2,
}

# ==========================================
# 5. JUGADOR Y ESTADO DEL JUEGO
# ==========================================
player = FirstPersonController(
    position=start_pos,
    speed=8,
    mouse_sensitivity=Vec2(40, 40),
)

state = {
    'stage': 1,
    'elapsed': 0.0,
    'running': False,
    'finished': False,
    'best_times': {1: None, 2: None},
    'falls': 0,
    'checkpoint_index': 0,
    'respawn_pos': Vec3(start_pos),
    'pad_cooldown': 0.0,
    'speed_boost_timer': 0.0,
    'speed_boost_value': 15.5,
    'banner_timer': None,
}

# ==========================================
# 6. INTERFAZ (HUD)
# ==========================================
hud_stats = Text(
    text='',
    position=(-0.85, 0.46),
    scale=1.1,
    color=color.white,
)
hud_best = Text(
    text='',
    position=(-0.85, 0.41),
    scale=0.95,
    color=color.yellow,
)
hud_controls = Text(
    text='WASD: Mover | Shift: Correr | Espacio: Saltar | R: Checkpoint | T: Reiniciar | 1/2: Etapa | Esc: Salir',
    position=(-0.85, -0.45),
    scale=0.82,
    color=color.smoke,
)
banner_text = Text(
    text='',
    origin=(0, 0),
    position=(0, 0.34),
    scale=1.35,
    color=color.white,
)


def show_banner(msg, msg_color=color.white, duration=2.5):
    """Muestra un mensaje temporal en la parte superior de la pantalla."""
    banner_text.text = msg
    banner_text.color = msg_color
    banner_text.enabled = True
    state['banner_timer'] = duration


def respawn_player(to_start=False):
    """Devuelve al jugador al último checkpoint (o al inicio si `to_start=True`)."""
    if hasattr(player, 'y_animator') and player.y_animator:
        player.y_animator.pause()
    player.air_time = 0
    player.grounded = False
    state['speed_boost_timer'] = 0.0
    player.position = Vec3(start_pos if to_start else state['respawn_pos'])


def clear_stage():
    """Destruye las entidades de la etapa actual antes de cargar otra."""
    for ent in stage_entities:
        destroy(ent)
    stage_entities.clear()
    moving_platforms.clear()
    blinking_platforms.clear()
    checkpoints.clear()
    jump_pads.clear()
    speed_pads.clear()
    hazards.clear()
    goal_refs['platform'] = None
    goal_refs['trophy'] = None


def load_stage(stage_num):
    """Carga la etapa indicada y reinicia contadores de intento."""
    clear_stage()
    state['stage'] = stage_num
    state['elapsed'] = 0.0
    state['running'] = False
    state['finished'] = False
    state['falls'] = 0
    state['checkpoint_index'] = 0
    state['respawn_pos'] = Vec3(start_pos)
    state['pad_cooldown'] = 0.0
    state['speed_boost_timer'] = 0.0

    STAGES[stage_num]()
    respawn_player(to_start=True)

    intro = (
        'Etapa 1: Llega a la plataforma dorada!'
        if stage_num == 1
        else 'Etapa 2: Cuidado con plataformas temporales y laseres!'
    )
    show_banner(intro, color.cyan if stage_num == 2 else color.white, duration=3.0)


def update_hud():
    stats_str = (
        f"Etapa {state['stage']}/2  |  "
        f"Tiempo: {state['elapsed']:.2f} s  |  "
        f"Checkpoint: {state['checkpoint_index']}/{len(checkpoints)}  |  "
        f"Caidas: {state['falls']}"
    )
    if hud_stats.text != stats_str:
        hud_stats.text = stats_str

    b1 = state['best_times'][1]
    b2 = state['best_times'][2]
    b1_str = f"{b1:.2f}s" if b1 is not None else '--'
    b2_str = f"{b2:.2f}s" if b2 is not None else '--'
    best_str = f"Mejor E1: {b1_str}  |  Mejor E2: {b2_str}"
    if hud_best.text != best_str:
        hud_best.text = best_str


def update_oscillating(ent, dt):
    """Mueve una entidad oscilante (plataforma móvil o láser) y guarda su delta."""
    old_pos = Vec3(ent.position)
    ent._phase += dt * ent.speed
    offset = sin(ent._phase) * ent.amplitude
    new_pos = Vec3(ent.origin_pos)
    if ent.axis == 'x':
        new_pos.x += offset
    elif ent.axis == 'y':
        new_pos.y += offset
    else:
        new_pos.z += offset
    ent.position = new_pos
    ent.delta = new_pos - old_pos


def player_hits_hazard(bar):
    """Comprueba solapamiento AABB entre el jugador y una barra láser."""
    return (
        abs(player.x - bar.x) < (bar.scale_x / 2 + 0.35)
        and abs(player.z - bar.z) < (bar.scale_z / 2 + 0.35)
        and (player.y + 1.8) > (bar.y - bar.scale_y / 2)
        and player.y < (bar.y + bar.scale_y / 2)
    )


# ==========================================
# 7. CICLO PRINCIPAL Y CONTROLES
# ==========================================
def update():
    dt = time.dt
    state['pad_cooldown'] = max(0.0, state['pad_cooldown'] - dt)
    state['speed_boost_timer'] = max(0.0, state['speed_boost_timer'] - dt)

    if state['banner_timer'] is not None:
        state['banner_timer'] -= dt
        if state['banner_timer'] <= 0:
            banner_text.enabled = False
            state['banner_timer'] = None

    # 1) Mover plataformas móviles y láseres
    for plat in moving_platforms:
        update_oscillating(plat, dt)
    for bar in hazards:
        update_oscillating(bar, dt)

    # 2) Actualizar ciclo de plataformas parpadeantes (5.0 s: 2.6 fija -> 1.0 aviso -> 1.4 oculta)
    for plat in blinking_platforms:
        plat._timer = (plat._timer + dt) % 5.0
        t = plat._timer
        if t < 2.6:
            plat.enabled = True
            plat.color = plat.base_color
        elif t < 3.6:
            plat.enabled = True
            plat.color = color.red if int(t * 10) % 2 == 0 else plat.base_color
        else:
            plat.enabled = False

    # 3) Velocidad (Turbo > Sprint > Normal)
    if state['speed_boost_timer'] > 0.0:
        player.speed = state['speed_boost_value']
    else:
        player.speed = 12 if held_keys['left shift'] else 8

    # 4) Cronómetro
    if not state['running'] and not state['finished']:
        if any(held_keys[k] for k in ('w', 'a', 's', 'd', 'space')):
            state['running'] = True
    if state['running'] and not state['finished']:
        state['elapsed'] += dt

    # 5) Detectar plataforma bajo los pies del jugador
    ground_ray = raycast(
        player.world_position + Vec3(0, 0.25, 0),
        Vec3(0, -1, 0),
        distance=0.55,
        ignore=[player],
    )
    if ground_ray.hit:
        entity = ground_ray.entity

        if entity in moving_platforms:
            player.position += entity.delta

        if entity in checkpoints and not entity.activated:
            entity.activated = True
            entity.color = color.green
            entity.beacon.color = color.green
            if entity.checkpoint_index > state['checkpoint_index']:
                state['checkpoint_index'] = entity.checkpoint_index
                state['respawn_pos'] = Vec3(entity.respawn_pos)
            show_banner(f"Checkpoint {entity.checkpoint_index} activado!", color.green, duration=2.0)

        if entity in jump_pads and state['pad_cooldown'] <= 0.0:
            state['pad_cooldown'] = 0.35
            if hasattr(player, 'y_animator') and player.y_animator:
                player.y_animator.pause()
            player.grounded = False
            player.air_time = 0
            player.animate_y(player.y + entity.boost, 0.55, resolution=60, curve=curve.out_expo)
            show_banner('Impulso!', color.lime, duration=0.8)

        if entity in speed_pads:
            if state['speed_boost_timer'] <= 0.1:
                show_banner('TURBO ACTIVADO!', color.turquoise, duration=1.0)
            state['speed_boost_timer'] = entity.boost_duration
            state['speed_boost_value'] = entity.speed_value

        if entity == goal_refs['platform'] and not state['finished']:
            state['finished'] = True
            state['running'] = False
            cur_stage = state['stage']
            best = state['best_times'][cur_stage]
            if best is None or state['elapsed'] < best:
                state['best_times'][cur_stage] = state['elapsed']

            if cur_stage == 1:
                show_banner(
                    f"ETAPA 1 COMPLETADA en {state['elapsed']:.2f} s! Presiona E para Etapa 2",
                    color.yellow,
                    duration=None,
                )
            else:
                show_banner(
                    f"ETAPA 2 COMPLETADA en {state['elapsed']:.2f} s! (T: Repetir | 1: Etapa 1)",
                    color.gold,
                    duration=None,
                )

    # 6) Colisión con láseres o caída al vacío
    if any(player_hits_hazard(bar) for bar in hazards):
        state['falls'] += 1
        respawn_player(to_start=False)
        show_banner('Tocaste un laser! Vuelta al checkpoint', color.red, duration=1.5)
    elif player.y < -8:
        state['falls'] += 1
        respawn_player(to_start=False)
        show_banner('Caiste! Vuelta al checkpoint', color.red, duration=1.5)

    # 7) Animación del trofeo y HUD
    if goal_refs['trophy']:
        goal_refs['trophy'].rotation_y += 60 * dt
    update_hud()


def input(key):
    if key == 'escape':
        application.quit()
    elif key == 'r':
        respawn_player(to_start=False)
        show_banner('Regresaste al checkpoint', color.orange, duration=1.2)
    elif key == 't':
        load_stage(state['stage'])
    elif key == '1':
        load_stage(1)
    elif key == '2':
        load_stage(2)
    elif key == 'e' and state['finished'] and state['stage'] == 1:
        load_stage(2)


load_stage(1)

if __name__ == '__main__':
    app.run()
