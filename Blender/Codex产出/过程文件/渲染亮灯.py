import bpy
from pathlib import Path
O=Path(__file__).resolve().parents[1]
s=bpy.context.scene;s.frame_set(60)
m=bpy.data.materials['Arrow bulbs | animate emission'];p=m.node_tree.nodes.get('Principled BSDF')
p.inputs['Emission Strength'].default_value=12;p.inputs['Emission Strength'].keyframe_insert('default_value',frame=60)
m.node_tree.update_tag();m.update_tag();bpy.context.view_layer.update()
s.render.filepath=str(O/'A_完整支架_亮灯.png')
bpy.ops.wm.save_as_mainfile(filepath=str(O/'A_收银台立牌_独立模型.blend'))
bpy.ops.render.render(write_still=True)
