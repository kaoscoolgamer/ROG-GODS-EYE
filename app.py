import os
import tempfile
import time
from pathlib import Path
from collections import Counter

import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="GOD'S EYE // Vision System", page_icon="👁️", layout="wide", initial_sidebar_state="expanded")

# --- Futuristic studio / hacker aesthetic ---
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#000;--panel:rgba(8,12,18,.86);--line:rgba(175,221,255,.19);--muted:rgba(255,255,255,.52);--text:#fff;--cyan:#AFDDFF;--violet:#6ab7ff;--pink:#d2efff;--green:#AFDDFF}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;color:var(--text)}
.stApp{background:radial-gradient(ellipse at 72% -10%,rgba(175,221,255,.10),transparent 36%),radial-gradient(ellipse at 2% 35%,rgba(175,221,255,.045),transparent 27%),var(--bg);color:var(--text)}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.14;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(to bottom,black,transparent 92%)}
[data-testid="stHeader"]{background:rgba(5,7,13,.75)}
[data-testid="stSidebar"]{background:rgba(7,10,18,.96);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--text)}
.block-container{padding-top:1.4rem;max-width:1600px;position:relative;z-index:1}
#MainMenu,footer{visibility:hidden}
.goe-top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:18px 22px;margin:0 0 20px;border:1px solid var(--line);border-radius:0;background:linear-gradient(115deg,rgba(10,15,22,.92),rgba(0,0,0,.76));box-shadow:0 16px 70px rgba(0,0,0,.25);animation:fadeSlide .8s ease both;position:relative;overflow:hidden}
.goe-top:after{content:"";position:absolute;top:0;left:-45%;width:32%;height:1px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);animation:scan 5s ease-in-out infinite}
.brand{display:flex;align-items:center;gap:13px}.eye{width:48px;height:48px;border-radius:0;display:grid;place-items:center;font-size:25px;background:rgba(175,221,255,.05);border:1px solid rgba(175,221,255,.45);box-shadow:0 0 28px rgba(175,221,255,.10);animation:eyePulse 4s infinite}
.brand-title{font-size:23px;letter-spacing:.13em;font-weight:700}.eyebrow,.mono{font-family:'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase}.eyebrow{font-size:10px;color:var(--muted);margin-top:3px}.live{font:11px 'DM Mono',monospace;color:var(--green);display:flex;align-items:center;gap:8px}.live:before{content:"";width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green);animation:blink 1.8s infinite}
.hero{padding:22px 2px 25px;animation:fadeSlide .8s .12s both}.hero h1{font-size:clamp(35px,5vw,64px);line-height:.98;letter-spacing:-.055em;margin:0;color:#f4f6ff;font-weight:700}.hero h1 span{background:linear-gradient(100deg,#fff 8%,var(--cyan) 55%,#fff 90%);-webkit-background-clip:text;background-clip:text;color:transparent}.hero p{color:var(--muted);font-size:14px;margin:15px 0 0;max-width:680px}
.section-label{font:10px 'DM Mono',monospace;letter-spacing:.16em;color:#9ba8c8;text-transform:uppercase;margin:6px 0 12px}.glass{border:1px solid var(--line);background:linear-gradient(145deg,rgba(17,23,40,.92),rgba(8,12,22,.86));border-radius:0;padding:18px;box-shadow:0 12px 35px rgba(0,0,0,.18);animation:fadeSlide .65s both;transition:transform .25s,border-color .25s,box-shadow .25s}.glass:hover{transform:translateY(-2px);border-color:rgba(72,230,255,.4);box-shadow:0 15px 40px rgba(0,0,0,.3),0 0 24px rgba(72,230,255,.05)}
.metric-label{font:10px 'DM Mono',monospace;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}.metric-number{font-size:32px;line-height:1.2;font-weight:600;margin-top:7px;letter-spacing:-.04em}.metric-note{font-size:11px;color:var(--cyan);margin-top:5px}
.stButton>button{border:1px solid rgba(72,230,255,.45);border-radius:0;background:rgba(175,221,255,.10);color:#f2f6ff;font-weight:600;transition:all .2s;min-height:42px}.stButton>button:hover{border-color:var(--cyan);box-shadow:0 0 24px rgba(72,230,255,.15);transform:translateY(-1px);color:white}
[data-testid="stFileUploader"]{border:1px dashed rgba(112,135,190,.42);border-radius:0;background:rgba(8,12,22,.5);padding:8px}
[data-testid="stMetric"]{background:rgba(13,19,33,.82);border:1px solid var(--line);border-radius:0;padding:15px}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:0;overflow:hidden}
.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(9,13,23,.7);border:1px solid var(--line);padding:6px;border-radius:0}.stTabs [data-baseweb="tab"]{border-radius:0;color:var(--muted);height:42px}.stTabs [aria-selected="true"]{background:rgba(175,221,255,.1);color:var(--cyan)}
hr{border-color:var(--line)}
.boot{font:11px 'DM Mono',monospace;color:var(--cyan);letter-spacing:.12em;padding:12px 0;animation:flicker 2.4s infinite}
/* More visible motion: cinematic boot sequence and staggered interface reveal */
.boot-screen{position:relative;isolation:isolate;overflow:hidden;min-height:420px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(ellipse at center,rgba(26,52,92,.42),rgba(5,7,13,.98) 66%);border:1px solid rgba(175,221,255,.28);border-radius:0;padding:44px 20px;box-shadow:0 0 90px rgba(175,221,255,.08),inset 0 0 55px rgba(175,221,255,.035)}
.boot-screen:after{content:"G O D ’ S   E Y E   / /   V I S I O N   S Y S T E M";position:absolute;top:16px;left:18px;font:9px 'DM Mono',monospace;letter-spacing:.18em;color:rgba(175,221,255,.55)}.boot-screen:before{content:"";position:absolute;inset:-60%;z-index:-1;background:repeating-linear-gradient(0deg,transparent 0 5px,rgba(72,230,255,.055) 6px,transparent 7px);animation:scanlines 8s linear infinite}
.boot-rings{position:relative;width:130px;height:130px;margin-bottom:28px;border:1px solid rgba(175,221,255,.25);border-radius:0;display:grid;place-items:center;animation:ringEnter 1.1s cubic-bezier(.2,.8,.2,1) both}
.boot-rings:before,.boot-rings:after{content:"";position:absolute;border:1px solid rgba(175,221,255,.45);border-radius:0;inset:10px;transform:rotate(45deg);animation:orbit 5s linear infinite}
.boot-rings:after{inset:-10px;border-color:rgba(175,221,255,.2);border-style:dashed;animation:orbit 18s linear infinite reverse}
.rog-emblem{width:118px;height:92px;filter:drop-shadow(0 0 9px rgba(175,221,255,.65));animation:eyeGlitch 3.2s .4s infinite}
.boot-title{font-size:clamp(32px,6vw,66px);font-weight:700;letter-spacing:.16em;margin:0;text-shadow:0 0 26px rgba(72,230,255,.18);animation:titleReveal .9s .35s both}
.boot-subtitle{font:11px 'DM Mono',monospace;color:var(--muted);letter-spacing:.2em;text-transform:uppercase;margin-top:12px;animation:fadeSlide .8s .7s both}
.boot-progress{height:3px;width:min(360px,78%);background:rgba(120,145,190,.16);margin:26px 0 12px;overflow:hidden;border-radius:10px}
.boot-progress span{display:block;width:100%;height:100%;transform-origin:left;background:linear-gradient(90deg,#AFDDFF,#FFFFFF,#AFDDFF);box-shadow:0 0 15px var(--cyan);animation:progressCharge 2.8s .2s both}
.boot-status{font:10px 'DM Mono',monospace;letter-spacing:.13em;color:var(--cyan);animation:flicker 2s infinite}
.boot-screen .stButton>button{max-width:270px;margin-top:24px;letter-spacing:.12em;animation:buttonArrive .7s 1s both}
.goe-top{animation:fadeSlide .8s ease both, borderGlow 6s 1s infinite}
.hero{animation:fadeSlide .8s .16s both}
.glass{animation:cardArrive .7s both}
@keyframes ringEnter{from{opacity:0;transform:scale(.45) rotate(-35deg);filter:blur(8px)}to{opacity:1;transform:scale(1) rotate(0);filter:blur(0)}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes eyeGlitch{0%,87%,100%{transform:translateX(0);filter:hue-rotate(0)}89%{transform:translateX(-3px);filter:hue-rotate(55deg)}91%{transform:translateX(3px);filter:hue-rotate(-55deg)}93%{transform:translateX(0)}}
@keyframes titleReveal{from{opacity:0;letter-spacing:.5em;filter:blur(8px);transform:translateY(12px)}to{opacity:1;letter-spacing:.16em;filter:blur(0);transform:translateY(0)}}
@keyframes progressCharge{0%{transform:scaleX(0)}70%{transform:scaleX(.78)}100%{transform:scaleX(1)}}
@keyframes buttonArrive{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes scanlines{to{transform:translateY(40px)}}
@keyframes cardArrive{from{opacity:0;transform:translateY(22px) scale(.985);filter:blur(4px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
@keyframes borderGlow{0%,100%{box-shadow:0 16px 70px rgba(0,0,0,.25)}50%{box-shadow:0 16px 70px rgba(0,0,0,.25),0 0 24px rgba(72,230,255,.07)}}
.footer{font:10px 'DM Mono',monospace;color:#687693;letter-spacing:.08em;padding:22px 0 5px;border-top:1px solid var(--line);margin-top:28px}
@keyframes fadeSlide{from{opacity:0;transform:translateY(13px)}to{opacity:1;transform:translateY(0)}}
@keyframes scan{0%{left:-45%}65%,100%{left:115%}}
@keyframes eyePulse{0%,100%{box-shadow:0 0 15px rgba(72,230,255,.1)}50%{box-shadow:0 0 28px rgba(168,121,255,.28)}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes flicker{0%,95%,100%{opacity:1}96%{opacity:.55}98%{opacity:.8}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
""", unsafe_allow_html=True)

# First-visit intro: brief, skippable, and not repeated on every interaction.
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False
if not st.session_state.intro_done:
    st.markdown('''<div class="boot-screen"><div class="boot-rings"><svg class="rog-emblem" viewBox="0 0 160 120" role="img" aria-label="God’s Eye angular emblem"><path d="M8 60 L44 18 L80 18 L59 40 L42 40 L26 60 L42 80 L59 80 L80 102 L44 102 Z" fill="none" stroke="#AFDDFF" stroke-width="3" stroke-linejoin="miter"/><path d="M152 60 L116 18 L80 18 L101 40 L118 40 L134 60 L118 80 L101 80 L80 102 L116 102 Z" fill="none" stroke="#AFDDFF" stroke-width="3" stroke-linejoin="miter"/><path d="M52 60 L68 44 L92 44 L108 60 L92 76 L68 76 Z" fill="rgba(175,221,255,.12)" stroke="#FFFFFF" stroke-width="2"/><circle cx="80" cy="60" r="8" fill="#AFDDFF"/><path d="M80 0 V26 M80 94 V120" stroke="#AFDDFF" stroke-width="1" opacity=".65"/></svg></div><div class="eyebrow">VISUAL INTELLIGENCE / SYSTEM BOOT</div><div class="boot-title">GOD’S <span style="color:#48e6ff">EYE</span></div><div class="boot-subtitle">Computer vision // analytics suite</div><div class="boot-progress"><span></span></div><div class="boot-status">INITIALIZING MODULES&nbsp; · &nbsp;VISION ENGINE READY</div></div>''', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button("ENTER SYSTEM  ↗", type="primary", use_container_width=True):
            st.session_state.intro_done = True
            st.rerun()
    st.stop()

st.markdown('''<div class="goe-top"><div class="brand"><div class="eye">◉</div><div><div class="brand-title">GOD’S EYE<span style="color:#48e6ff">.</span></div><div class="eyebrow">Visual intelligence / analytics suite</div></div></div><div style="text-align:right"><div class="live">SYSTEM ONLINE</div><div class="eyebrow" style="margin-top:8px">YOLO VISION ENGINE · LOCAL ANALYSIS</div></div></div><div class="hero"><div class="eyebrow">01 / COMPUTER VISION LAB</div><h1>See beyond<br><span>the obvious.</span></h1><p>Analyse images and video with AI-powered object detection. Built as a CBSE Class 10 AI project by Zakhwan Padikkal · 10 R.</p></div>''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="eyebrow">SYSTEM CONTROLS</div>', unsafe_allow_html=True)
    st.markdown("### ◉ Vision engine")
    model_size = st.selectbox("Model profile", ["YOLOv8n · Fast", "YOLOv8s · Balanced", "YOLOv8m · Detail"], index=1, help="Larger models can detect smaller/farther-away people better, but are slower and use more memory.")
    model_file = {"YOLOv8n · Fast":"yolov8n.pt", "YOLOv8s · Balanced":"yolov8s.pt", "YOLOv8m · Detail":"yolov8m.pt"}[model_size]
    conf = st.slider("Confidence threshold", 0.10, 0.85, 0.25, 0.05)
    image_size = st.select_slider("Inference resolution", options=[640, 800, 960, 1280], value=960, help="Higher resolution can help with small people in crowded scenes, but takes longer.")
    person_focus = st.toggle("People-focused mode", value=True, help="Only show person detections in results. This does not identify individuals.")
    st.markdown("---")
    st.markdown('<div class="eyebrow">MODEL NOTES</div>', unsafe_allow_html=True)
    st.caption("For crowded crosswalks, start with YOLOv8s or YOLOv8m at 960 px. Fine-tuning on properly labelled crowd images is needed for a meaningful dataset-specific improvement.")
    st.caption("Use footage you own or have permission to analyse. This app detects objects, not identities.")

@st.cache_resource(show_spinner=False)
def load_model(weights):
    from ultralytics import YOLO
    return YOLO(weights)

def predict_image(model, rgb, confidence, imgsz, people_only):
    classes = [0] if people_only else None  # COCO class 0 is person
    result = model.predict(source=rgb, conf=confidence, imgsz=imgsz, classes=classes, verbose=False)[0]
    plotted = result.plot()
    plotted = plotted[:, :, ::-1]  # BGR to RGB
    records = []
    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            records.append({"Object": result.names.get(cls_id, str(cls_id)), "Confidence": round(float(box.conf[0].item()), 3), "Box (x1,y1,x2,y2)": [round(float(v), 1) for v in box.xyxy[0].tolist()]})
    return plotted, records

tab_image, tab_video, tab_training = st.tabs(["◈  IMAGE ANALYSIS", "◉  VIDEO ANALYSIS", "⌘  MODEL LAB"])

with tab_image:
    st.markdown('<div class="section-label">01 / Input source</div>', unsafe_allow_html=True)
    up = st.file_uploader("Drop an image for analysis", type=["png", "jpg", "jpeg", "webp"], key="image_upload")
    if up:
        image = Image.open(up).convert("RGB")
        col_a, col_b = st.columns([1.35, 1], gap="large")
        with col_a:
            st.markdown('<div class="section-label">SOURCE FRAME</div>', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        with col_b:
            st.markdown('<div class="section-label">ANALYSIS CONFIGURATION</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass"><div class="metric-label">Selected engine</div><div style="font-size:22px;font-weight:600;margin:5px 0">'+model_file+'</div><div class="metric-note">RESOLUTION / '+str(image_size)+' PX</div><div style="font-size:12px;color:#8e9ab6;margin-top:10px">'+('People-focused detection enabled' if person_focus else 'General object detection enabled')+'</div></div>', unsafe_allow_html=True)
            run = st.button("RUN DETECTION  ↗", type="primary", use_container_width=True, key="run_image")
        if run:
            try:
                with st.spinner("Loading vision engine and analysing frame…"):
                    model = load_model(model_file)
                    annotated, records = predict_image(model, np.array(image), conf, image_size, person_focus)
                st.markdown('<div class="section-label">02 / Detection output</div>', unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                with m1: st.markdown(f'<div class="glass"><div class="metric-label">Objects detected</div><div class="metric-number">{len(records)}</div><div class="metric-note">FRAME TOTAL</div></div>', unsafe_allow_html=True)
                with m2: st.markdown(f'<div class="glass"><div class="metric-label">People detected</div><div class="metric-number">{sum(1 for r in records if r["Object"]=="person")}</div><div class="metric-note">VISIBLE PERSON BOXES</div></div>', unsafe_allow_html=True)
                with m3: st.markdown(f'<div class="glass"><div class="metric-label">Model profile</div><div class="metric-number" style="font-size:25px">{model_size.split(" · ")[0]}</div><div class="metric-note">CONFIDENCE ≥ {conf:.0%}</div></div>', unsafe_allow_html=True)
                left, right = st.columns([1.4, 1], gap="large")
                with left:
                    st.markdown('<div class="section-label">ANNOTATED FRAME</div>', unsafe_allow_html=True)
                    st.image(annotated, use_container_width=True)
                    st.download_button("DOWNLOAD ANNOTATED IMAGE", data=Image.fromarray(annotated).tobytes(), file_name="gods_eye_detection.rgb", mime="application/octet-stream")
                with right:
                    st.markdown('<div class="section-label">DETECTION LOG</div>', unsafe_allow_html=True)
                    if records:
                        st.dataframe(records, use_container_width=True, hide_index=True)
                        counts = Counter(r["Object"] for r in records)
                        st.bar_chart(counts)
                    else:
                        st.info("No objects detected above this confidence threshold. Try lowering the threshold or using a larger model.")
            except Exception as e:
                st.error(f"Detection failed: {e}")
                st.info("If this is the first run, the model weights may need to download. On Streamlit Cloud, use opencv-python-headless and include libgl1 in packages.txt if OpenCV reports a missing system library.")
    else:
        st.markdown('<div class="glass"><div class="metric-label">Awaiting input</div><div style="font-size:22px;margin:9px 0">Upload a frame to begin.</div><div style="color:#8e9ab6;font-size:13px">For crowded pedestrian scenes, choose YOLOv8s or YOLOv8m and increase inference resolution. Small, occluded people may still be missed.</div></div>', unsafe_allow_html=True)

with tab_video:
    st.markdown('<div class="section-label">VIDEO / FRAME SAMPLING</div>', unsafe_allow_html=True)
    video = st.file_uploader("Upload a short video", type=["mp4", "mov", "avi", "m4v"], key="video_upload")
    stride_seconds = st.slider("Sample interval (seconds)", 0.5, 5.0, 1.5, 0.5)
    if video and st.button("ANALYSE VIDEO  ↗", type="primary", use_container_width=True):
        video_path = None
        cap = None
        try:
            import cv2
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(video.name).suffix or ".mp4") as tmp:
                tmp.write(video.getbuffer())
                video_path = tmp.name
            model = load_model(model_file)
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 24
            total = max(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            stride = max(1, int(fps * stride_seconds))
            progress = st.progress(0)
            frame_count = 0
            sampled = 0
            people_per_frame = []
            previews = []
            all_counts = Counter()
            while cap.isOpened():
                ok, frame = cap.read()
                if not ok: break
                if frame_count % stride == 0:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    plotted, records = predict_image(model, rgb, conf, image_size, person_focus)
                    previews.append(plotted)
                    sampled += 1
                    people_per_frame.append(sum(1 for r in records if r["Object"] == "person"))
                    all_counts.update(r["Object"] for r in records)
                frame_count += 1
                if frame_count % 10 == 0:
                    progress.progress(min(1.0, frame_count / total))
            cap.release(); cap = None
            progress.progress(1.0)
            st.markdown('<div class="section-label">VIDEO SUMMARY</div>', unsafe_allow_html=True)
            a,b,c = st.columns(3)
            a.metric("Frames analysed", sampled)
            b.metric("Peak people per sampled frame", max(people_per_frame, default=0))
            c.metric("Mean people per sampled frame", round(sum(people_per_frame)/len(people_per_frame), 1) if people_per_frame else 0)
            if previews:
                st.image(previews[:8], caption=[f"Sample {i+1}" for i in range(min(8,len(previews)))], width=260)
            if people_per_frame:
                st.line_chart({"People detected per sampled frame": people_per_frame})
            st.caption("Counts are detections per sampled frame, not unique people. This demo does not identify individuals or track them across cameras.")
        except Exception as e:
            st.error(f"Video analysis failed: {e}")
        finally:
            if cap is not None: cap.release()
            if video_path and os.path.exists(video_path): os.unlink(video_path)

with tab_training:
    st.markdown('<div class="section-label">MODEL LAB / CROWD SCENE IMPROVEMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass"><div class="metric-label">Current capability</div><div style="font-size:23px;font-weight:600;margin:8px 0">Pretrained COCO detector</div><div style="color:#8e9ab6;font-size:13px;line-height:1.7">The included model can detect the generic <b>person</b> class. It has not been fine-tuned specifically on Shibuya Crossing footage. Better crowded-scene performance requires a representative, labelled dataset and validation.</div></div>', unsafe_allow_html=True)
    st.markdown("#### A responsible fine-tuning workflow")
    st.markdown("""
1. Gather permitted, appropriately licensed crosswalk/crowd images representing different times, weather, camera angles, and crowd densities.
2. Label **every visible person** with bounding boxes in CVAT or Label Studio; use consistent rules for tiny, partially occluded people.
3. Split by source video/location into training, validation, and test sets so near-duplicate frames do not leak across splits.
4. Train from a pretrained checkpoint, then compare precision, recall, and mAP on a held-out crowded-scene test set.
5. Only replace the model after it demonstrably improves; dense crowds still produce missed detections and overlapping boxes.
""")
    st.code("yolo detect train model=yolov8s.pt data=shibuya_people.yaml epochs=50 imgsz=960 batch=8", language="bash")
    st.warning("This command is a template: it will not train until you provide a correctly labelled dataset and a valid shibuya_people.yaml file. Training is best done on a GPU. Do not use the system to identify people or infer personal attributes.")

st.markdown('<div class="footer">GOD’S EYE // VISUAL INTELLIGENCE SYSTEM &nbsp; • &nbsp; CREATED BY ZAKHWAN PADIKKAL · 10 R &nbsp; • &nbsp; AI WEEK PROJECT</div>', unsafe_allow_html=True)
