import bpy, sys, os, math, mathutils
argv = sys.argv[sys.argv.index("--")+1:]
dl, out = argv[0], argv[1]
models = {"marble_bust_01":"2k","classic_laptop":"1k","circuit_board":"1k","digital_wrist_watch":"1k","cross_pein_hammer":"1k"}
for m,res in models.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_x = 512; sc.render.resolution_y = 512
    bpy.ops.import_scene.gltf(filepath=os.path.join(dl, m, f"{m}_{res}.gltf"))
    objs = [o for o in sc.objects if o.type=='MESH']
    pts = [o.matrix_world @ mathutils.Vector(c) for o in objs for c in o.bound_box]
    mn = mathutils.Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)))
    mx = mathutils.Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
    c = (mn+mx)/2; size = max(mx-mn)
    world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes=True
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.5,0.5,0.5,1)
    for i,(view,dirv) in enumerate([("front",(0,-1,0.25)),("side",(1,0,0.2))]):
        cam_data = bpy.data.cameras.new("c"); cam = bpy.data.objects.new("c", cam_data); sc.collection.objects.link(cam)
        d = mathutils.Vector(dirv).normalized()
        cam.location = c + d*size*2.2
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z','Y').to_euler()
        sc.camera = cam
        sc.render.filepath = os.path.join(out, f"{m}_{view}.png")
        bpy.ops.render.render(write_still=True)
    print("RENDERED", m)
