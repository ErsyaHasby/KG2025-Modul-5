"""
Blender Python Script untuk Demo Texture Types
Dapat langsung dijalankan di Blender (Scripting > Run Script)
"""

import bpy
import os

def create_pbr_material(name, textures_dict):
    """
    Membuat PBR material lengkap dengan multiple texture maps
    
    textures_dict format:
    {
        'base_color': 'path/to/color.jpg',
        'normal': 'path/to/normal.png',
        'roughness': 'path/to/roughness.jpg',
        'metallic': 'path/to/metallic.jpg'
    }
    """
    
    # Buat material baru
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Buat Principled BSDF dan Material Output
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    y_offset = 400
    
    # Base Color
    if 'base_color' in textures_dict:
        tex = nodes.new('ShaderNodeTexImage')
        tex.location = (-400, y_offset)
        tex.image = bpy.data.images.load(textures_dict['base_color'])
        tex.image.colorspace_settings.name = 'sRGB'
        links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
        y_offset -= 300
    
    # Normal Map
    if 'normal' in textures_dict:
        tex = nodes.new('ShaderNodeTexImage')
        tex.location = (-700, y_offset)
        tex.image = bpy.data.images.load(textures_dict['normal'])
        tex.image.colorspace_settings.name = 'Non-Color'
        
        normal_map = nodes.new('ShaderNodeNormalMap')
        normal_map.location = (-400, y_offset)
        
        links.new(tex.outputs['Color'], normal_map.inputs['Color'])
        links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
        y_offset -= 300
    
    # Roughness
    if 'roughness' in textures_dict:
        tex = nodes.new('ShaderNodeTexImage')
        tex.location = (-400, y_offset)
        tex.image = bpy.data.images.load(textures_dict['roughness'])
        tex.image.colorspace_settings.name = 'Non-Color'
        links.new(tex.outputs['Color'], bsdf.inputs['Roughness'])
        y_offset -= 300
    
    # Metallic
    if 'metallic' in textures_dict:
        tex = nodes.new('ShaderNodeTexImage')
        tex.location = (-400, y_offset)
        tex.image = bpy.data.images.load(textures_dict['metallic'])
        tex.image.colorspace_settings.name = 'Non-Color'
        links.new(tex.outputs['Color'], bsdf.inputs['Metallic'])
    
    print(f"🎨 PBR Material '{name}' berhasil dibuat!")
    return mat

def create_demo_objects():
    """Membuat objek-objek demo untuk testing texture"""
    
    # Hapus objek yang sudah ada (opsional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Buat Plane untuk texture demo
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = "Demo_Plane"
    
    # Tambahkan UV untuk plane
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("📦 Objek demo berhasil dibuat!")
    return plane

def create_procedural_checker_material():
    """Membuat material checker procedural untuk demo"""
    
    mat = bpy.data.materials.new(name="Procedural_Checker")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Buat nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    checker = nodes.new('ShaderNodeTexChecker')
    checker.location = (-400, 0)
    checker.inputs['Scale'].default_value = 8.0  # Jumlah tiles
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (-100, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    # Hubungkan nodes
    links.new(tex_coord.outputs['UV'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print("♟️ Procedural checker material berhasil dibuat!")
    return mat

def main():
    """Fungsi utama untuk menjalankan demo"""
    
    print("🎨 === Blender Texture Types Demo ===")
    print("1. 📦 Membuat objek demo...")
    plane = create_demo_objects()
    
    print("\n2. ♟️ Membuat procedural checker material...")
    checker_mat = create_procedural_checker_material()
    
    print("\n3. 🖼️ Membuat PBR material dengan texture maps...")
    
    # Catatan: Ganti path ini dengan path ke texture Anda
    # Untuk demo, kita akan membuat material tanpa texture files
    # karena kita tidak tahu lokasi file texture di komputer Anda
    
    # Contoh jika Anda punya texture files:
    # textures = {
    #     'base_color': 'C:/textures/wood_color.jpg',
    #     'normal': 'C:/textures/wood_normal.png',
    #     'roughness': 'C:/textures/wood_roughness.jpg',
    # }
    # wood_mat = create_pbr_material("Wood_PBR", textures)
    
    print("\n4. 🎯 Assign checker material ke objek demo...")
    if plane.data.materials:
        plane.data.materials[0] = checker_mat
    else:
        plane.data.materials.append(checker_mat)
    
    print("\n✅ === Demo selesai! ===")
    print(f"✅ Plane '{plane.name}' dibuat dengan UV unwrap")
    print(f"✅ Material '{checker_mat.name}' diterapkan dengan Checker Texture")
    checker_node = checker_mat.node_tree.nodes.get('Checker Texture')
    if checker_node:
        print(f"✅ Checker Scale: {checker_node.inputs['Scale'].default_value}")
    print("\n💡 Tips:")
    print("   - Untuk menggunakan texture files, ubah path di bagian 3")
    print("   - Pastikan texture files ada di lokasi yang ditentukan")
    print("   - Switch ke Material Preview atau Rendered mode untuk melihat hasil")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()