import bpy, bmesh, numpy as np, sys
a=sys.argv[sys.argv.index('--')+1:]; D=np.load(a[0]); V=D['V']; Q=D['Q']
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],Q.tolist()); ob=bpy.data.objects.new('o',me); bpy.context.collection.objects.link(ob)
m=ob.modifiers.new('s','SUBSURF'); m.levels=int(a[2]); m.render_levels=int(a[2]); m.uv_smooth='NONE'; m.boundary_smooth='ALL'
dg=bpy.context.evaluated_depsgraph_get(); e=ob.evaluated_get(dg).to_mesh()
V2=np.array([v.co[:] for v in e.vertices]); Q2=np.array([p.vertices[:] for p in e.polygons])
np.savez(a[1],V=V2,Q=Q2)
