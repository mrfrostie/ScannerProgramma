import cv2
from pylibdmtx.pylibdmtx import decode
import numpy as np

def decode_datamatrix_from_frame(frame):
    # Optionally resize for speed
    frame = cv2.resize(frame, (640, 480))
    # pylibdmtx can decode directly from numpy array (grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded_results = decode(gray)
    return decoded_results, frame

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    cap.set(cv2.CAP_PROP_FPS, 60)

    print("Press 'q' to quit.")
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Resize for speed
        frame = cv2.resize(frame, (640, 480))

        # Decode every 2nd frame for higher FPS
        if frame_count % 1 == 0:
            decoded_data, display_frame = decode_datamatrix_from_frame(frame)
        else:
            display_frame = frame
            decoded_data = None

        if decoded_data:
            for result in decoded_data:
                decoded_text = result.data.decode('utf-8')
                rect = result.rect
                cv2.rectangle(display_frame, (rect.left, rect.top),
                              (rect.left + rect.width, rect.top + rect.height),
                              (0, 255, 0), 2)
                cv2.putText(display_frame, decoded_text, (rect.left, rect.top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                print(f"Decoded Data: {decoded_text}")

        cv2.imshow('Webcam Data Matrix Scanner', display_frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()