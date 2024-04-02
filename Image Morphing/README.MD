<h1 align="center">
    Image Face Morpher
  </a>
</h1>

- ### Before Installation

    1. Clone the repository

    ```
    git clone https://github.ncsu.edu/kgala2/Privacy_20_2023
    ```


    2. Create virtual environment

    ```
    python -m venv <name_of_virtualenv>
    ```

    3. Activate Python Virtual environment

    ```
    <name_of_virtualenv>\Scripts\activate.bat for Windows users.
    source <name_of_virtualenv>/bin/activate for linux users.
    ```

  	4. Enter the correct folder

    ```
    cd '.\Image Morphing\' 
    ```

    5. Also in the above folder add ```shape_predictor_68_face_landmarks.dat```. Download it from https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat.

    6. In the folder Image Morphing place your image which you want to be morphed and rename it as pic1.jpg. Add another image which you want to morph as pic2.jpg.

    7. Change the alpha value to whatever value suits you. Alpha ranges from 0 to 1 and as alpha reaches 1, the more close the warped image is to pic2.jpg. As alpha decreases to 0, the more close the warped image is to pic1.jpg.

    8. Make sure you have dlib and open cv installed. Please check this https://geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/ for downloading dlib.
	
    9. Install opencv using ```pip install opencv-python```.

    10. Install imutils using ```pip install imutils```.

    11. Install numpy using ```pip install numpy```.

    


- ### Installation and Run


    ```
	
    1. Run the below command in the folder

    python .\morph.py
    ```


- ### References

The methodology behind the above code is https://learnopencv.com/face-morph-using-opencv-cpp-python/. 
