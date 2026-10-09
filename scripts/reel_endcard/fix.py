"""Re-set the "Yours" on a Home Portrait reel's end card in Charlotte with the tagline logo treatment (10 degree lean,
heavier weight), leaving the rest of the reel untouched. The new word is blended in with the end card's own crossfade.

usage: python3 scripts/reel_endcard/fix.py land space which saturday
Reads campaign-guide/reels/<key>.mp4 and writes <key>_charlotte.mp4 here (work files are gitignored). Run it on the
original reels only; the four in campaign-guide/reels were corrected on October 9, 2026.
"""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FF="/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
R="/home/user/builder-studio/campaign-guide/reels"
def run(*a): subprocess.run([FF,"-v","error","-y",*a],check=True)
for k in sys.argv[1:]:
    src=f"{R}/{k}.mp4"
    # crossfade timing from the start of the file: mean gray difference of the word area against the final frame
    raw=subprocess.run([FF,"-v","error","-i",src,"-vf","crop=500:274:300:798,scale=125:68","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    n=125*68; fr=[raw[i:i+n] for i in range(0,len(raw)-n+1,n)]; last=fr[-1]
    d=[sum(abs(a-b) for a,b in zip(f,last))/n for f in fr]
    i1=next(i for i in range(len(d)) if d[i]<0.6 and all(v<0.6 for v in d[i:]))
    # last frame before the fade starts: walk back from i1 while the difference keeps falling
    i0=i1-1
    while i0>0 and d[i0-1]>d[i0]+0.5: i0-=1
    T0,T1=i0/24,i1/24
    print(k,"fade frames",i0,"to",i1,"(%.3fs to %.3fs)"%(T0,T1),[round(v) for v in d[i0-1:i1+1]])
    run("-sseof","-0.5","-i",src,"-frames:v","1",f"card_{k}.png")
    subprocess.run(["node","card.js",k],check=True,env={"NODE_PATH":subprocess.run(["npm","root","-g"],capture_output=True,text=True).stdout.strip(),"PATH":"/usr/local/bin:/usr/bin:/bin"})
    run("-i",f"card_{k}_new.png","-i",f"card_{k}.png","-filter_complex","[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_mode=subtract,format=rgb24","-frames:v","1",f"P_{k}.png")
    run("-i",f"card_{k}.png","-i",f"card_{k}_new.png","-filter_complex","[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_mode=subtract,format=rgb24","-frames:v","1",f"N_{k}.png")
    D=T1-T0
    a=f"clip((T-{T0:.4f})/{D:.4f}\\,0\\,1)"
    fc=(f"[0:v]format=gbrp[v];[1:v]format=gbrp[p];[2:v]format=gbrp[n];"
        f"[v][p]blend=all_expr='A+{a}*B':shortest=1[v1];[v1][n]blend=all_expr='A-{a}*B':shortest=1,format=yuv420p[o]")
    run("-i",src,"-framerate","24","-loop","1","-i",f"P_{k}.png","-framerate","24","-loop","1","-i",f"N_{k}.png","-filter_complex",fc,
        "-map","[o]","-map","0:a?","-c:v","libx264","-crf","20","-preset","slow","-profile:v","high","-pix_fmt","yuv420p","-r","24",
        "-c:a","copy","-movflags","+faststart",f"{k}_charlotte.mp4")
    print(k,"done")
