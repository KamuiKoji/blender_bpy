# 原点をバウンディングボックス底面中心に移動

import bpy
from mathutils import Vector
import copy

# アドオンに関する情報を保持する、bl_info変数
bl_info = {
	"name": "原点をバウンディングボックス底面中心に移動",
	"author": "Shinichi kojima",
	"version": (1, 0),
	"blender": (2, 79, 0),
	"location": "3Dビュー > オブジェクト",
	"description": "原点をバウンディングボックス底面中心に移動するアドオン",
	"warning": "",
	"support": "TESTING",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"
	}


#
class SkSetOriginBottomBound(bpy.types.Operator):

	bl_idname = "object.sk_set_origin_bottom_bound"
	bl_label = "原点を底面中心に移動"
	bl_description = "原点をバウンディングボックス底面中心に移動"
	bl_options = {'REGISTER', 'UNDO'}

	# メニューを実行した時に呼ばれる関数
	def execute(self, context):
		area = bpy.context.area
		original_type = area.type

		# エリアタイプをVIEW_3Dに変更しないと「選択物に3Dカーソルをスナップ」がエラーになる
		area.type = 'VIEW_3D'

		obj = bpy.context.object
		# バウンディングボックスはローカル座標
		local_coords = obj.bound_box[:]

		# ローカル座標をワールド座標に変換するため、.matrix_worldを掛ける。from mathutils import Vector 必要。
		to_global = lambda p: obj.matrix_world * Vector(p[:])
		global_coords = [to_global(p).to_tuple() for p in local_coords]

		# 現在の3Dカーソルの位置を保存。参照渡しにならないようにcopy.deepcopy()。import copy 必要。
		original_cursor = copy.deepcopy(bpy.context.scene.cursor_location)

		# バウンディングボックス底面の対角の中心座標を3Dカーソル座標にセット
		for i in range(3):
			bpy.context.scene.cursor_location[i] = (global_coords[0][i] + global_coords[7][i])/2

		#エリアタイプの変更は不要だが、編集モードのままだと原点を3Dカーソルに移動がエラーになる
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		area.type = original_type
		bpy.context.scene.cursor_location = original_cursor

		return {'FINISHED'}


# メニューを構築する関数
def menu_fn(self, context):
	self.layout.separator()
	self.layout.operator(SkSetOriginBottomBound.bl_idname)


# アドオン有効化時の処理
def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_fn)
	print("[enable] " + SkSetOriginBottomBound.bl_idname )


# アドオン無効化時の処理
def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_fn)
	bpy.utils.unregister_module(__name__)
	print("[disable] " + SkSetOriginBottomBound.bl_idname )


# メイン処理
	if __name__ == "__main__":
		register()
