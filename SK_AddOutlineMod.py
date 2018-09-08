# 選択オブジェクトに輪郭線用の厚み付けとベベルモディファイアを追加します。

import bpy
from bpy.props import StringProperty, FloatVectorProperty, EnumProperty

# アドオンに関する情報を保持する、bl_info変数
bl_info = {
	"name": "輪郭線用モディファイアの設定",
	"author": "Shinichi kojima",
	"version": (1, 0),
	"blender": (2, 79, 0),
	"location": "3Dビュー > オブジェクト",
	"description": "輪郭線用モディファイアの設定",
	"warning": "",
	"support": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"
	}



class SkAddOutlineMod(bpy.types.Operator):

	bl_idname = "object.sk_add_outline_mod"
	bl_label = "輪郭線用モディファイアの設定"
	bl_description = "輪郭線用に厚み付けとベベルのモディファイアを設定"
	bl_options = {'REGISTER', 'UNDO'}

	type = StringProperty()

	# メニューを実行した時に呼ばれる関数
	def execute(self, context):
		mod_name = 'OUTLINE.'
		selectObject = bpy.context.selected_objects

		for i in range(0,len(selectObject)):
			#モディファイアを追加する
			if self.type == 'add':
				bpy.context.scene.objects.active = selectObject[i]
				
				#bevel edge ベベルによるアウトライン
				if bpy.context.object.type == 'MESH':
					mod = bpy.context.object.modifiers.new(type="BEVEL", name=mod_name + "BEVEL")
					mod.width = 0.004
					mod.limit_method = 'ANGLE'
					mod.angle_limit = 1.55334
					mod.material = 1
				
				# urapori edge 裏ポリによるアウトライン
				if (bpy.context.object.type == 'MESH' or bpy.context.object.type == 'CURVE'):
					mod = bpy.context.object.modifiers.new(type="SOLIDIFY", name=mod_name + "URAPORI")
					mod.thickness = -0.003
					mod.use_flip_normals = True
					mod.material_offset = 1
				
				#オブジェクトのワイヤーフレーム表示のチェックをオフ
				bpy.context.object.show_wire = False
				bpy.context.object.show_all_edges = False

			# モディファイアを削除する
			elif self.type == 'remove':
				for k in range(0,len(selectObject[i].modifiers)):
					if k > len(selectObject[i].modifiers)-1:
						break
					while( -1 != selectObject[i].modifiers[k].name.find(mod_name)):
						selectObject[i].modifiers.remove(selectObject[i].modifiers[k])
						if k > len(selectObject[i].modifiers)-1:
							break

			# モディファイアの表示とレンダリングをオンにする
			elif self.type == 'on':
				for j in range(0,len(selectObject[i].modifiers)):
					if -1 != selectObject[i].modifiers[j].name.find(mod_name):
						selectObject[i].modifiers[j].show_render = True
						selectObject[i].modifiers[j].show_viewport = True

			# モディファイアの表示とレンダリングをオフにする
			elif self.type == 'off':
				for j in range(0,len(selectObject[i].modifiers)):
					if -1 != selectObject[i].modifiers[j].name.find(mod_name):
						selectObject[i].modifiers[j].show_render = False
						selectObject[i].modifiers[j].show_viewport = False

		return {'FINISHED'}


# メインメニュー
class SkAddOutlineModMenu(bpy.types.Menu):

	bl_idname = "object.sk_add_outline_mod_menu"
	bl_label = "輪郭線用モディファイアの設定"
	bl_description = "輪郭線用にベベルと厚み付けを設定"

	def draw(self, context):
		layout = self.layout
		# サブメニューの登録
		layout.operator(SkAddOutlineMod.bl_idname, text='追加').type = 'add'
		layout.operator(SkAddOutlineMod.bl_idname, text='削除').type = 'remove'
		layout.operator(SkAddOutlineMod.bl_idname, text='オン').type = 'on'
		layout.operator(SkAddOutlineMod.bl_idname, text='オフ').type = 'off'


# メニューを構築する関数
def menu_fn(self, context):
	self.layout.separator()
	#サブメニュー作るときはlayout.menuをつかう
	self.layout.menu(SkAddOutlineModMenu.bl_idname)


# アドオン有効化時の処理
def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_fn)
	print("[enable] " + SkAddOutlineMod.bl_idname )


# アドオン無効化時の処理
def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_fn)
	bpy.utils.unregister_module(__name__)
	print("[disable] " + SkAddOutlineMod.bl_idname )


# メイン処理
	if __name__ == "__main__":
		register()
