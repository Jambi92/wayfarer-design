import sys,glob
from PIL import Image
pre=sys.argv[1]; out=sys.argv[2]; ncol=int(sys.argv[3]) if len(sys.argv)>3 else 3; W=int(sys.argv[4]) if len(sys.argv)>4 else 400
fs=sorted(glob.glob(pre+'_*.png')); n=len(fs); rows=(n+ncol-1)//ncol; im=Image.new('RGB',(W*ncol,W*rows),(30,30,34))
for i,f in enumerate(fs): im.paste(Image.open(f).resize((W,W)),((i%ncol)*W,(i//ncol)*W))
im.save(out)
