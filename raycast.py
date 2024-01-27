import pygame as pg
import math
from settings import *

# Physics based ray casting for camera
class RayCasting:
    def __init__(self, game):
        self.game = game
        self.cast_result = []
        self.objects_to_render = []
        self.textures = self.game.renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.cast_result):
            depth, proj_height, texture, offset = values


            if proj_height < HEIGHT:
                wall_col = self.textures[texture-1].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_col = pg.transform.scale(wall_col, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_col = self.textures[texture-1].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_col = pg.transform.scale(wall_col, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # experimental fog


            self.objects_to_render.append((depth, wall_col, wall_pos))

    def ray_cast(self):
        self.cast_result = []

        # set position for player and world
        px, py = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        tex_vert, tex_hor = 1, 1

        # set starting angle
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

  
        # shoot rays
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - py) / sin_a

            # calculate position of intersect
            x_hor = px + depth_hor * cos_a

            # determine the depth to the next y-axis grid line
            delta_depth = dy / sin_a

            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    tex_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - px) / cos_a

            # calculate position of intersect
            y_vert = py + depth_vert * sin_a

            # determine the depth to the next x-axis grid line
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    tex_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, tex_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, tex_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # calculate projection height (wall height)
            proj_height = SCREEN_DIST / (depth + 0.0001)

            if DEBUG:
                # draw rays for debug
                pg.draw.line(self.game.screen, 'yellow', (10 * px, 10 * py),
                            (10 * px + 10 * depth * cos_a, 10 * py + 10 * depth * sin_a), 2)
            else:
                # draw 1 color walls
                # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
                # pg.draw.rect(self.game.screen, color,
                #             (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
                
                # draw textured walls
                self.cast_result.append((depth, proj_height, texture, offset))

            # increase angle
            ray_angle += DELTA_ANGLE   
    
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()



# Physics ray cast for 2 vectors
def castRay_p(game, source, target, angle=0):
    # They are at same coords
    tolerance = 1
    if abs(source[0] - target[0]) < tolerance and abs(source[1] - target[1]) < tolerance:
        return True, 0, 0, source, target
      
    # calculate angle between both points (0.0001 needed to avoid division by 0.0)
    if angle == 0:
        ray_angle = math.atan2(int(target[1])-int(source[1]), int(target[0])-int(source[0])) + 0.0001
    else:
        ray_angle = angle

    sin_a = math.sin(ray_angle)
    cos_a = math.cos(ray_angle)

    wall_dist_v, wall_dist_h = 0, 0
    target_dist_v, target_dist_h = 0, 0

    # set positions for source and target
    src_x, src_y = source
    src_x_map, src_y_map = (int(source[0]), int(source[1]))

    target_x, target_y = target
    target_x_map, target_y_map = (int(target[0]), int(target[1]))
    target_map = target_x_map, target_y_map 

    # horizontals
    y_hor, dy = (src_y_map + 1, 1) if sin_a > 0 else (src_y_map - 1e-6, -1)

    depth_hor = (y_hor - src_y) / sin_a

    # calculate position of intersect
    x_hor = src_x + depth_hor * cos_a

    # determine the depth to the next y-axis grid line
    delta_depth = dy / sin_a
    dx = delta_depth * cos_a

    # wall collisions
    for i in range(MAX_DEPTH):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor == target_map:
            target_dist_h = depth_hor
            break
        if tile_hor in game.map.world_map:
            wall_dist_h = depth_hor
            break
        x_hor += dx
        y_hor += dy
        depth_hor += delta_depth


    # verticals
    x_vert, dx = (src_x_map + 1, 1) if cos_a > 0 else (src_x_map - 1e-6, -1)

    depth_vert = (x_vert - src_x) / cos_a

    # calculate position of intersect
    y_vert = src_y + depth_vert * sin_a

    # determine the depth to the next x-axis grid line
    delta_depth = dx / cos_a
    dy = delta_depth * sin_a

    # wall collisions
    for i in range(MAX_DEPTH):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert == target_map:
            target_dist_v = depth_vert
            break
        if tile_vert in game.map.world_map:
            wall_dist_v = depth_vert
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth

    target_dist = max(target_dist_v, target_dist_h)
    wall_dist = max(wall_dist_v, wall_dist_h)

    if DEBUG:
        print(f"Angle = {ray_angle}")
        print(f"TargetDist = {target_dist}")
        print(f"WallDist = {wall_dist}")

    if 0 < target_dist < wall_dist or not wall_dist:
        if DEBUG:
            pg.draw.line(game.screen, 'orange', (10 * src_x, 10 * src_y),
                (10 * target_x, 10 * target_y), 8)

        return True, target_dist, wall_dist, source, target

    return False, target_dist, wall_dist, source, target

# Physics ray cast for entities
def castRay_e(game, source, target, angle=0):
    # They are at same coords
    tolerance = 1
    if abs(source[0] - target[0]) < tolerance and abs(source[1] - target[1]) < tolerance:
        return True, 0, 0, source, target

    # calculate angle between both points (0.0001 needed to avoid division by 0.0)
    if angle == 0:
        ray_angle = math.atan2(int(target[1])-int(source[1]), int(target[0])-int(source[0])) + 0.0001
    else:
        ray_angle = angle

    # Fix order size issues
    if target > source: 
        # shoot rays
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        # swap target and source
        temp = target 
        target = source
        source = temp
    else:
        # shoot inverse rays
        sin_a = -math.sin(ray_angle)
        cos_a = -math.cos(ray_angle)


    wall_dist_v, wall_dist_h = 0, 0
    target_dist_v, target_dist_h = 0, 0

    # set positions for source and target
    src_x, src_y = source
    src_x_map, src_y_map = (int(source[0]), int(source[1]))

    target_x, target_y = target
    target_x_map, target_y_map = (int(target[0]), int(target[1]))
    target_map = target_x_map, target_y_map 

    # horizontals
    y_hor, dy = (src_y_map + 1, 1) if sin_a > 0 else (src_y_map - 1e-6, -1)

    depth_hor = (y_hor - src_y) / sin_a

    # calculate position of intersect
    x_hor = src_x + depth_hor * cos_a

    # determine the depth to the next y-axis grid line
    delta_depth = dy / sin_a
    dx = delta_depth * cos_a
    
    walls_hit = []

    # wall collisions
    for i in range(MAX_DEPTH):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor == target_map:
            target_dist_h = depth_hor
            break
        if tile_hor in game.map.world_map:
            wall_dist_h = depth_hor
            walls_hit.append(tile_hor)  # Store the coordinates of the hit wall
            break
        x_hor += dx
        y_hor += dy
        depth_hor += delta_depth


    # verticals
    x_vert, dx = (src_x_map + 1, 1) if cos_a > 0 else (src_x_map - 1e-6, -1)

    depth_vert = (x_vert - src_x) / cos_a

    # calculate position of intersect
    y_vert = src_y + depth_vert * sin_a

    # determine the depth to the next x-axis grid line
    delta_depth = dx / cos_a
    dy = delta_depth * sin_a

    # wall collisions
    for i in range(MAX_DEPTH):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert == target_map:
            target_dist_v = depth_vert
            break
        if tile_vert in game.map.world_map:
            wall_dist_v = depth_vert
            walls_hit.append(tile_vert)  # Store the coordinates of the hit wall
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth

    # print(target_dist_v, target_dist_h)
    target_dist = max(target_dist_v, target_dist_h)  # add to stop casting bug when on same tile
    wall_dist = max(wall_dist_v, wall_dist_h)
  

    if DEBUG:
        print(f"Angle = {ray_angle}")
        print(f"TargetDist = {target_dist}")
        print(f"WallDist = {wall_dist}")
        
        if wall_dist:
          [pg.draw.rect(game.screen, 'green', (pos[0] * 10, pos[1] * 10, 10, 10), 1)
            for pos in walls_hit]
            
    # print(f"Debug: target_dist = {target_dist}, wall_dist = {wall_dist}")

    # if 0 < target_dist < wall_dist or not wall_dist:
    if 0 < target_dist < wall_dist or not wall_dist:
        if DEBUG:
            pg.draw.line(game.screen, 'orange', (10 * src_x, 10 * src_y),
                (10 * target_x, 10 * target_y), 2)
            
        return True, target_dist, wall_dist, source, target

    return False, target_dist, wall_dist, source, target