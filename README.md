# Face Attend
<p align="center">
    <img width = "300" height = "300" src="./face_attend.png">
</p>



## Features
- Adding face data of a person to the database
- Detect face of known person using video feed
- Mark attendance of a valid person when detected
- Generating a csv file with attendance for a particalar date



## Instructions 📝
- **Create a virtual environment:**
     ```python3 -m venv .venv```
- **Activate the virtual environment:**
    ```source .venv/bin/activate```
- **Install the package:**
    ```pip install faceattend```

>[!NOTE]
The above instructions are specific to macOS and Linux.</br>

### Windows specific instructions
- **Creating virtual environments see [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments)**</br>
- **For issues with installation of the face-recognition package see [here](https://stackoverflow.com/questions/70001837/problem-in-installing-python-library-face-recognition-on-windows-10-11)**

   
## Database setup 🛢
### Create the database

- Import the ```create_database()``` function from ```create_database``` module</br>
```from faceattend.create_datebase import create_database```

- Then just use the ```create_database()``` function to create the database
```create_database()```
- When database is successfully created it displays</br>
```Database created!```

### Add valid faces in database

- Import the ```Face``` class from ```face``` module</br>
```from faceattend.face import Face```

- Now use the ```Face``` class's add_face method to add face data and name of the person </br>
```Face.add_face("Person's Name","Path to the Person's image file")```

- If the face was added successfully it displays</br>
```Face Added```

### Generating CSV file 
#### For a particular date
- Import the ```Attendance``` class from ```attendance``` module</br>
```from faceattend.attendance import Attendance```
- Now use ```Attendance``` class's ```generate_csv_date()``` function
```Attendance.generate_csv_date("sample_date")```
#### For a particular employee
- Use ```Attendance``` class's ```generate_csv_emp()``` function
```Attendance.generate_csv_date("emp_id")```

#### If CSV file was generated it displays
```CSV file generated!```



## How to run?
- Import the ```detect_face()``` function from the ```detect``` module</br>
```from faceattend.detect import detect_face```
- Then just call the ```detect_face()``` function</br>
```detect_face()```
