import cv2
import numpy as np
import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

def process_image(img):
    np_img = np.array(img)
    img_bgr = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    height, width = img_bgr.shape[:2]
    y1, y2 = int(0 * height), int(1 * height)
    x1, x2 = int(0.1 * width), int(0.7 * width)

    cropped = img_bgr[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((8, 1), np.uint8))

    # Sharpening after morphological operation
    sharpen_kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
    sharpened = cv2.filter2D(closed, -1, sharpen_kernel)
    # thresh_val = 128
    # _, thresh = cv2.threshold(sharpened, thresh_val, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR with bounding boxes
    results = reader.readtext(sharpened, detail=1, allowlist='.0123456789')
    print("Raw OCR Results:", results)

    annotated = cv2.cvtColor(sharpened.copy(), cv2.COLOR_GRAY2BGR)

    float_results = []
    for bbox, text, conf in results:
        cleaned = re.sub(r'[^\d\.]+', '', text)
        if re.fullmatch(r'\d+\.?\d*', cleaned):
            float_results.append(cleaned)
        pts = np.array(bbox, dtype=np.int32)
        cv2.polylines(annotated, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(annotated, text, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    final = float_results[0] if float_results else "No reading"

    final = final[:2] + '.' + final[2:4] if len(final) > 2 else final

    # Convert intermediate results for Streamlit
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    closed_rgb = cv2.cvtColor(closed, cv2.COLOR_GRAY2RGB)
    sharpened_rgb = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2RGB)
    # thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return final, cropped_rgb, closed_rgb, sharpened_rgb, annotated_rgb
