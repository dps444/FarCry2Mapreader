from os import walk,mkdir
from os.path import expanduser
from json import dump
from PIL.Image import frombytes,merge
from PIL import ImageChops
def fun():
    mlist={}
    for path,subdir,file in walk(expanduser("~")+"\\Documents\\My Games\\Far Cry 2"):
        for name in file:
            if name.endswith(".fc2map"):
                with open(f"{path}/{name}","rb") as f:
                    try:
                        f.seek(28)
                        cname=f.read(int.from_bytes(f.read(4),"little")).decode("utf-8",errors="replace")
                        f.seek(f.tell()+8)
                        aname=f.read(int.from_bytes(f.read(4),"little")).decode("utf-8",errors="replace")
                        mname=f.read(int.from_bytes(f.read(4),"little")).decode("utf-8",errors="replace")
                        mpid=int.from_bytes(f.read(8),"little")
                        f.seek(f.tell()+72)
                        msize=int.from_bytes(f.read(4),"little")
                        f.seek(f.tell()+4)
                        modes=int.from_bytes(f.read(4),"little")
                        val1=int.from_bytes(f.read(4),"little")
                        val2=int.from_bytes(f.read(4),"little")
                        val3=int.from_bytes(f.read(4),"little")
                        val4=int.from_bytes(f.read(4),"little")
                        image=frombytes("RGBA",(128,128),f.read(int(val1*val2*val3*val4/8)),"raw")
                        #correct colours and pixels
                        image = image.convert("RGB").convert("RGBA")
                        r, g, b, a = image.split()
                        image = merge("RGBA", (b, g, r, a))
                        image = ImageChops.offset(image, -3, 0)
                        last_columns = image.crop((val1 - 3, 0, val1, val1))
                        last_columns = last_columns.crop((0, 1, 3, val1))
                        last_columns = last_columns.resize((3, val1 - 1))
                        image.paste(last_columns, (val1 - 3, 0))
                        image.save(f"thumbs/{mpid}.png")
                        p=path.replace(expanduser("~")+"\\Documents\\My Games\\Far Cry 2\\","")
                        for i in ["$","#","[","]","/","."]:
                            mname=mname.replace(i,"_")
                        mlist[mname]={
                            "creator":cname,
                            "author":aname,
                            "size":msize,
                            "mapid":mpid,
                            "modes":modes,
                            "location":f"{p}\\{name}"
                        }
                        mlist[mpid]=f"{p}\{name}"
                        print(mname,"processed")
                    except Exception as e:
                        print(name,e)
    with open("maps.json","w") as f:
        dump(mlist,f,indent=6)
try:
    mkdir("thumbs")
except Exception:
    pass
fun()
