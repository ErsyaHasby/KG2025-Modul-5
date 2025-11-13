"""
Blender Python Script untuk Demo Procedural Textures
Dapat langsung dijalankan di Blender (Scripting > Run Script)
"""

import bpy

def create_dirt_material(name="Dirty_Surface"):
    """
    Membuat material dengan procedural dirt/scratches
    Menggunakan Noise texture untuk variasi
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise Texture untuk dirt
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 50.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # ColorRamp untuk control dirt intensity
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    colorramp.color_ramp.elements[0].position = 0.3
    colorramp.color_ramp.elements[1].position = 0.7
    
    # Base color (clean surface)
    rgb_clean = nodes.new('ShaderNodeRGB')
    rgb_clean.location = (-400, 300)
    rgb_clean.outputs[0].default_value = (0.8, 0.8, 0.8, 1.0)  # Clean white
    
    # Dirt color
    rgb_dirt = nodes.new('ShaderNodeRGB')
    rgb_dirt.location = (-400, 150)
    rgb_dirt.outputs[0].default_value = (0.2, 0.15, 0.1, 1.0)  # Brown dirt
    
    # Mix clean and dirty colors
    mix_rgb = nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (-200, 200)
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.5
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Hubungkan semua
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], mix_rgb.inputs['Fac'])
    links.new(rgb_clean.outputs['Color'], mix_rgb.inputs['Color1'])
    links.new(rgb_dirt.outputs['Color'], mix_rgb.inputs['Color2'])
    links.new(mix_rgb.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"🟤 Procedural dirt material '{name}' berhasil dibuat!")
    return mat

def create_stone_material(name="Procedural_Stone"):
    """
    Membuat material batu menggunakan Voronoi texture
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    # Mapping untuk scale
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (5.0, 5.0, 5.0)
    
    # Voronoi untuk pola stone
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 0)
    voronoi.feature = 'F1'  # Atau 'F2', 'DISTANCE_TO_EDGE'
    voronoi.distance = 'EUCLIDEAN'
    voronoi.inputs['Scale'].default_value = 3.0
    
    # Noise untuk variasi
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -300)
    noise.inputs['Scale'].default_value = 10.0
    
    # Mix Voronoi dan Noise
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 0)
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Fac'].default_value = 1.0
    
    # ColorRamp untuk stone colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    
    # Atur warna batu (gray variations)
    colorramp.color_ramp.elements[0].color = (0.3, 0.3, 0.35, 1.0)
    colorramp.color_ramp.elements[1].color = (0.6, 0.6, 0.65, 1.0)
    
    # Bump untuk surface detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.5
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    # Hubungkan
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(voronoi.outputs['Distance'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mix.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"🪨 Procedural stone material '{name}' berhasil dibuat!")
    return mat

def create_wood_material(name="Procedural_Wood"):
    """
    Membuat material kayu menggunakan Wave texture
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Mapping untuk orientasi wood grain
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 20.0)  # Stretch di Z untuk rings
    
    # Wave Texture untuk wood rings
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-400, 0)
    wave.wave_type = 'RINGS'
    wave.rings_direction = 'Z'
    wave.wave_profile = 'SAW'
    wave.inputs['Scale'].default_value = 15.0
    wave.inputs['Distortion'].default_value = 2.0
    wave.inputs['Detail'].default_value = 5.0
    
    # ColorRamp untuk wood colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 0)
    
    # Warna kayu (light to dark brown)
    colorramp.color_ramp.elements[0].color = (0.6, 0.4, 0.2, 1.0)  # Light brown
    colorramp.color_ramp.elements[1].color = (0.3, 0.2, 0.1, 1.0)  # Dark brown
    
    # Noise untuk variasi
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, -300)
    noise.inputs['Scale'].default_value = 50.0
    noise.inputs['Detail'].default_value = 10.0
    
    # Bump untuk texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.3
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.4
    # Note: Specular removed in Blender 4.x, roughness controls appearance
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    # Hubungkan
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    links.new(wave.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"🌳 Procedural wood material '{name}' berhasil dibuat!")
    return mat

def create_rock_material(name="Procedural_Rock"):
    """
    Membuat material rock menggunakan Noise fractal
    Note: Musgrave removed in Blender 4.0, using Noise Texture instead
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Noise Texture (replacement for Musgrave in Blender 4.x)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 10.0
    noise.inputs['Roughness'].default_value = 0.5
    # Note: Blender 4.x Noise has different parameters than old Musgrave
    
    # ColorRamp untuk rock colors
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 0)
    
    # Warna rock (dark gray to light gray)
    colorramp.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1.0)
    colorramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)
    
    # Displacement untuk actual geometry displacement
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (200, -200)
    displacement.inputs['Scale'].default_value = 0.1
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.9
    
    # Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    # Hubungkan
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], displacement.inputs['Height'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
    
    print(f"🏔️ Procedural rock material '{name}' dengan displacement berhasil dibuat!")
    return mat

def create_demo_objects():
    """Membuat objek-objek demo untuk testing material"""
    
    # Hapus objek yang sudah ada (opsional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Buat beberapa objek untuk demo
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-6, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Demo_Cube"
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(-2, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Demo_Sphere"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(2, 0, 0))
    cylinder = bpy.context.active_object
    cylinder.name = "Demo_Cylinder"
    
    # Buat objek untuk displacement demo
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, y_subdivisions=20, size=4, location=(6, 0, 0))
    grid = bpy.context.active_object
    grid.name = "Demo_Grid"
    
    # Subdivide grid untuk lebih detail
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("📦 Objek demo berhasil dibuat!")
    return cube, sphere, cylinder, grid

def main():
    """Fungsi utama untuk menjalankan demo"""
    
    print("🎨 === Blender Procedural Textures Demo ===")
    print("1. 📦 Membuat objek demo...")
    cube, sphere, cylinder, grid = create_demo_objects()
    
    print("\n2. 🟤 Membuat procedural dirt material...")
    dirt_mat = create_dirt_material("Dirty_Metal")
    
    print("\n3. 🪨 Membuat procedural stone material...")
    stone_mat = create_stone_material("Procedural_Stone")
    
    print("\n4. 🌳 Membuat procedural wood material...")
    wood_mat = create_wood_material("Procedural_Wood")
    
    print("\n5. 🏔️ Membuat procedural rock material dengan displacement...")
    rock_mat = create_rock_material("Procedural_Rock")
    
    print("\n6. 🎯 Assign materials ke objek...")
    # Assign materials ke objek
    if cube.data.materials:
        cube.data.materials[0] = dirt_mat
    else:
        cube.data.materials.append(dirt_mat)
    
    if sphere.data.materials:
        sphere.data.materials[0] = stone_mat
    else:
        sphere.data.materials.append(stone_mat)
    
    if cylinder.data.materials:
        cylinder.data.materials[0] = wood_mat
    else:
        cylinder.data.materials.append(wood_mat)
    
    if grid.data.materials:
        grid.data.materials[0] = rock_mat
    else:
        grid.data.materials.append(rock_mat)
    
    print("\n✅ === Demo selesai! ===")
    print(f"✅ Cube: Dirt material (Noise + Mix RGB)")
    print(f"✅ Sphere: Stone material (Voronoi + Bump)")
    print(f"✅ Cylinder: Wood material (Wave texture)")
    print(f"✅ Grid: Rock material (Musgrave + Displacement)")
    print(f"✅ Total materials: {len(bpy.data.materials)}")
    print("\n💡 Tips:")
    print("   - Render untuk melihat hasil procedural textures")
    print("   - Coba modifikasi parameter di node untuk variasi")
    print("   - Gunakan displacement untuk detail geometri (perlu subdivide)")
    print("   - Combine berbagai procedural textures untuk hasil kompleks")
    print("   - Switch ke Material Preview/Rendered mode untuk preview")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()