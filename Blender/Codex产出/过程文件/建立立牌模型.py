import bpy, json, math
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC'
D=json.loads((O/'过程文件/灯泡坐标.json').read_text()); pts=[]
for item in D['outline']:
 if item[0] in ['M','L']:pts.append(tuple(item[1:]))
 elif item[0]=='C':
  p0=pts[-1];x1,y1,x2,y2,x3,y3=item[1:]
  for j in range(1,25):
   t=j/24;u=1-t;pts.append((u**3*p0[0]+3*u*u*t*x1+3*u*t*t*x2+t**3*x3,u**3*p0[1]+3*u*u*t*y1+3*u*t*t*y2+t**3*y3))
scale=.076/(2370-150)
def coord(x,y,depth=0):return ((x-1200)*scale,depth,.22-(y-110)*scale)
def mat(name,col,metal=0,rough=.3):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;m.node_tree.nodes.clear();p=m.node_tree.nodes.get('Principled BSDF') or m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');p.name='Principled BSDF';out=m.node_tree.nodes.get('Material Output') or m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
cream=mat('Cream enamel',(.79,.71,.52),.25,.26);steel=mat('Satin nickel',(.65,.68,.7),.92,.22);red=mat('Cherry red back',(.38,.032,.028),.4,.3)
mesh=bpy.data.meshes.new('True sign silhouette');mesh.from_pydata([coord(x,y) for x,y in pts],[],[list(reversed(range(len(pts))))]);mesh.update()
obj=bpy.data.objects.new('Checkout sign | 76 mm face',mesh);bpy.context.collection.objects.link(obj)
uv=mesh.uv_layers.new(name='Front exact registration')
for poly in mesh.polygons:
 for li in poly.loop_indices:
  x,y=pts[mesh.loops[li].vertex_index];uv.data[li].uv=(x/2400,1-y/1900)
paint=mat('A | screenprinted cream and cherry face',(1,1,1),.15,.32);p=paint.node_tree.nodes.get('Principled BSDF');tex=paint.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(O/'A_奶油搪瓷箭头_正面.png'));paint.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color']);obj.data.materials.append(paint);obj.data.materials.append(red)
sol=obj.modifiers.new('1.5 mm rolled metal body','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.material_offset=1;sol.material_offset_rim=1
bev=obj.modifiers.new('Soft enamel edge','BEVEL');bev.width=.0003;bev.segments=3
# Nickel trim following actual physical outline
curve=bpy.data.curves.new('Nickel perimeter','CURVE');curve.dimensions='3D';curve.bevel_depth=.00022;curve.bevel_resolution=3
spl=curve.splines.new('POLY');spl.points.add(len(pts)-1)
for p,(x,y) in zip(spl.points,pts):p.co=(*coord(x,y,-.0003),1)
spl.use_cyclic_u=True;ob=bpy.data.objects.new('Rolled nickel rim',curve);bpy.context.collection.objects.link(ob);ob.data.materials.append(steel)
def cylinder(name,radius,depth,loc,material,sc=(1,1,1)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(material);b=ob.modifiers.new('Rounded manufactured edge','BEVEL');b.width=min(depth*.25,.0025);b.segments=4
 for p in ob.data.polygons:p.use_smooth=True
 return ob
cylinder('Low oval weighted enamel base | 45 x 28 x 8 mm',.0225,.008,(0,.003,.004),cream,(1,.622,1))
cylinder('Base collar',.003,.008,(0,.003,.011),steel)
cylinder('Nickel pole | 2.5 mm',.00125,.162,(0,.003,.092),steel)
# Physical lamp domes; keyed emission for later animation handoff.
lamp=mat('Arrow bulbs | animate emission',(.93,.69,.30),.1,.25);p=lamp.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.65,.21,1)
for frame,val in [(1,0),(59,0),(60,12),(90,12)]:p.inputs['Emission Strength'].default_value=val;p.inputs['Emission Strength'].keyframe_insert('default_value',frame=frame)
for i,(x,y) in enumerate(D['centres']):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=20*scale,location=coord(x,y,-.00036));ob=bpy.context.object;ob.name=f'Arrow bulb {i+1}';ob.scale=(1,.6,1);ob.data.materials.append(lamp)
 for f in ob.data.polygons:f.use_smooth=True
floor=mat('Warm grey studio',(.55,.53,.48),0,.7)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0005));bpy.context.object.name='Studio floor';bpy.context.object.data.materials.append(floor)
scene.world.color=(.35,.35,.35)
def area(name,loc,energy,size):
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.name=name;ob.data.energy=energy;ob.data.shape='DISK';ob.data.size=size;ob.rotation_euler=(Vector((0,0,.11))-ob.location).to_track_quat('-Z','Y').to_euler()
area('Large softbox',(-.18,-.22,.34),6,.2);area('Right fill',(.18,-.08,.25),2,.18);area('Rear edge',(.08,.15,.28),4,.15)
bpy.ops.object.camera_add(location=(.11,-.48,.26));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.112))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.27;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1100;scene.render.resolution_y=1600;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.fps=30;scene.frame_end=90
scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-1.3;scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(O/'A_收银台立牌_独立模型.blend'))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'A_收银台立牌_独立模型.blend'))
for frame,name in [(1,'A_完整支架_未亮灯.png'),(60,'A_完整支架_亮灯.png')]:
 scene.frame_set(frame);lamp.node_tree.update_tag();lamp.update_tag();bpy.context.view_layer.update();scene.render.filepath=str(O/name);bpy.ops.render.render(write_still=True)
