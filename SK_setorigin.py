import bpy

# アドオンに関する情報を保持する、bl_info変数
bl_info = {
	"name": "原点を選択物に移動",
	"author": "Shinichi kojima",
	"version": (1, 0),
	"blender": (2, 75, 0),
	"location": "3Dビュー > メッシュ",
	"description": "原点を選択物に移動するアドオン",
	"warning": "",
	"support": "TESTING",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"
}


#
class SkOriginMove(bpy.types.Operator):

	bl_idname = "object.sk_origin_move"
	bl_label = "原点を選択物に移動"
	bl_description = "原点を選択物に移動"
	bl_options = {'REGISTER', 'UNDO'}

	# メニューを実行した時に呼ばれる関数
	def execute(self, context):
		area = bpy.context.area
		old_type = area.type

		# エリアタイプをVIEW_3Dに変更しないと「選択物に3Dカーソルをスナップ」がエラーになる
		area.type = 'VIEW_3D'  
		bpy.ops.view3d.snap_cursor_to_selected()

		#エリアタイプの変更は不要だが、編集モードのままだと原点を3Dカーソルに移動がエラーになる
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		area.type = old_type

		return {'FINISHED'}


# メニューを構築する関数
def menu_fn(self, context):
	self.layout.separator()
	self.layout.operator(SkOriginMove.bl_idname)


# アドオン有効化時の処理
def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_fn)
	print("ON")


# アドオン無効化時の処理
def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_fn)
	bpy.utils.unregister_module(__name__)
	print("OFF")


# メイン処理
if __name__ == "__main__":
	register()