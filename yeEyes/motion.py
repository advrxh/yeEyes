import cv2
import imageio

from pathlib import Path
import time, datetime
import logging

from yeEyes.settings import *
from yeEyes.dis_hook import Hook

cap = cv2.VideoCapture(VIDEO_SOURCE)

prev_rec = None
record_start = None
prev_frame = None
recording = False
gif_frames = []
running = True

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s]:[%(asctime)s]:[%(message)s]"
)

hook = Hook()

FRAME_SIZE = (int(cap.get(3)), int(cap.get(4)))


def write_to_gif(loc, gif_frmes):
    running = False
    logging.info("TEMPERORY MONITOR SHUTDOWN")
    logging.info(f"ENCODING GIF TO -> {loc}")
    with imageio.get_writer(loc, mode="I") as writer:
        for idx, frm in enumerate(gif_frmes):
            frm = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
            writer.append_data(frm)
    running = True
    logging.info("REBOOT INTIATED")


while running:
    time.sleep(0.2)
    _, frm = cap.read()
    if _:
        gray_scale = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        gray_scale = cv2.GaussianBlur(gray_scale, (21, 21), 0)
    else:
        break
    if prev_frame is None:
        prev_frame = gray_scale
        continue
    frm_diff = cv2.absdiff(prev_frame, gray_scale)

    frm_threshold = cv2.threshold(frm_diff, 50, 255, cv2.THRESH_BINARY)[1]
    frm_threshold = cv2.dilate(frm_threshold, None, iterations=5)

    contours, _ = cv2.findContours(
        frm_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not recording:
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                logging.info("PERMIETER INTACT")
                break
            logging.info("MOTION DETECTED")
            recording = True
            current_time = str(datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
            rec = str(Path(OUTPUT_DIR + f"/CLIP_{current_time}.gif").resolve())
            prev_rec = rec
            record_start = time.time()
    if recording:
        if (time.time() - record_start) <= CLIP_DURATION:
            gif_frames.append(frm)
        else:
            if prev_rec is not None:
                # cv2.destroyAllWindows()
                write_to_gif(prev_rec, gif_frames)
                hook.notify(prev_rec)
            prev_rec = None
            record_start = None
            recording = False
            gif_frames = []

    # cv2.imshow("img", frm)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
# cv2.destroyAllWindows()
