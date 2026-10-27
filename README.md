
# SmartVision - Camera-Based Attendance System

A Python-based attendance management system that uses OpenCV for face detection and camera-based student registration.

## Features

- Register students using a webcam
- Detect faces in real time
- Compare live face images with registered images
- Automatically record attendance
- Prevent duplicate attendance entries on the same day
- Store attendance records in CSV format
- View attendance records from the terminal

## Technologies Used

- Python
- OpenCV
- CSV
- OS and DateTime modules

## Project Structure

```text
smartvision-attendance-system/
├── attendance_system.py
├── requirements.txt
├── README.md
├── .gitignore
├── students/
└── attendance/
    └── attendance.csv
```

## Installation

1. Install Python 3.
2. Clone this repository:

```bash
git clone https://github.com/krishmahto/smartvision-attendance-system.git
```

3. Open the project folder:

```bash
cd smartvision-attendance-system
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python attendance_system.py
```

Follow the terminal menu to register students, start attendance, or view attendance records.

## Important Notes

- A working webcam is required.
- Register students before starting attendance.
- Student face images and attendance records are stored locally.
- The current implementation uses basic image-difference comparison and is not a robust facial recognition system.

## Future Improvements

- Improve face recognition accuracy
- Add a graphical user interface
- Generate attendance reports
- Add secure student data management

## Author

**Krish Kumar Mahto**
