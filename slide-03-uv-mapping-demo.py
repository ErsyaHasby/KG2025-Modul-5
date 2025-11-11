"""
Blender Python Script untuk Demo UV Mapping
Dapat langsung dijalankan di Blender (Scripting > Run Script)
"""

import bpy
import bmesh

def create_demo_object():
    """Membuat objek demo untuk UV mapping"""
    
    # Hapus objek yang sudah ada (opsional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Buat objek yang lebih kompleks untuk demo UV mapping
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "UV_Demo_Object"
    
    # Subdivide untuk membuat lebih banyak faces
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("📦 Objek demo berhasil dibuat!")
    return obj

def smart_uv_project(obj, angle_limit=66, island_margin=0.02):
    """
    Melakukan Smart UV Project pada objek
    
    Parameters:
    - obj: Blender object
    - angle_limit: Sudut maksimum untuk menentukan island (degrees)
    - island_margin: Jarak antar UV islands (0.0 - 1.0)
    """
    
    # Pastikan objek adalah mesh
    if obj.type != 'MESH':
        print("Error: Objek bukan mesh!")
        return
    
    # Set objek sebagai active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Masuk ke Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Jalankan Smart UV Project
    bpy.ops.uv.smart_project(
        angle_limit=angle_limit * (3.14159 / 180),  # Convert ke radians
        island_margin=island_margin,
        area_weight=0.0,
        correct_aspect=True,
        scale_to_bounds=False
    )
    
    # Kembali ke Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print(f"🎯 Smart UV Project selesai untuk '{obj.name}'")

def cube_projection(obj, cube_size=1.0):
    """Melakukan Cube Projection UV mapping"""
    
    if obj.type != 'MESH':
        return
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Cube Projection
    bpy.ops.uv.cube_project(
        cube_size=cube_size,
        correct_aspect=True,
        clip_to_bounds=False,
        scale_to_bounds=False
    )
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"🎲 Cube Projection selesai untuk '{obj.name}'")

def mark_seams_by_angle(obj, angle=30):
    """
    Menandai seams berdasarkan sudut antar faces
    Berguna untuk hard edges
    """
    
    if obj.type != 'MESH':
        return
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Mark seams berdasarkan sudut
    bpy.ops.uv.seams_from_islands()
    
    # Atau gunakan edge angle
    bpy.ops.mesh.edges_select_sharp(sharpness=angle * (3.14159 / 180))
    bpy.ops.uv.mark_seam(clear=False)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print("🔪 Seams berhasil ditandai!")

def unwrap_with_seams(obj):
    """Unwrap berdasarkan seams yang sudah ditandai"""
    
    if obj.type != 'MESH':
        return
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Unwrap
    bpy.ops.uv.unwrap(
        method='ANGLE_BASED',  # atau 'CONFORMAL'
        margin=0.001
    )
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print("📐 Unwrap selesai!")

def pack_uv_islands(obj, margin=0.02, rotate=True):
    """
    Mengatur ulang UV islands agar efisien menggunakan texture space
    
    Parameters:
    - margin: Jarak antar islands
    - rotate: Izinkan rotasi untuk packing lebih efisien
    """
    
    if obj.type != 'MESH':
        return
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Pack islands
    bpy.ops.uv.pack_islands(
        margin=margin,
        rotate=rotate
    )
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print("📦 UV islands berhasil di-pack!")

def print_uv_coordinates(obj):
    """Mencetak koordinat UV dari objek"""
    
    if obj.type != 'MESH':
        return
    
    mesh = obj.data
    
    # Cek apakah ada UV layer
    if not mesh.uv_layers:
        print("Objek tidak memiliki UV map!")
        return
    
    # Dapatkan active UV layer
    uv_layer = mesh.uv_layers.active.data
    
    print(f"UV Coordinates untuk '{obj.name}':")
    print(f"Total UV points: {len(uv_layer)}")
    
    # Print beberapa koordinat pertama
    for i, uv in enumerate(uv_layer[:10]):
        print(f"  UV[{i}]: U={uv.uv.x:.4f}, V={uv.uv.y:.4f}")

def create_uv_checker_material():
    """
    Membuat material dengan checker pattern untuk validasi UV
    Berguna untuk melihat distorsi dan stretching
    """
    
    mat = bpy.data.materials.new(name="UV_Checker")
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
    
    print("♟️ UV Checker material berhasil dibuat!")
    return mat

def main():
    """Fungsi utama untuk menjalankan demo"""
    
    print("🗺️ === Blender UV Mapping Demo ===")
    print("1. 📦 Membuat objek demo...")
    obj = create_demo_object()
    
    print("\n2. ♟️ Membuat UV checker material...")
    checker_mat = create_uv_checker_material()
    
    print("\n3. 🎨 Assign checker material ke objek...")
    if obj.data.materials:
        obj.data.materials[0] = checker_mat
    else:
        obj.data.materials.append(checker_mat)
    
    print("\n4. 🎯 Melakukan Smart UV Project...")
    smart_uv_project(obj, angle_limit=66, island_margin=0.02)
    
    print("\n5. 📊 Print UV coordinates...")
    print_uv_coordinates(obj)
    
    print("\n6. 🔄 Mencoba metode UV mapping lain...")
    
    # Reset UV
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.reset()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("\n   a. 🎲 Cube Projection...")
    cube_projection(obj)
    
    # Reset UV lagi
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.reset()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("\n   b. 🔪 Mark seams dan unwrap...")
    mark_seams_by_angle(obj, angle=30)
    unwrap_with_seams(obj)
    
    print("\n   c. 📦 Pack UV islands...")
    pack_uv_islands(obj, margin=0.02, rotate=True)
    
    print("\n✅ === Demo selesai! ===")
    print(f"✅ Objek '{obj.name}' memiliki {len(obj.data.polygons)} faces")
    print(f"✅ UV layer: {len(obj.data.uv_layers)} layer(s)")
    print(f"✅ Material '{checker_mat.name}' diterapkan")
    print("\n💡 Tips:")
    print("   - Buka UV Editor (View > UV Editor) untuk melihat hasil UV mapping")
    print("   - Gunakan checker material untuk melihat distorsi")
    print("   - Coba berbagai metode UV mapping untuk hasil terbaik")
    print("   - Switch ke Material Preview mode untuk melihat checker pattern")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()