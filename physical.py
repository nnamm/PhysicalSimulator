import bpy
import os
import math


def delete_all():
    """ デフォルトで存在しているCubeを削除 """
    bpy.ops.object.delete()


def create_scene():
    """ シーンを作成 """
    # Cube作成
    cube_count = 10
    for axis_x in range(0, cube_count):
        for axis_y in range(0, cube_count):
            for axis_z in range(0, cube_count):
                # pattern1
                bpy.ops.mesh.primitive_cube_add(location=(axis_x*2, axis_y*2, axis_z*2))
                bpy.ops.rigidbody.object_add()

                # pattern2
                # bpy.ops.mesh.primitive_cube_add(location=(axis_x*2, axis_y*2, axis_z*2), rotation=(15, 15, 0))
                # bpy.ops.rigidbody.object_add()

                # pattern3
                # bpy.ops.mesh.primitive_cube_add(location=(axis_x*2, axis_y*2, axis_z*2))
                #bpy.ops.rigidbody.object_add()
                # bpy.ops.object.modifier_add(type='SOFT_BODY')

    # 平面作成
    bpy.ops.mesh.primitive_plane_add(location=(cube_count-1, cube_count-1, -10))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.data.objects["Plane"].scale = (cube_count+10, cube_count+10, 1)

    # カメラ
    bpy.data.objects["Camera"].location = (cube_count+20, cube_count+20, cube_count+20)
    bpy.data.objects["Camera"].rotation_euler = (math.pi/6, 0, math.pi*3/4)
    bpy.data.cameras["Camera"].lens = 10

    # 照明
    bpy.data.objects["Lamp"].location = (0, 0, cube_count+10)
    bpy.data.lamps["Lamp"].type = 'SUN'


def start_simulation():
    """ 物理シミュレーション """
    bpy.ops.ptcache.bake_all()

    # 動画作成
    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 300
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    bpy.data.scenes["Scene"].render.filepath = "Physical.avi"
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 250
    bpy.ops.render.render(animation=True)

    # 保存
    save_path = os.path.abspath(os.path.dirname(__file__))
    bpy.path.relpath(save_path)
    bpy.ops.wm.save_as_mainfile(filepath="Physical.blend", relative_remap=True)


if __name__ == '__main__':
    delete_all()
    create_scene()
    start_simulation()
