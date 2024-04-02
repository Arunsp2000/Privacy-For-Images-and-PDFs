<h1 align="center">
    Image Anonymizer
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
    cd '.\Image Anonymization\' 
    ```

    5. In the folder Image Anonymization place your image that you want to be anonymized and rename is as 'pic1.jpg'.

    6. Install opencv using ```pip install opencv-python```.

    7. Install numpy using ```pip install numpy```.

    8. Install PIL using https://www.geeksforgeeks.org/how-to-install-pil-on-windows/.
    
  	9. Run either ```python gaussian.py``` or ```python laplace.py``` to get your results. The results are stored for multiple epsilon values in the same folder.


