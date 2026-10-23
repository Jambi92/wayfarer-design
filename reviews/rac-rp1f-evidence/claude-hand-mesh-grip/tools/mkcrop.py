import pickle,numpy as np,sys
RD=pickle.load(open('rig_c3/rig_data.pkl','rb')); z=np.load(sys.argv[1]); V=z['V']
for s in 'LR': np.save(sys.argv[2]+'_%s.npy'%s, V[RD[s]['vid']]*[1,-1,1]/100)
