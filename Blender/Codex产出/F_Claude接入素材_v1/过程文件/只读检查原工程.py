import bpy,json
from pathlib import Path
s=bpy.context.scene
r={'scene':{'units':s.unit_settings.system,'scale_length':s.unit_settings.scale_length,'frames':[s.frame_start,s.frame_end],'fps':s.render.fps},'objects':[]}
for o in bpy.data.objects:
 d={'name':o.name,'type':o.type,'location':list(o.location),'dimensions':list(o.dimensions),'materials':[m.name for m in o.data.materials if m] if hasattr(o.data,'materials') else []}
 if o.type=='FONT':d['text']=o.data.body
 r['objects'].append(d)
r['images']=[{'name':i.name,'path':i.filepath,'size':list(i.size)} for i in bpy.data.images]
Path('/Users/kummerspeck/Documents/ChatGPT/Blender/Codex产出/F_Claude接入素材_v1/过程文件/原工程只读检查.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
