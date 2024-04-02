<h1 align="center">
    PDF Anonymizer
  </a>
</h1>

- ### Before Installation


    1. Clone the repository

    ```
    git clone https://github.ncsu.edu/kgala2/Privacy_20_2023
    ```

    2. In the folder PDF Redaction place your PDF which you want to be redacted or morphed and rename it as input.pdf. A sample input.pdf has been provided as well.

  	3. If you want to redact images directly, place the images in the tempImages folder. Also, make sure to set line 197 of ```redaction.py``` as Redaction(onlyImages = 1) 

    4. If you want to morph instead of redacting the images, set line 197 of ```redaction.py``` as Redaction(morph=1) 

    5. If you want to use the redaction class as an API please do by setting Redaction(useAsApi=1)

    6. Make sure to add the Poppler bin to the environment path. Download it from here https://github.com/oschwartz10612/poppler-windows/releases.

    7. Make sure to add the tesseract.exe to the environment variables. Download it from here https://github.com/UB-Mannheim/tesseract/wiki.
    
    *NOTE: Morphing gives text files while redacting gives images.*
    


- ### Installation and Run


    1. Create virtual environment

    ```
    python -m venv <name_of_virtualenv>
    ```

    2. Activate Python Virtual environment

    ```
    <name_of_virtualenv>\Scripts\activate.bat for Windows users.
    source <name_of_virtualenv>/bin/activate for linux users.
    ```

  	3. Enter the correct folder

    ```
    cd '.\PDF Redaction\' 
    ```

    4. Install dependencies

    ```
    pip install -r requirements.txt
    ```
	
    5. Run the below command in the folder

    ```
    python .\redaction.py
    ```

    6. The output should be present in the outputFolder

    *Note: There is another file called redactOnlyPDF.py which can be run as ```python .\redactOnlyPDF.py``` if you want to run redaction on a PDF, but the issue here is it does not remove the underlying text.*


- ### How the evaluations were run

    1. First ```preprocessData.py``` was run on the ```validation.csv```(taken from https://www.kaggle.com/datasets/gowrishankarp/newspaper-text-summarization-cnn-dailymail). For simplicity only 2000 rows were taken from the dataset.

    2. This gave an ```output.csv``` file which contains two columns with the original text and modified text.

    3. The first 200 rows(```fake2.csv```) and the last 190 rows(```fake1.csv```) were taken from ```output.csv``` and run separately on a collab session.

    4. The code that was run is in ```Final.ipynb```.(Uses the bart summarizer along with co-sine similarity)

    5. The two outputs were joined and the similarities were stored in the ```similarities.csv```.(387 rows)

    6. The final evaluations are present in the ```Evaluations.ipynb``` file. It shows the descriptive features of the data.
