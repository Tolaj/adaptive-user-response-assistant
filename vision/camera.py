import cv2
from config.vlm import VLM_CAMERA_INDEX, VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT

_cap = None


def get_camera():
    global _cap
    if _cap is not None:
        return _cap
    _cap = cv2.VideoCapture(VLM_CAMERA_INDEX)
    _cap.set(cv2.CAP_PROP_FRAME_WIDTH, VLM_FRAME_WIDTH)
    _cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VLM_FRAME_HEIGHT)
    _cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return _cap


def release_camera():
    global _cap
    if _cap:
        _cap.release()
        _cap = None
