import cv2
import os
import csv
import time
from datetime import datetime

# ============================================================
# SMARTVISION - CAMERA BASED ATTENDANCE SYSTEM
# ============================================================

# -----------------------------
# FOLDER SETTINGS
# -----------------------------

STUDENT_FOLDER = "students"
ATTENDANCE_FOLDER = "attendance"

ATTENDANCE_FILE = os.path.join(
    ATTENDANCE_FOLDER,
    "attendance.csv"
)

# Create folders if they don't exist
os.makedirs(STUDENT_FOLDER, exist_ok=True)
os.makedirs(ATTENDANCE_FOLDER, exist_ok=True)
2
2

# -----------------------------
# FACE DETECTOR
# -----------------------------

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# -----------------------------
# CREATE ATTENDANCE FILE
# -----------------------------

if not os.path.exists(ATTENDANCE_FILE):

    with open(
        ATTENDANCE_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Date",
            "Time"
        ])


# ============================================================
# REGISTER STUDENT
# ============================================================

def register_student():

    print("\n==============================")
    print("      REGISTER STUDENT")
    print("==============================")

    name = input("Enter student name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    # Remove characters that can cause filename problems
    safe_name = ""

    for character in name:

        if character.isalnum() or character in "_-":
            safe_name += character

    if safe_name == "":
        print("Invalid name.")
        return

    filename = os.path.join(
        STUDENT_FOLDER,
        safe_name + ".jpg"
    )

    # Open webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera could not be opened.")
        return

    print("\nCamera started.")
    print("Look at the camera.")
    print("Press SPACE to capture your face.")
    print("Press ESC to cancel.")

    while True:

        success, frame = camera.read()

        if not success:
            print("Could not read camera.")
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Register Student",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # SPACE
        if key == 32:

            if len(faces) == 0:

                print("No face detected.")
                continue

            # Use first detected face
            x, y, w, h = faces[0]

            face_image = gray[
                y:y + h,
                x:x + w
            ]

            cv2.imwrite(
                filename,
                face_image
            )

            print(
                "\nStudent registered successfully!"
            )

            print(
                "Saved as:",
                filename
            )

            break

        # ESC
        elif key == 27:

            print("Registration cancelled.")
            break

    camera.release()
    cv2.destroyAllWindows()


# ============================================================
# LOAD REGISTERED STUDENTS
# ============================================================

def load_students():

    students = []

    for filename in os.listdir(STUDENT_FOLDER):

        if filename.lower().endswith(".jpg"):

            path = os.path.join(
                STUDENT_FOLDER,
                filename
            )

            image = cv2.imread(
                path,
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                continue

            name = os.path.splitext(
                filename
            )[0]

            students.append(
                (name, image)
            )

    return students


# ============================================================
# CALCULATE FACE SIMILARITY
# ============================================================

def compare_faces(
    registered_face,
    live_face
):

    try:

        # Resize both images
        registered_face = cv2.resize(
            registered_face,
            (200, 200)
        )

        live_face = cv2.resize(
            live_face,
            (200, 200)
        )

        # Calculate absolute difference
        difference = cv2.absdiff(
            registered_face,
            live_face
        )

        # Average difference
        score = difference.mean()

        return score

    except Exception:

        return 999


# ============================================================
# MARK ATTENDANCE
# ============================================================

def mark_attendance(name):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    # Check whether student is already present
    already_present = False

    if os.path.exists(ATTENDANCE_FILE):

        with open(
            ATTENDANCE_FILE,
            "r",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (
                    row["Name"] == name
                    and row["Date"] == today
                ):

                    already_present = True
                    break

    if already_present:

        return False

    # Add attendance
    with open(
        ATTENDANCE_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            today,
            current_time
        ])

    return True


# ============================================================
# START ATTENDANCE
# ============================================================

def start_attendance():

    print("\n==============================")
    print("       START ATTENDANCE")
    print("==============================")

    students = load_students()

    if len(students) == 0:

        print(
            "No students registered."
        )

        print(
            "Register students first."
        )

        return

    print(
        "\nRegistered students:"
    )

    for student in students:

        print(
            "-",
            student[0]
        )

    print("\nStarting camera...")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print(
            "Camera could not be opened."
        )

        return

    print("\nAttendance started.")
    print("Press Q to stop.")

    last_recognized_name = ""
    recognition_time = 0

    while True:

        success, frame = camera.read()

        if not success:

            print(
                "Could not read camera."
            )

            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        recognized_name = "Unknown"

        for (x, y, w, h) in faces:

            live_face = gray[
                y:y + h,
                x:x + w
            ]

            best_name = "Unknown"
            best_score = 999

            # Compare with every registered student
            for name, registered_face in students:

                score = compare_faces(
                    registered_face,
                    live_face
                )

                if score < best_score:

                    best_score = score
                    best_name = name

            # Recognition threshold
            if best_score < 60:

                recognized_name = best_name

                # Mark attendance
                if recognized_name != last_recognized_name:

                    added = mark_attendance(
                        recognized_name
                    )

                    if added:

                        print(
                            recognized_name,
                            "marked PRESENT"
                        )

                    else:

                        print(
                            recognized_name,
                            "already marked today"
                        )

                    last_recognized_name = recognized_name
                    recognition_time = time.time()

            else:

                recognized_name = "Unknown"

            # Draw rectangle
            if recognized_name != "Unknown":

                rectangle_color = (
                    0,
                    255,
                    0
                )

            else:

                rectangle_color = (
                    0,
                    0,
                    255
                )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                rectangle_color,
                2
            )

            # Display name
            cv2.putText(
                frame,
                recognized_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                rectangle_color,
                2
            )

        # Display title
        cv2.putText(
            frame,
            "SMARTVISION ATTENDANCE",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press Q to exit",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "SmartVision Attendance",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

    camera.release()
    cv2.destroyAllWindows()


# ============================================================
# VIEW ATTENDANCE
# ============================================================

def view_attendance():

    print("\n==============================")
    print("       ATTENDANCE RECORD")
    print("==============================")

    if not os.path.exists(
        ATTENDANCE_FILE
    ):

        print(
            "Attendance file does not exist."
        )

        return

    with open(
        ATTENDANCE_FILE,
        "r",
        newline=""
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            print(
                " | ".join(row)
            )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("====================================")
        print("      SMARTVISION ATTENDANCE")
        print("====================================")
        print("1. Register Student")
        print("2. Start Attendance")
        print("3. View Attendance")
        print("4. Exit")
        print("====================================")

        choice = input(
            "Enter your choice: "
        )

        if choice == "1":

            register_student()

        elif choice == "2":

            start_attendance()

        elif choice == "3":

            view_attendance()

        elif choice == "4":

            print(
                "Thank you for using SmartVision."
            )

            break

        else:

            print(
                "Invalid choice."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()