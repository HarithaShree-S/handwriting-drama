"""
Handwriting Forensics Lab - Computer Vision Analyzer
Calculates ink density, contour dimensions, and variation metrics using OpenCV.
"""

import cv2
import numpy as np
from typing import Optional, Dict


def analyze_handwriting(image_bytes: bytes) -> Optional[Dict[str, int]]:
    """
    Takes uploaded image bytes, runs real computer vision processing,
    and returns a dictionary of raw physical metrics:
      - pen_aggression: based on ink density ratio (Otsu thresholding)
      - letter_ego: based on average contour height vs image height
      - personal_space: based on average horizontal gap between word contours
      - chaos_level: based on standard deviation of contour heights
    """
    if not image_bytes:
        return None

    try:
        # Convert image bytes to an OpenCV image array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None or img.size == 0:
            return None

        # Step 1: Convert to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 2: Apply Otsu's Thresholding (separates ink from background)
        # Binary inverse: Ink becomes white (255), paper becomes black (0) for math counting
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Metric 1: Pen Aggression (Ink Density)
        total_pixels = thresh.size
        ink_pixels = cv2.countNonZero(thresh)
        ink_density_ratio = ink_pixels / total_pixels if total_pixels > 0 else 0
        # Scale into a 0 - 100 range (typical handwriting occupies 2% to 15% of page space)
        pen_aggression = int(np.clip((ink_density_ratio / 0.12) * 100, 10, 99))

        # Step 3: Find Contours (Word & Letter Bounding Boxes)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out tiny noise dots
        valid_boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 5 and h > 5:  # ignore micro pixels
                valid_boxes.append((x, y, w, h))

        if not valid_boxes:
            return {
                "pen_aggression": pen_aggression,
                "letter_ego": 50,
                "personal_space": 50,
                "chaos_level": 50,
            }

        # Metric 2: Letter Ego (Average height of character/word contours)
        heights = [box[3] for box in valid_boxes]
        avg_height = float(np.mean(heights))
        # Normalize average height against image height
        img_height = img.shape[0]
        height_ratio = (avg_height / img_height) if img_height > 0 else 0.05
        letter_ego = int(np.clip((height_ratio / 0.10) * 100, 15, 98))

        # Metric 3: Word Personal Space (Average gap between horizontally sorted bounding boxes)
        valid_boxes = sorted(valid_boxes, key=lambda b: b[0])  # sort left to right
        gaps = []
        for i in range(len(valid_boxes) - 1):
            x1, y1, w1, h1 = valid_boxes[i]
            x2, y2, w2, h2 = valid_boxes[i + 1]
            gap = x2 - (x1 + w1)
            if 2 < gap < 200:  # reasonable gap range
                gaps.append(gap)

        avg_gap = float(np.mean(gaps)) if gaps else 25.0
        personal_space = int(np.clip((avg_gap / 60) * 100, 10, 95))

        # Metric 4: Chaos Level (Variation/Standard Deviation in contour heights)
        height_std = float(np.std(heights)) if len(heights) > 1 else 10.0
        chaos_level = int(np.clip((height_std / 30) * 100, 15, 99))

        return {
            "pen_aggression": pen_aggression,
            "letter_ego": letter_ego,
            "personal_space": personal_space,
            "chaos_level": chaos_level,
        }

    except Exception:
        # Graceful fallback in case of unexpected decoding or OpenCV exceptions
        return None