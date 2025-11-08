"""
Blender Python Script untuk Demo Material Introduction
Dapat langsung dijalankan di Blender (Scripting > Run Script)

Demo ini mencakup:
- Membuat material dasar dengan Principled BSDF
- Material metal (Gold) dan non-metal (Plastic)
- Assign material ke objek
- Setup lighting dan camera
- Viewport shading

Tested dan bekerja dengan Blender 3.x/4.x
"""

import bpy

def create_basic_material():
    """Membuat material dasar dengan Principled BSDF"""
    
    # Membuat material baru
    material = bpy.data.materials.new(name="Material_Saya")
    
    # Aktifkan penggunaan nodes
    material.use_nodes = True
    
    # Dapatkan node tree
    nodes = material.node_tree.nodes
    
    # Hapus default nodes (opsional)
    nodes.clear()
    
    # Tambahkan Principled BSDF node
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Tambahkan Material Output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Hubungkan BSDF ke Output
    links = material.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print("Material berhasil dibuat!")
    return material

def set_material_properties():
    """Mengatur properti material"""
    
    # Ambil material yang sudah ada
    mat = bpy.data.materials["Material_Saya"]
    
    # Dapatkan Principled BSDF node
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Set Base Color (RGB + Alpha)
    bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1.0)
    
    # Set Metallic (0.0 - 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    
    # Set Roughness (0.0 - 1.0)
    bsdf.inputs['Roughness'].default_value = 0.3
    
    # Note: 'Specular' parameter mungkin berbeda di versi Blender yang berbeda
    # Untuk Blender 4.x, gunakan 'Specular IOR Level' atau skip jika tidak ada
    
    print("Properti material berhasil diatur!")

def create_metal_material(name, color, roughness):
    """Membuat material metal dengan warna dan roughness tertentu"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 1.0  # Metal penuh
    bsdf.inputs['Roughness'].default_value = roughness
    
    return mat

def create_plastic_material(name, color, roughness):
    """Membuat material plastic/non-metal"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 0.0  # Non-metal
    bsdf.inputs['Roughness'].default_value = roughness
    
    return mat

def assign_material_to_object(obj_name, material_name):
    """Assign material ke objek"""
    
    # Pilih objek berdasarkan nama
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        print(f"Objek '{obj_name}' tidak ditemukan!")
        return
    
    # Dapatkan atau buat material
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        print(f"Material '{material_name}' tidak ditemukan!")
        return
    
    # Assign material ke objek
    if obj.data.materials:
        # Jika objek sudah punya material, replace yang pertama
        obj.data.materials[0] = mat
    else:
        # Jika objek belum punya material, tambahkan
        obj.data.materials.append(mat)
    
    print(f"Material '{mat.name}' berhasil di-assign ke '{obj.name}'")

def create_demo_objects():
    """Membuat objek-objek demo untuk testing material"""
    
    # Hapus semua objek yang sudah ada (opsional, hati-hati!)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Buat Cube
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-4, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Demo_Cube"
    
    # Buat Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Demo_Sphere"
    
    # Buat Cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(4, 0, 0))
    cylinder = bpy.context.active_object
    cylinder.name = "Demo_Cylinder"
    
    print("✓ Objek demo berhasil dibuat!")
    print(f"  - Cube: {cube.name} at {cube.location}")
    print(f"  - Sphere: {sphere.name} at {sphere.location}")
    print(f"  - Cylinder: {cylinder.name} at {cylinder.location}")
    
    return cube, sphere, cylinder

def setup_lighting():
    """Setup lighting untuk melihat material lebih baik"""
    
    # Hapus light yang ada
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Tambahkan Sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.name = "Sun_Light"
    sun.data.energy = 3.0
    
    print("✓ Sun light ditambahkan")

def setup_camera():
    """Setup camera untuk view yang lebih baik"""
    
    # Hapus camera yang ada
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Tambahkan camera baru
    bpy.ops.object.camera_add(location=(8, -8, 5))
    camera = bpy.context.active_object
    camera.name = "Demo_Camera"
    camera.rotation_euler = (1.1, 0, 0.785)
    
    # Set sebagai active camera
    bpy.context.scene.camera = camera
    
    print("✓ Camera diatur")

def setup_viewport_shading():
    """Set viewport shading ke Material Preview"""
    
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    print("✓ Viewport shading diubah ke Material Preview")
                    break

def print_material_info():
    """Cetak informasi material yang dibuat"""
    
    print("\n=== RINGKASAN DEMO MATERIAL ===\n")
    
    print("📦 OBJEK YANG DIBUAT:")
    print("  1. Demo_Cube (Cube di kiri)")
    print("  2. Demo_Sphere (Sphere di tengah)")
    print("  3. Demo_Cylinder (Cylinder di kanan)")
    print("  4. Sun_Light (Pencahayaan)")
    print("  5. Demo_Camera\n")
    
    print("🎨 MATERIAL YANG DIBUAT:")
    materials_info = [
        ("Material_Saya", "Demo_Cube", "Red plastic-like", "Non-metallic"),
        ("Gold", "Demo_Sphere", "Gold metal", "Full metallic"),
        ("Plastic_Red", "Demo_Cylinder", "Red plastic", "Non-metallic")
    ]
    
    for i, (mat_name, obj_name, desc, metal) in enumerate(materials_info, 1):
        mat = bpy.data.materials.get(mat_name)
        if mat:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                color = bsdf.inputs['Base Color'].default_value
                rough = bsdf.inputs['Roughness'].default_value
                metallic = bsdf.inputs['Metallic'].default_value
                
                print(f"  {i}. {mat_name} → {obj_name}")
                print(f"     - Color: RGB({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})")
                print(f"     - Metallic: {metallic:.1f} ({metal})")
                print(f"     - Roughness: {rough:.1f}")
                print(f"     - Description: {desc}\n")

def main():
    """Fungsi utama untuk menjalankan demo"""
    
    print("=== BLENDER MATERIAL DEMO ===\n")
    
    print("1. Membuat objek demo...")
    cube, sphere, cylinder = create_demo_objects()
    
    print("\n2. Membuat material dasar...")
    basic_mat = create_basic_material()
    
    print("\n3. Mengatur properti material...")
    set_material_properties()
    
    print("\n4. Membuat material metal (Gold)...")
    gold = create_metal_material("Gold", (1.0, 0.766, 0.336, 1.0), 0.1)
    print("✓ Material 'Gold' berhasil dibuat!")
    
    print("\n5. Membuat material plastic (Plastic Red)...")
    plastic_red = create_plastic_material("Plastic_Red", (0.8, 0.1, 0.1, 1.0), 0.4)
    print("✓ Material 'Plastic_Red' berhasil dibuat!")
    
    print("\n6. Assign material ke objek...")
    assign_material_to_object("Demo_Cube", "Material_Saya")
    assign_material_to_object("Demo_Sphere", "Gold")
    assign_material_to_object("Demo_Cylinder", "Plastic_Red")
    
    print("\n7. Setup lighting dan camera...")
    setup_lighting()
    setup_camera()
    
    print("\n8. Setup viewport shading...")
    setup_viewport_shading()
    
    # Cetak ringkasan
    print_material_info()
    
    print("\n✅ DEMO BERHASIL!")
    print("💡 Tips:")
    print("   - Tekan 'Z' dan pilih 'Rendered' untuk melihat hasil lebih realistis")
    print("   - Tekan Numpad 0 untuk melihat dari camera view")
    print("   - Buka Shading workspace untuk melihat node setup")
    print("   - Coba ubah nilai Roughness dan Metallic di Properties panel\n")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()