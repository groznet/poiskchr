import os

BASE_DIR = "content/videos"
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=0Y_elO0Oxmg",
    "https://www.youtube.com/watch?v=iReLTGoI0FM",
    "https://www.youtube.com/watch?v=mHudW4UYqkg",
    "https://www.youtube.com/watch?v=BVcPCqQr4KI",
    "https://www.youtube.com/watch?v=qrZlcmKlJz4",
    "https://www.youtube.com/watch?v=BRVHuE0X6AM",
    "https://www.youtube.com/watch?v=5dQiqQSeu-k",
    "https://www.youtube.com/watch?v=NtbVSgAAkmI",
    "https://www.youtube.com/watch?v=k4ZYszRPjdY",
    "https://www.youtube.com/watch?v=8_atn_iK40I",
    "https://www.youtube.com/watch?v=A5mNKhmNmKg",
    "https://www.youtube.com/watch?v=apOMT31TVk8",
    "https://www.youtube.com/watch?v=80_KD1pgYCU",
    "https://www.youtube.com/watch?v=cxq34uF_iRA",
    "https://www.youtube.com/watch?v=tIZhglw6mb0",
    "https://www.youtube.com/watch?v=Hxp5j_sCdvE",
    "https://www.youtube.com/watch?v=faVORod_DZE",
    "https://www.youtube.com/watch?v=zGPE-uxLrrc",
    "https://www.youtube.com/watch?v=C29vxLKb74I",
    "https://www.youtube.com/watch?v=9AoSI_evFtk",
    "https://www.youtube.com/watch?v=wTO6pO32ffI",
    "https://www.youtube.com/watch?v=I0d4_aV5mtg",
    "https://www.youtube.com/watch?v=BNehvTjG9z8",
    "https://www.youtube.com/watch?v=LMg3-UQmyQI",
    "https://www.youtube.com/watch?v=vztfWCfc3FI",
    "https://www.youtube.com/watch?v=QRhnEzC4luA",
    "https://www.youtube.com/watch?v=eQf9ke2FqBE",
    "https://www.youtube.com/watch?v=WqeptLFGLfo",
    "https://www.youtube.com/watch?v=G4hTVFxgBdc",
    "https://www.youtube.com/watch?v=NpEaa2P7qZI",
    "https://www.youtube.com/watch?v=MmwlfJPw_8g",
    "https://www.youtube.com/watch?v=EyLNYNYtK_w",
    "https://www.youtube.com/watch?v=KY1eMvgrp2U",
    "https://www.youtube.com/watch?v=hKgUR3ImvtU",
    "https://www.youtube.com/watch?v=H9qkMbUK3JI",
    "https://www.youtube.com/watch?v=xZSkXBJPBoE",
    "https://www.youtube.com/watch?v=foAJk2cKn7c",
    "https://www.youtube.com/watch?v=Z6Ij3eX4qbM",
    "https://www.youtube.com/watch?v=NCKRBJegvqQ",
    "https://www.youtube.com/watch?v=JuNFQhCuM3g",
    "https://www.youtube.com/watch?v=gBJU5c-ILqg",
    "https://www.youtube.com/watch?v=bRypxA2h80Y",
    "https://www.youtube.com/watch?v=zcDRDh5zfE4",
    "https://www.youtube.com/watch?v=pVhpvMRkoRE",
    "https://www.youtube.com/watch?v=aFy2t-9Ff4c",
    "https://www.youtube.com/watch?v=YejRI9LrQ-A",
    "https://www.youtube.com/watch?v=apnsmhCdccw",
    "https://www.youtube.com/watch?v=-IPIKDP-th4",
    "https://www.youtube.com/watch?v=gEeiL3umAmY",
    "https://www.youtube.com/watch?v=kGYYSWvSup4",
    "https://www.youtube.com/watch?v=dg0BT-ZWEJU",
    "https://www.youtube.com/watch?v=y0l3QrvslMQ",
    "https://www.youtube.com/watch?v=5YPa7ROpm3o",
    "https://www.youtube.com/watch?v=0nl2kd1Go4w",
    "https://www.youtube.com/watch?v=pzQQRNKpRew",
    # ... add all URLs
]

for url in VIDEO_URLS:
    video_id = url.split("v=")[1]
    folder = os.path.join(BASE_DIR, video_id)
    os.makedirs(folder, exist_ok=True)
    
    index_md = os.path.join(folder, "index.md")
    if not os.path.exists(index_md):
        with open(index_md, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "Видео {video_id}"
date: 2025-11-27
url: "{url}"
thumb: "/images/thumbs/{video_id}.jpg"
---
""")
        print(f"Created {index_md}")
