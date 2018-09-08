#定型サイズの平面を追加するアドオン
#20180407 Shinichi Kojima

bl_info = {
    "name": "Add Standard Size Plane",
    "author": "Shinichi Kojima",
    "version": (1, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Add > Mesh > Standard Size",
    "description": "Adds a new Mesh add Standard Size Plane Object",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "category": "Add Mesh",
    }


import bpy
from bpy.types import Operator
from bpy.props import StringProperty,FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from collections import OrderedDict


def add_object(self, context):
    verts = [
        Vector((0,0,0)),
        Vector((self.dimensions[self.sizeType][0], 0, 0)),
        Vector((self.dimensions[self.sizeType][0], self.dimensions[self.sizeType][1], 0)),
        Vector((0, self.dimensions[self.sizeType][1], 0)),
    ]
    edges = []

    # 厚みがあるとき、モディファイアでZの正方向に厚みが付くように面を反転
    if self.dimensions[self.sizeType][2] > 0:
        faces = [[3, 2, 1, 0]]
    else:
        faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="STD_"+self.sizeType)
    mesh.from_pydata(verts, edges, faces)

    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)

    # 厚み付けモディファイア追加
    if self.dimensions[self.sizeType][2] > 0:
        mod = bpy.context.object.modifiers.new(type="SOLIDIFY", name = "Solidify")
        mod.thickness = self.dimensions[self.sizeType][2]

    # 90度回転
    if self.dimensions[self.sizeType][3]:
        bpy.context.object.rotation_euler[0] = 1.5708


class SkAddStdsizePlane(Operator, AddObjectHelper):
    bl_idname = "mesh.sk_add_stdsize_plane"
    bl_label = "add Standard Size plane"
    bl_options = {'REGISTER', 'UNDO'}

    #dimensions[X, Y, Z, rotationX=90 ,日本語名]
    dimensions = OrderedDict([
        ("Diskcase_CD",(0.142, 0.124, 0.01, True, "CDケース")),
        ("Diskcase_DVD",(0.135, 0.190, 0.014, True, "DVDケース")),
        ("Diskcase_BD",(0.135, 0.170 ,0.013, True, "BDケース" )),

        ("Book_Bunko",(0.105, 0.148, 0, True, "文庫本")),
        ("Book_ComicS-Sinsyo",(0.113, 0.176, 0, True, "コミック小（新書）")),
        ("Book_ComicM-B6",(0.128, 0.182, 0, True, "コミック中（B6）")),
        ("Book_ComicL-A5",(0.148, 0.210, 0, True, "コミック大（A5）")),

        ("Paper_Postcard",(0.100, 0.148, 0, False, "はがき")),
        ("Paper_Futo(CHO3)",(0.120, 0.234, 0, False, "封筒 長3")),
        ("Paper_A4",(0.210, 0.297, 0, False, "A4")),
        ("Paper_B5",(0.182, 0.257, 0, False, "B5")),
        ("Paper_A2(Sinbunsi)",(0.420, 0.594, 0, False, "A2（新聞紙 片面)")),
        ("Paper_B2",(0.515, 0.728, 0, False, "B2")),
        ("Paper_Mozousi",(0.788, 1.091, 0, False, "模造紙")),
        ("Paper_Hansi",(0.243, 0.333, 0, False, "半紙")),

        ("SwitchBottun",(0.0295, 0.023, 0, True, "スイッチ")),
        ("SwitchPlate",(0.070, 0.120, 0.009, True, "スイッチプレート")),

        ("Box_Tissue",(0.230, 0.115, 0.050, False, "ティッシュボックス")),
        ("Box_Dress",(0.40, 0.74, 0.30, False, "衣装ケース")),

        ("Plane_Tatami(DANCHI-MA)",(0.85, 1.700, 0, False, "畳（団地間）")),
        ("Plane_Tenjo-tenken-ko",(0.5, 0.5, 0, False, "天井点検口")),
        ("Plane_Tenjo-Keikoutou-Umekomi",(0.25, 1.25, 0, False, "埋込型蛍光灯")),

        ("2x4_6ft",(0.038, 0.089, 1.8288, False, "ツーバイフォー")),

        ("Board_Colorbox",(0.40, 0.28, 0.015, False, "カラーボックス板")),

        ("10inch(16:9)",(0.221, 0.125, 0, True, "10インチ")),
    ])

    scale = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )
    
    sizeType = StringProperty()



    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# メインメニュー
class SkAddStdsizeMenu(bpy.types.Menu):
    bl_idname = "mesh.sk_add_stdsize_menu"
    bl_label = "add Standard Size"
    bl_description = "add Standard Size"

    def draw(self, context):
        layout = self.layout
        # サブメニューの登録
        for key in SkAddStdsizePlane.dimensions.keys():
            layout.operator(SkAddStdsizePlane.bl_idname, text=SkAddStdsizePlane.dimensions[key][4]).sizeType = key


        
# メニューを構築する関数
def menu_fnc(self, context):
    self.layout.separator()
    self.layout.menu(SkAddStdsizeMenu.bl_idname,text="Standard Size",icon='PLUGIN')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_fnc)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_fnc)


if __name__ == "__main__":
    register()
