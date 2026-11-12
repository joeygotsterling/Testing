#!/usr/bin/env bash
# Generates soundtrack.m4a: a soft ambient pad (Am -> F -> C -> G) with crossfaded chords.
set -euo pipefail
cd "$(dirname "$0")"
env_(){ echo "clip((t-$1)/0.8\,0\,1)*clip(($2-t)/0.8\,0\,1)"; }
C(){ echo "($(env_ $1 $2))*(sin(2*PI*$3*t)+0.6*sin(2*PI*$4*t)+0.5*sin(2*PI*$5*t)+0.45*sin(2*PI*$6*t))"; }
EXPR="0.06*($(C -1 6 110 220 261.63 329.63)+$(C 5.2 11.6 87.31 174.61 261.63 349.23)+$(C 10.8 17.2 130.81 261.63 329.63 392)+$(C 16.4 23 98 196 293.66 392))"
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=$EXPR:s=44100:d=22" \
  -af "lowpass=f=1800,aecho=0.8:0.85:60|120:0.35|0.25,afade=t=in:d=1.5,afade=t=out:st=20:d=2,volume=1.4" \
  -c:a aac -b:a 160k soundtrack.m4a
echo "wrote soundtrack.m4a"
