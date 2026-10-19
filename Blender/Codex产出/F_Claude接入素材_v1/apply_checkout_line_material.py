"""Optional Blender script: recolor the existing nine checkout dashes only.
No object moves, geometry changes, timeline changes or file saving.
"""
import bpy, re, json
names=[f'LineDash_{i}' for i in range(9)]
missing=[n for n in names if n not in bpy.data.objects]
if missing:
    raise RuntimeError('Expected original dashes missing; nothing changed: '+', '.join(missing))
objects=[bpy.data.objects[n] for n in names]
if any(o.type!='MESH' for o in objects):
    raise RuntimeError('Expected mesh objects; nothing changed.')
before={o.name:{'location':tuple(o.location),'dimensions':tuple(o.dimensions),'old_materials':[m.name if m else None for m in o.data.materials]} for o in objects}
def linear_hex(value):
    c=[int(value[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)+(1,)
name='M_Codex_CheckoutLine_F_v1'
m=bpy.data.materials.new(name) # always a new material; never edit shared M_Ink
m.use_nodes=True;m.node_tree.nodes.clear();n=m.node_tree.nodes;l=m.node_tree.links
out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled')
p.inputs['Roughness'].default_value=.82;p.inputs['Metallic'].default_value=0
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=45;tex.inputs['Detail'].default_value=2
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=linear_hex('203B52');ramp.color_ramp.elements[1].color=linear_hex('29465D')
coord=n.new('ShaderNodeTexCoord');bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.000012
l.new(coord.outputs['Generated'],tex.inputs['Vector']);l.new(tex.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],p.inputs['Base Color']);l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal']);l.new(p.outputs['BSDF'],out.inputs['Surface'])
m.diffuse_color=linear_hex('243F57')
for o in objects:
    # Keep polygon material indices, secondary slots, transforms and mesh intact.
    if len(o.data.materials):o.data.materials[0]=m
    else:o.data.materials.append(m)
    assert tuple(o.location)==before[o.name]['location']
    assert tuple(o.dimensions)==before[o.name]['dimensions']
print('CODEX_LINE_CHECK '+json.dumps({'material':m.name,'count':len(objects),'preserved_geometry':True,'before':before},ensure_ascii=False))
