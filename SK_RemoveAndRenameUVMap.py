#選択オブジェクトの非レンダリングアクティブなUVマップを消してレンダリングアクティブをリネーム

import bpy

#統一するUVマップの名前
UVMAP_NAME = 'UVMap'

selectObjects = bpy.context.selected_objects

for obj in selectObjects:
    if obj.type == 'MESH':
        removeList = []
        uvMaps = obj.data.uv_textures

        for uvmap in uvMaps:
          if uvmap.active_render == True:
            renameUvMap = uvmap.name
          else:
            removeList.append(uvmap.name)

        for uvMapName in removeList:
            uvMaps.remove(uvMaps[uvMapName])
            print('remove uvMap :'+obj.name+' :'+uvMapName)

        uvMaps[renameUvMap].name = UVMAP_NAME 
        print('rename :'+obj.name+' :'+renameUvMap)

print('finish')
