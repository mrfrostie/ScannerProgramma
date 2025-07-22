import cv2
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import numpy as np

def decode_datamatrix_from_frame(frame):
    """
    Decodes a Data Matrix ECC 200 barcode from a video frame.

    Args:
        frame: A NumPy array representing the video frame.

    Returns:
        A list of Decoded objects, each containing the decoded data and rectangle.
        Returns None if decoding fails or no Data Matrix is found.
    """
    try:
        # Convert the OpenCV frame (NumPy array) to a PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        decoded_results = decode(image)
        return decoded_results
    except Exception as e:
        # print(f"Error decoding Data Matrix from frame: {e}") # Uncomment for debugging
        return None

if __name__ == "__main__":
    # Initialize the webcam
    cap = cv2.VideoCapture(0)  # 0 usually refers to the default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam

        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the frame to grayscale for potentially better decoding performance
        # Although pylibdmtx handles color images, grayscale can sometimes be more robust
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode Data Matrix from the current frame
        decoded_data = decode_datamatrix_from_frame(gray_frame)


        if decoded_data:
            for result in decoded_data:
                decoded_text = result.data.decode('utf-8')
                print(f"Decoded Data: {decoded_text}")
                # You can also draw the rectangle around the detected Data Matrix
                rect = result.rect
                cv2.rectangle(frame, (rect.left, rect.top),
                              (rect.left + rect.width, rect.top + rect.height),
                              (0, 255, 0), 2) # Green rectangle, thickness 2
                cv2.putText(frame, decoded_text, (rect.left, rect.top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Webcam Data Matrix Scanner', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()