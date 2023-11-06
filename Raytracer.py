
"""
Credit:
Huge thanks to Sebastian Lague
https://www.youtube.com/watch?v=Qz0KTGYJtUk&t=1418s

to cs.princeton.edu
https://www.cs.princeton.edu/courses/archive/fall00/cs426/lectures/raycast/sld017.htm

to antonako and idmean
https://stackoverflow.com/a/6178290

and to Ray Tracing in One Weekend
https://raytracing.github.io

"""


from kandinsky import *
import math
import random
import time

def add_vectors(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def sub_vectors(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def multiply_vector(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)

def multiply_vectors(a, b):
    return (a[0] * b[0], a[1] * b[1], a[2] * b[2])

def normalize_vector(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if length == 0: return v
    return (v[0] / length, v[1] / length, v[2] / length)

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def reflect_vector(vector, normal):
    return sub_vectors(vector, multiply_vector(normal, 2 * dot_product(vector, normal)))

def cross_vectors(u, v):
    x = u[1] * v[2] - u[2] * v[1]
    y = u[2] * v[0] - u[0] * v[2]
    z = u[0] * v[1] - u[1] * v[0]
    return (x, y, z)

def euler_to_matrix(x, y, z):
    sy = math.sin(y)
    cy = math.cos(y)
    sp = math.sin(x)
    cp = math.cos(x)
    sr = math.sin(z)
    cr = math.cos(z)

    # Calculate the rotation matrix
    R = [[cy*cr + sy*sp*sr, -cy*sr + sy*sp*cr, sy*cp],
        [sr*cp, cr*cp, -sp],
        [-sy*cr + cy*sp*sr, sy*sr + cy*sp*cr, cy*cp]]

    return R

def random_dir():
    while True:
        x = random_value_normal_distribution()
        y = random_value_normal_distribution()
        z = random_value_normal_distribution()
        pointInCube = (x, y, z)
        sqrDistFromCenter = dot_product(pointInCube, pointInCube)
        if sqrDistFromCenter <= 1:
            return multiply_vector(pointInCube, 1 / math.sqrt(sqrDistFromCenter))
        
def pos_sphere(radius):
    while True:
        x = random_value_normal_distribution()
        y = random_value_normal_distribution()
        z = random_value_normal_distribution()
        pointInCube = (x, y, z)
        sqrDistFromCenter = dot_product(pointInCube, pointInCube)
        if sqrDistFromCenter <= 1:
            return multiply_vector(pointInCube, radius)

def random_he_dir(normal):
    dir = random_dir()
    dot_dir = dot_product(normal, dir)
    if dot_dir < 0:
        dir = multiply_vector(dir, -1)
    return dir

def random_value_normal_distribution():
    # Thanks to https://stackoverflow.com/a/6178290
    theta = 23.1415926 * random.random()
    rho = math.sqrt(-2 * math.log(random.random()))
    return (rho * math.cos(theta))/3

def create_ray(x, y):
    planeHeight = camera['focus'] * math.tan(camera['fov'] * 0.5)*2
    planeWidth = planeHeight * (WIDTH/HEIGHT)
    bottomLeftLocal = (-planeWidth / 2, -planeHeight / 2, camera['focus'])
    tx = x / (WIDTH - 1)
    ty = y / (HEIGHT - 1)

    pointLocal = add_vectors(bottomLeftLocal, (planeWidth * tx, planeHeight * ty, 0))

    R = euler_to_matrix(camera['rotation'][0], camera['rotation'][1], camera['rotation'][2])

    # Define camera right, up, and forward vectors
    cam_right = [R[0][0], R[1][0], R[2][0]]
    cam_up = [R[0][1], R[1][1], R[2][1]]
    cam_forward = [-R[0][2], -R[1][2], -R[2][2]]

    point = add_vectors(camera['position'], add_vectors(multiply_vector(cam_right, pointLocal[0]), add_vectors(multiply_vector(cam_up, pointLocal[1]), multiply_vector(cam_forward, pointLocal[2]))))
    dir = normalize_vector(sub_vectors(point, camera['position']))
    return point, dir

def colide_ray(point, dir, objects):
    closest_hit, closest_dis, closest_pos, closest_normal, closest_obj = False, 1000, (0, 0, 0), (0, 0, 0), None
    colide_bbox = 0
    for object in objects:
        if object['type'] == 'sphere':
            hit, dis, pos, normal = intersect_sphere(point, dir, object)
        elif object['type'] == 'plane':
            hit, dis, pos, normal = intersect_plane(point, dir, object)
        elif object['type'] == 'mesh':
            hit, dis, pos, normal = intersect_mesh(point, dir, object, colide_bbox)
            colide_bbox += 1
        if dis < closest_dis:
            closest_hit, closest_dis, closest_pos, closest_normal, closest_obj = hit, dis, pos, normal, object

    return closest_hit, closest_dis, closest_pos, closest_normal, closest_obj

def lerp(diffuse, reflect, mix):
    return add_vectors(multiply_vector(reflect, 1-mix), multiply_vector(diffuse, mix))

def calculate_color(point, dir, objects):
    point = camera['position']
    rayColor = (1, 1, 1)
    incoLight = (0, 0, 0)
    emittedLight = (0, 0, 0)
    hit_var = 0
    emittedLight = (0, 0, 0)
    emittedLightstr = 1
    objectColor = (0, 0, 0)
    AO_Str = 1
    for d in range(DEPTH):
        hit, dis, pos, normal, object = colide_ray(point, dir, objects)
        hit_var += hit*1
        if hit:
            emittedLight = multiply_vector(object['emmisiveColor'], object['emmisiveStrenght'])
            isSpecBounce = 1-object['specular'] >= random.random()
            shadow_point = pos
            AO_point = pos
            for light in lights:
                shadow_dir = normalize_vector(sub_vectors(add_vectors(light['position'], pos_sphere(light['radius'])), shadow_point))
                shadow_hit, shadow_dis, shadow_pos, shadow_normal, shadow_object = colide_ray(shadow_point, shadow_dir, objects)
                if shadow_hit:
                    emittedLight = add_vectors((0, 0, 0), emittedLight)
                else:
                    emittedLight = add_vectors(multiply_vector(light['emmisiveColor'], light['emmisiveStrenght']), emittedLight)
                    light_distance = math.sqrt((light['position'][0] - shadow_point[0]) ** 2 +
                                                (light['position'][1] - shadow_point[1]) ** 2 +
                                                (light['position'][2] - shadow_point[2]) ** 2)
                    light_falloff = (1 / (light_distance)**2)
                    emittedLightstr = light_falloff
                    emittedLightstr *= dot_product(normal, shadow_dir)           
                    emittedLight = multiply_vector(emittedLight, emittedLightstr)
        
            objectColor = object['color']
            rayColor = multiply_vectors(rayColor, lerp(objectColor, (1, 1, 1), isSpecBounce))
            incoLight = add_vectors(multiply_vector(multiply_vectors(emittedLight, rayColor), 1-object['metallic']), incoLight)
        else:
            incoLight = add_vectors(incoLight, BACKGROUND)
            break

        reflect_dir = reflect_vector(dir, normal)
        diffuse_dir = normalize_vector(add_vectors(normal, random_he_dir(normal)))
        mix = max(object['roughness'], 1-object['metallic'])
        dir = lerp(diffuse_dir, reflect_dir, mix*(isSpecBounce))
        point = pos
        
    return hit_var, incoLight

def intersect_sphere(point, dir, sphere):
    center = sphere['position']
    radius = sphere['radius']

    oc = sub_vectors(point, center)
    a = dot_product(dir, dir)
    b = 2 * dot_product(oc, dir)
    c = dot_product(oc, oc) - radius ** 2
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)

    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    if t1 < EPSILON and t2 < EPSILON:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)

    if t1 > camera['far_plane'] and t2 > camera['far_plane']:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)

    dist = min(t1, t2)
    pos = []
    for i in range(3):
        pos.append(point[i] + dist * dir[i])
    pos = tuple(pos)
    normal = normalize_vector(sub_vectors(pos, center))
    return True, dist, pos, normal

def intersect_plane(point, dir, plane):
    normal = plane['normal']

    denominator = dot_product(normal, dir)

    if abs(denominator) < 0:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)

    t = dot_product(normal, sub_vectors(plane['position'], point)) / denominator
    
    if t < EPSILON or t > camera['far_plane']:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)

    pos = add_vectors(point, multiply_vector(dir, t))

    return True, t, pos, normal

def intersect_mesh(point, dir, object, colide_bbox):
    bboxma, bboxmi = bboxs[colide_bbox]

    if ray_bbox_intersect(point, dir, [bboxma, bboxmi]) == False:
        return False, float('inf'), (0, 0, 0), (0, 0, 0)
    # Initialize the closest hit distance and intersection point
    closest_hit_dist = float('inf')
    closest_hit_pos = None
    closest_hit_normal = None

    mesh = object['mesh']
    # Iterate over the triangles of the mesh
    for triangle in mesh:
        a, b, c, normal = triangle

        a = add_vectors(a, object['position'])
        b = add_vectors(b, object['position'])
        c = add_vectors(c, object['position'])
    
        edgeAB = sub_vectors(b, a)
        edgeAC = sub_vectors(c, a)
        normal_v = cross_vectors(edgeAB, edgeAC)
        ao = sub_vectors(point, a)
        dao = cross_vectors(ao, dir)

        determinant = -dot_product(dir, normal_v)
        if determinant < EPSILON:
            continue
        invDet = 1.0 / determinant

        t = dot_product(ao, normal_v) * invDet
        if t > closest_hit_dist:
            continue
        u = dot_product(edgeAC, dao) * invDet
        v = -dot_product(edgeAB, dao) * invDet
        w = 1 - u - v

        if u <= 0 or v <= 0 or w <= 0:
            continue

        # find out where is the intersection point
        intersection_point = add_vectors(point, multiply_vector(dir, t))

        if t > EPSILON and t <= closest_hit_dist: # ray intersection
            closest_hit_dist = t
            closest_hit_pos = intersection_point
            closest_hit_normal = normal

    if closest_hit_dist == float('inf'):
        return False, float('inf'), (0, 0, 0), (0, 0, 0)
    return True, closest_hit_dist, closest_hit_pos, closest_hit_normal

def ray_bbox_intersect(point, dir, bbox):
    box_max, box_min = bbox

    # Calculate the intersection points of the ray with the six planes that define the box
    t_near = float('-inf')
    t_far = float('inf')
    for i in range(3):
        if abs(dir[i]) < 1e-6:
            if point[i] < box_min[i] or point[i] > box_max[i]:
                return False
        else:
            t1 = (box_min[i] - point[i]) / dir[i]
            t2 = (box_max[i] - point[i]) / dir[i]
            t_near = max(t_near, min(t1, t2))
            t_far = min(t_far, max(t1, t2))

    # Check if any of the intersection points are inside the box
    if t_near > t_far or t_far < 0:
        return False
    intersection_point =  add_vectors(point, multiply_vector(dir, t_near))
    if intersection_point[0] < box_min[0] or intersection_point[0] > box_max[0]:
        return False
    if intersection_point[1] < box_min[1] or intersection_point[1] > box_max[1]:
        return False
    if intersection_point[2] < box_min[2] or intersection_point[2] > box_max[2]:
        return False

    return True

def denoise():
    for y in range(HEIGHT):
          for x in range(WIDTH):
            total = [0, 0, 0]
            count = 0
            for dy in range(-1, 1):
                for dx in range(-1, 1):
                    nx = x + dx
                    ny = y + dy
                    if nx >= 0 and nx < WIDTH and ny >= 0 and ny < HEIGHT:
                        color = get_pixel(nx, ny)
                        total[0] += color[0]
                        total[1] += color[1]
                        total[2] += color[2]
                        count += 1
            average = [int(t / count) for t in total]
            set_pixel(x, y, tuple(average))

def tone_map_color(color):
    r, g, b = color
    def gamma_correct(c):
        if c <= 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * pow(c, 1/2.4) - 0.055

    r = gamma_correct(r)
    g = gamma_correct(g)
    b = gamma_correct(b)
    if r > 1:
        g = g + (r - 1)/10
        b = b + (r - 1)/10
        r = 1
    if g > 1:
        r = r + (g - 1)/10
        b = b + (g - 1)/10
        g = 1
    if b > 1:
        r = r + (b - 1)/10
        g = g + (b - 1)/10
        b = 1
    r = min(r, 1)
    g = min(g, 1)
    tone_mapped = (r, g, b)
    return tone_mapped

#The scene need to be pasted between here
objects = [
    {
        'type': 'sphere',
        'position': (0, 0, -7),
        'radius': 1,
        'color': (0, 1, 0),
        'metallic': 0,
        'roughness': 1,
        'specular': 0,
        'emmisiveColor': (1, 1, 1),
        'emmisiveStrenght': 0
    },
    {
        'type': 'plane',
        'position': (0, -1, 0),
        'normal': (0, 1, 0),
        'size': 5,
        'color': (1, 1, 1),
        'metallic': 0,
        'roughness': 1,
        'specular': 0,
        'emmisiveColor': (1, 1, 1),
        'emmisiveStrenght': 0
    }
]

lights = [
    {
        'position': (0.0, 5, -3.4510927200317383),
        'radius': 0.10000000149011612,
        'emmisiveColor': (1.0, 1.0, 1.0),
        'emmisiveStrenght': 10.0
    },
]

camera = {
    'position': (0.0, 0.0, 0.0),
    'rotation': (math.radians(0.0), math.radians(0.0), math.radians(0.0)),
    'focus': 10.0,
    'far_plane': 100.0,
    'fov': math.radians(27.999968417477657)
}
#and there

bboxs =[]
for object in objects:
    if not object['type'] == 'mesh':continue
    mesh = object['mesh']
    bboxma = [float('-inf'), float('-inf'), float('-inf')]
    bboxmi = [float('inf'), float('inf'), float('inf')]
    for triangle in mesh:
        a, b, c, normal = triangle

        a = add_vectors(a, object['position'])
        b = add_vectors(b, object['position'])
        c = add_vectors(c, object['position'])

        for i in range(3):
            bboxma[i] = max(a[i]+0.01, bboxma[i])
            bboxma[i] = max(b[i]+0.01, bboxma[i])
            bboxma[i] = max(c[i]+0.01, bboxma[i])
            bboxmi[i] = min(a[i]-0.01, bboxmi[i])
            bboxmi[i] = min(b[i]-0.01, bboxmi[i])
            bboxmi[i] = min(c[i]-0.01, bboxmi[i])
    bboxs.append([bboxma, bboxmi])

print(bboxs)
HEIGHT = 222
WIDTH = 320
SIZE = 1
DEPTH = 10
SAMPLE = 30
EPSILON = 0.0001
BACKGROUND = (0.05, 0.05, 0.05)

dT = 0
start = time.time()
fill_rect(0, 0, 320, 222, (0, 0, 0))
for y in range(0, HEIGHT, SIZE):
    debut = time.time()
    Trm, Trs = divmod((222-y)*dT, 60)
    print(round((y/222)*100),"%", int(Trm), "m", int(Trs), "s")
    for x in range(0, WIDTH, SIZE):
        color = (0, 0, 0)
        hit_var = 0
        for s in range(SAMPLE):
            point, dir = create_ray(x, y*-1+222)
            hit, color_raw = calculate_color(point, dir, objects)
            #color_raw = multiply_vector(add_vectors(color_raw, (1, 1, 1)), 0.5)
            hit_var += hit
            color = add_vectors(color_raw, color)
            if hit_var == 0 and s == 10:
                color = multiply_vector(BACKGROUND, SAMPLE)
                break

        color = multiply_vector(color, 1/(SAMPLE))
        #color = multiply_vector(color, 2)
        color = tone_map_color(color)
        fill_rect(x, y, SIZE, SIZE,  multiply_vector(color, 255))
    dT = time.time()-debut

dur = time.time() - start
Trm, Trs = divmod(dur, 60)
print(f"Render finished {int(Trm)}m {int(Trs)}s")
start = time.time()
denoise() # Dose not work with beta of the kandinsky module
dur = time.time() - start
Trm, Trs = divmod(dur, 60)
print(f"Denoise finished {int(Trm)}m {int(Trs)}s")
#while True:{}
