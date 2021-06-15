import cv2
import mediapipe as mp
import numpy as np

from ..face_data import FaceAndIrisLandmarks
from ..settings import settings


class FaceTracking:
    def __init__(
        self,
        # max_num_faces=1,  # assume always 1 face
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_frame)

        if result.multi_face_landmarks is None:
            return None

        normalized_landmarks = np.empty(shape=(settings.face_landmark_num, 3), dtype=float)
        width_multiplier = float(settings.width) / settings.normalize_factor
        height_multiplier = float(settings.height) / settings.normalize_factor

        for landmarks in result.multi_face_landmarks:
            for i in range(settings.face_landmark_num):
                normalized_landmarks[i] = [
                    landmarks.landmark[i].x * width_multiplier,
                    landmarks.landmark[i].y * height_multiplier,
                    landmarks.landmark[i].z
                ]
            break  # assume 1 face

        return FaceAndIrisLandmarks(face_landmarks=normalized_landmarks)