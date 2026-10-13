import trimesh, numpy as np, igl, time, sys
D='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd'
m=trimesh.load(D+'/GO-RD0-SOURCE.obj',process=False); V=np.ascontiguousarray(m.vertices,float); F=np.ascontiguousarray(m.faces,np.int64)
h=float(sys.argv[1]) if len(sys.argv)>1 else 0.6
lo=np.floor(V.min(0))-3; hi=np.ceil(V.max(0))+3
xs=np.arange(lo[0],hi[0],h); ys=np.arange(lo[1],hi[1],h); zs=np.arange(lo[2],hi[2],h)
G=np.zeros((len(xs),len(ys),len(zs)),np.float32); X,Y=np.meshgrid(xs,ys,indexing='ij'); t=time.time()
for k in range(0,len(zs),20):
    Z=zs[k:k+20]; P=np.stack(np.broadcast_arrays(X[...,None],Y[...,None],Z[None,None,:]),-1).reshape(-1,3)
    G[:,:,k:k+20]=igl.fast_winding_number(V,F,P).reshape(len(xs),len(ys),len(Z))
print(time.time()-t); np.savez_compressed(D+'/wn.npz',G=G,lo=lo,h=h)
