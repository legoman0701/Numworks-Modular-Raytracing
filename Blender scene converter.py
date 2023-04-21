import bpy
import math
with open('Scene.txt', 'w') as file:
    for obj in bpy.context.scene.objects:
        typ = 'mesh'
        type = obj.type
        name = obj.name
        if 'sphere' in name:typ = 'sphere'
        elif 'plane' in name:typ = 'plane'
        if type == "MESH" and typ == "mesh":
            mesh = obj.data
            # Get the triangles of the mesh
            triangles = []
            for poly in mesh.polygons:
                print(len(poly.vertices))
                if len(poly.vertices) == 3:
                    triangle = []
                    for i in range(3):
                        vertex_index = poly.vertices[i]
                        vertex = mesh.vertices[vertex_index]
                        position = vertex.co
                        rounded_list = []

                        # Loop through each element in the tuple and round it to 2 decimal places
                        for num in position:
                            rounded_num = round(num, 2)
                            rounded_list.append(rounded_num)

                        triangle.append(tuple(rounded_list))
                    normal = poly.normal

                    rounded_list = []

                    # Loop through each element in the tuple and round it to 2 decimal places
                    for num in normal:
                        rounded_num = round(num, 2)
                        rounded_list.append(rounded_num)

                    triangle.append(tuple(rounded_list))
                    triangles.append(triangle)

            # Print the triangles

            num_rows = len(triangles)

            # Define the number of lines to skip
            y = 2
            file.write(f"{name} = [")
            # Loop through each row in the list
            for i in range(num_rows):
                # Print the elements in the row
                file.write(str(triangles[i]))
                file.write(",\n")
                
            file.write("]\n")

    # Get the objects
    file.write("objects = [\n")
    for obj in bpy.context.scene.objects:
        name = obj.name
        typ = 'mesh'
        if 'sphere' in name:typ = 'sphere'
        elif 'plane' in name:typ = 'plane'
        type = obj.type
        # Get the mesh of the object
        if type == "MESH":
            print(obj.name)
            bpy.ops.object.transform_apply(rotation=True, location=False, scale=True)
            mesh = obj.data

            # Get the first material slot of the object
            material_slot = obj.material_slots[0]

            # Get the material applied to the material slot
            material = material_slot.material

            color = material.node_tree.nodes["Principled BSDF"].inputs[0].default_value
            metallic = material.node_tree.nodes["Principled BSDF"].inputs[6].default_value
            specular = material.node_tree.nodes["Principled BSDF"].inputs[7].default_value
            roughness = material.node_tree.nodes["Principled BSDF"].inputs[9].default_value
            emmisiveColor = material.node_tree.nodes["Principled BSDF"].inputs[19].default_value
            emmisiveStrenght = material.node_tree.nodes["Principled BSDF"].inputs[20].default_value
            emmisiveColor = tuple(emmisiveColor)
            emmisiveColor = (emmisiveColor[0], emmisiveColor[1], emmisiveColor[2])
            color = tuple(color)
            color = (color[0], color[1], color[2])
            file.write("    {\n")
            file.write(f"        'type': '{typ}',\n")
            if typ == 'mesh':
                file.write(f"        'mesh': {name},\n")
            file.write(f"        'position': {tuple(obj.location)},\n")
            if typ == 'plane':
                file.write(f"        'normal': {tuple(mesh.vertices[0].normal)},\n")
            print(tuple(mesh.vertices[0].normal))
            if typ == 'sphere':
                file.write(f"        'radius': {float(obj.dimensions[0]/2)},\n")
            file.write(f"        'color': {color},\n")
            file.write(f"        'metallic': {float(metallic)},\n")
            file.write(f"        'roughness': {float(roughness)},\n")
            file.write(f"        'specular': {float(specular)},\n")
            file.write(f"        'emmisiveColor': {emmisiveColor},\n")
            file.write(f"        'emmisiveStrenght': {float(emmisiveStrenght)}\n")
            file.write("    },\n")
                
    file.write("]\n\n")
    file.write("lights = [\n")
    # Get the lights
    for obj in bpy.context.scene.objects:
        type = obj.type
        # Get the mesh of the object
        if type == "LIGHT":
            # Get the radius of the light
            radius = obj.data.shadow_soft_size

            # Get the emissive color of the light
            emissive_color = obj.data.color

            # Get the emissive strength of the light
            emissive_strength = obj.data.energy

            emmisiveColor = tuple(emissive_color)
            emmisiveColor = (emmisiveColor[0], emmisiveColor[1], emmisiveColor[2])
        
            file.write("    {\n")
            file.write(f"        'position': {tuple(obj.location)},\n")
            file.write(f"        'radius': {float(radius)},\n")
            file.write(f"        'emmisiveColor': {emmisiveColor},\n")
            file.write(f"        'emmisiveStrenght': {float(emissive_strength)/25}\n")
            file.write("    },\n")

    file.write("]\n\n")
    file.write("camera = {\n")
    # Get the lights
    for obj in bpy.context.scene.objects:
        print(obj)
        type = obj.type
        print(type)
        # Get the mesh of the object
        if type == "CAMERA":
            # Get the radius of the light
            far_plane = obj.data.clip_end
            focus = obj.data.dof.focus_distance
            fov = obj.data.angle
            rotation = tuple(obj.rotation_euler)
            
            file.write(f"    'position': {tuple(obj.location)},\n")
            file.write(f"    'rotation': (math.radians({math.degrees(rotation[0])}), math.radians({math.degrees(rotation[1])}), math.radians({math.degrees(rotation[2])})),\n")
            file.write(f"    'focus': {float(focus)},\n")
            file.write(f"    'far_plane': {float(far_plane)},\n")
            file.write(f"    'fov': math.radians({float(math.degrees(fov)*0.707109990959094)})\n")

            file.write("}\n")

