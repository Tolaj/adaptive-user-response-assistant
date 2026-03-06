import cv2
import base64
from config.vlm import VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT, VLM_JPEG_QUALITY
from vision.camera import get_camera


def snap_b64() -> str:
    cap = get_camera()
    cap.grab()
    _, frame = cap.read()
    frame = cv2.resize(frame, (VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT))
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, VLM_JPEG_QUALITY])
    return base64.b64encode(buf).decode()
