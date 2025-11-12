"""
Blender Python Script untuk Demo Shader Editor & Node System
Dapat langsung dijalankan di Blender (Scripting > Run Script)
"""

import bpy

def create_basic_node_setup(mat_name):
    """Membuat material dengan node setup dasar"""
    
    # Buat material
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Buat Texture Coordinate node
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Buat Mapping node (untuk scale, rotate, translate)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    
    # Buat Image Texture node
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (-400, 0)
    
    # Buat Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Buat Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Hubungkan nodes
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"🎨 Material '{mat_name}' dengan node setup berhasil dibuat!")
    return mat

def add_colorramp_gradient(material):
    """
    Menambahkan ColorRamp untuk membuat gradient effect
    Berguna untuk masking atau color variation
    """
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Cari Principled BSDF
    bsdf = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf = node
            break
    
    if not bsdf:
        print("Principled BSDF tidak ditemukan!")
        return
    
    # Buat Texture Coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, -300)
    
    # Buat Separate XYZ (untuk mendapatkan Z coordinate)
    separate = nodes.new('ShaderNodeSeparateXYZ')
    separate.location = (-400, -300)
    
    # Buat ColorRamp
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, -300)
    
    # Atur ColorRamp (gradient dari merah ke biru)
    colorramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    colorramp.color_ramp.elements[1].color = (0.0, 0.0, 1.0, 1.0)  # Blue
    
    # Hubungkan
    links.new(tex_coord.outputs['Object'], separate.inputs['Vector'])
    links.new(separate.outputs['Z'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    print("🌈 ColorRamp gradient berhasil ditambahkan!")
    return True

def mix_two_textures(mat_name, mix_factor=0.5):
    """
    Membuat material yang me-mix dua texture
    Berguna untuk blending materials
    """
    
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture 1
    tex1 = nodes.new('ShaderNodeTexImage')
    tex1.location = (-600, 300)
    
    # Texture 2
    tex2 = nodes.new('ShaderNodeTexImage')
    tex2.location = (-600, 0)
    
    # Mix RGB node
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-300, 150)
    mix.blend_type = 'MIX'  # Bisa juga: 'ADD', 'MULTIPLY', 'OVERLAY', dll
    mix.inputs['Fac'].default_value = mix_factor
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Hubungkan
    links.new(tex1.outputs['Color'], mix.inputs['Color1'])
    links.new(tex2.outputs['Color'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print(f"🎭 Mixed texture material '{mat_name}' berhasil dibuat!")
    return mat

def create_glass_material(name="Glass", color=(0.8, 0.9, 1.0, 1.0), ior=1.45):
    """
    Membuat realistic glass material
    IOR values: Air=1.0, Water=1.33, Glass=1.45, Diamond=2.42
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Principled BSDF dengan glass settings
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Set glass properties
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.0  # Smooth glass
    bsdf.inputs['IOR'].default_value = ior
    # Note: Blender 4.x uses 'Transmission Weight' instead of 'Transmission'
    transmission_input = 'Transmission Weight' if 'Transmission Weight' in bsdf.inputs else 'Transmission'
    bsdf.inputs[transmission_input].default_value = 1.0  # Fully transparent
    
    # Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # IMPORTANT: Enable blend mode untuk transparency
    mat.blend_method = 'BLEND'
    # Note: shadow_method removed in Blender 4.x, using transparent shadow instead
    if hasattr(mat, 'shadow_method'):
        mat.shadow_method = 'HASHED'
    else:
        mat.use_transparent_shadow = True
    
    print(f"🔮 Glass material '{name}' berhasil dibuat!")
    return mat

def create_emission_material(name="Emission", color=(1.0, 0.5, 0.0, 1.0), strength=10.0):
    """
    Membuat emission material (glowing/light-emitting)
    Berguna untuk neon signs, screens, lights
    """
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Emission shader
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Color'].default_value = color
    emission.inputs['Strength'].default_value = strength
    
    # Material Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    print(f"💡 Emission material '{name}' berhasil dibuat!")
    return mat

def create_node_group_uv_scale(group_name="UV_Scale"):
    """
    Membuat node group untuk UV scaling yang dapat digunakan kembali
    """
    
    # Buat node group baru
    group = bpy.data.node_groups.new(name=group_name, type='ShaderNodeTree')
    
    # Buat input dan output untuk group
    group_inputs = group.nodes.new('NodeGroupInput')
    group_inputs.location = (-400, 0)
    
    group_outputs = group.nodes.new('NodeGroupOutput')
    group_outputs.location = (400, 0)
    
    # Define inputs - use interface for Blender 4.x, inputs for 3.x
    if hasattr(group, 'interface'):
        # Blender 4.x
        group.interface.new_socket('UV', in_out='INPUT', socket_type='NodeSocketVector')
        group.interface.new_socket('Scale', in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket('UV', in_out='OUTPUT', socket_type='NodeSocketVector')
    else:
        # Blender 3.x
        group.inputs.new('NodeSocketVector', 'UV')
        group.inputs.new('NodeSocketFloat', 'Scale')
        group.outputs.new('NodeSocketVector', 'UV')
    
    # Buat node di dalam group
    mapping = group.nodes.new('ShaderNodeMapping')
    mapping.location = (0, 0)
    
    # Hubungkan
    group.links.new(group_inputs.outputs['UV'], mapping.inputs['Vector'])
    group.links.new(group_inputs.outputs['Scale'], mapping.inputs['Scale'])
    group.links.new(mapping.outputs['Vector'], group_outputs.inputs['UV'])
    
    print(f"🔧 Node Group '{group_name}' berhasil dibuat!")
    return group

def use_node_group(material, group_name):
    """Menggunakan node group dalam material"""
    
    nodes = material.node_tree.nodes
    
    # Tambahkan node group ke material
    group_node = nodes.new('ShaderNodeGroup')
    group_node.node_tree = bpy.data.node_groups[group_name]
    group_node.location = (-400, 0)
    
    print(f"📦 Node Group '{group_name}' ditambahkan ke material")
    return group_node

def create_demo_objects():
    """Membuat objek-objek demo untuk testing material"""
    
    # Hapus objek yang sudah ada (opsional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Buat beberapa objek untuk demo
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-4, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Demo_Cube"
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Demo_Sphere"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(4, 0, 0))
    cylinder = bpy.context.active_object
    cylinder.name = "Demo_Cylinder"
    
    print("📦 Objek demo berhasil dibuat!")
    return cube, sphere, cylinder

def main():
    """Fungsi utama untuk menjalankan demo"""
    
    print("🎨 === Blender Shader Editor Demo ===")
    print("1. 📦 Membuat objek demo...")
    cube, sphere, cylinder = create_demo_objects()
    
    print("\n2. 🎨 Membuat material dengan node setup dasar...")
    basic_mat = create_basic_node_setup("Basic_Node_Material")
    
    print("\n3. 🌈 Membuat material dengan gradient...")
    gradient_mat = bpy.data.materials.new("Gradient_Material")
    gradient_mat.use_nodes = True
    add_colorramp_gradient(gradient_mat)
    
    print("\n4. 🎭 Membuat material dengan mix textures...")
    mixed = mix_two_textures("Mixed_Material", mix_factor=0.5)
    
    print("\n5. 🔮 Membuat glass material...")
    glass = create_glass_material("Glass_Material")
    
    print("\n6. 💡 Membuat emission material...")
    emission = create_emission_material("Emission_Material")
    
    print("\n7. 🔧 Membuat node group...")
    uv_scale_group = create_node_group_uv_scale("UV_Scale_Group")
    
    print("\n8. 📦 Menggunakan node group...")
    group_mat = bpy.data.materials.new("Group_Material")
    group_mat.use_nodes = True
    use_node_group(group_mat, "UV_Scale_Group")
    
    print("\n9. 🎯 Assign materials ke objek...")
    # Assign materials ke objek
    if cube.data.materials:
        cube.data.materials[0] = basic_mat
    else:
        cube.data.materials.append(basic_mat)
    
    if sphere.data.materials:
        sphere.data.materials[0] = glass
    else:
        sphere.data.materials.append(glass)
    
    if cylinder.data.materials:
        cylinder.data.materials[0] = emission
    else:
        cylinder.data.materials.append(emission)
    
    print("\n✅ === Demo selesai! ===")
    print(f"✅ Cube: Material '{basic_mat.name}' dengan {len(basic_mat.node_tree.nodes)} nodes")
    print(f"✅ Sphere: Glass material dengan transmission")
    print(f"✅ Cylinder: Emission material (glowing)")
    print(f"✅ Total materials: {len(bpy.data.materials)}")
    print(f"✅ Node groups: {len(bpy.data.node_groups)}")
    print("\n💡 Tips:")
    print("   - Buka Shader Editor untuk melihat node setup")
    print("   - Coba modifikasi node dan lihat perubahan material")
    print("   - Gunakan node groups untuk setup yang kompleks")
    print("   - Switch ke Material Preview/Rendered mode untuk melihat hasil")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()