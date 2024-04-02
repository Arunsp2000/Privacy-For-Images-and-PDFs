# imports
import re
import spacy
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import pytesseract
import os
import fitz
from faker import Faker

# Redaction Class
class Redaction:

    # Constructor which takes two params: onlyImages for working with only images(default is PDFs) and morph if you want to change the contents instead of redacting
    def __init__(self, onlyImages = 0, morph = 0, useAsApi = 0) -> None:
        self.nlp = spacy.load("en_core_web_md")
        self.fake = Faker()
        if(useAsApi == 0):
            self.inputPdf = "input.pdf"
            self.morphedPdf = "morphed.pdf"
            self.tempFolder = "tempImages" 
            self.outputFolder = "outputFolder"
            self.pages = []
            if morph == 0:
                self.images = []
                if(onlyImages == 0):
                    self.deleteContents(self.tempFolder)
                    self.pdfToImages()
                
                self.deleteContents(self.outputFolder)

                self.redact()
                if(onlyImages == 0):
                    self.deleteContents(self.tempFolder) 
            else:
                self.deleteContents(self.outputFolder)
                self.morph()

    # Deletes contents in a folder
    def deleteContents(self, outputFolder):
        if os.path.exists(outputFolder):
            for fileName in os.listdir(outputFolder):
                filePath = os.path.join(outputFolder, fileName)
                os.remove(filePath)
        else:
            os.makedirs(outputFolder)

    # Converts PDF to Images
    def pdfToImages(self):
        images = convert_from_path(self.inputPdf)
        for i, image in enumerate(images):
            imagePath = f"{self.tempFolder}/page_{i + 1}.png"
            image.save(imagePath, 'PNG')
        
    # Converts Image to a dictionary which contains text and its respective locations
    def imageData(self, imagepath):
        image = Image.open(imagepath)
        self.images.append(image)
        page = pytesseract.image_to_data(image, output_type="dict")
        return page

    # Finds the coordinates of particular text boxes
    def findCoordinate(self, pii, data, boundingBox):
        for val in pii:
            for idx in range(len(data["text"])):
                i = data["text"][idx].strip()

                if i and val in i:
                    x, y, w, h = (
                        data["left"][idx],
                        data["top"][idx],
                        data["width"][idx],
                        data["height"][idx],
                    )
                    boundingBox.append((x, y, w, h))

    # Draws the black box
    def drawBlackBox(self, bbox, pageNum):
        draw = ImageDraw.Draw(self.images[pageNum])
        for box in bbox:
            x, y, w, h = box
            draw.rectangle([x, y, x + w, y + h], fill="black", outline="black")

    # Outputs the images to the folder      
    def output(self):
        for i, image in enumerate(self.images):
            imagePath = f"{self.outputFolder}/page_{i + 1}.png"
            image.save(imagePath, 'PNG')
    
    # Uses the converted images of a pdf
    # For each page we search for the sensitive information and its respective coordinates and draw the bounding boxes over them
    def redact(self):
        for filename in os.listdir(self.tempFolder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                imagePath = os.path.join(self.tempFolder, filename)
                self.pages.append(self.imageData(imagePath))

        for pageNum, page in enumerate(self.pages):
            bbox = []
            text =" ".join((line.strip() for line in page["text"] if line))
            pii1 = self.detectPiiWithSpacy(text)
            pii2 = self.detectPiiWithRegex(text)
            pii = pii1 + pii2
            newpii = []
            for i in pii:
                c = i.split(" ")
                newpii.extend(c)
            
            pii = newpii
            self.findCoordinate(pii, page, bbox)
            self.drawBlackBox(bbox, pageNum)
        
        self.output()
    
    # Changes the details present in the text by morphing the sensitive details(Could be used if users just want the content and not the nouns)
    def morph(self):
        pdfDoc = fitz.open(self.inputPdf)
        for pageNum in range(pdfDoc.page_count):
            page = pdfDoc[pageNum]

            text = page.get_text()
            text = self.replacePiiWithSpacy(text)
            text = self.replacePiiWithRegex(text)
            fileName = self.outputFolder + "/" + "page_" + str(pageNum+1) + ".txt"
            with open(fileName, 'w') as file:
                file.write(text)


    # Replacing of entities such as people names and geographical locations with certain values
    def replacePiiWithSpacy(self, text):
        doc = self.nlp(text)
        pii_entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "LOC"]:
                pii_entities.append((ent.text, ent.label_))
        for val, label in pii_entities:
            if label == "PERSON":
                vals = val.split(" ")
                name = self.fake.name()
                text = re.sub(val, name, text)
                for v in vals:
                    text = re.sub(v, name, text)

            else:
                text = re.sub(val, self.fake.city(), text)
        return text
    
    # Replacing of phone numbers, country code, email, ssn and zip codes with certain values.
    def replacePiiWithRegex(self, text):
        phone_number_pattern = r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        country_code_pattern = r'\+\d{1,4}[-.\s]?'
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ssn_pattern = r'\d{3}[-.\s]?\d{2}[-.\s]?\d{4}'
        zipcode_pattern = r'\d{5}'

        text = re.sub(phone_number_pattern, self.fake.phone_number(), text)
        text = re.sub(email_pattern, self.fake.email(), text)
        text = re.sub(ssn_pattern, self.fake.ssn(), text)
        text = re.sub(country_code_pattern,"", text)
        text = re.sub(zipcode_pattern, self.fake.zipcode(), text)

        return text

    # Detection of entities such as people names and geographical locations.
    def detectPiiWithSpacy(self, text):
        doc = self.nlp(text)
        pii_entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "LOC"]:
                pii_entities.append((ent.text, ent.label_))
        
        return [x[0] for x in pii_entities]

    # Detection of phone numbers, country code, email, ssn and zip codes.
    def detectPiiWithRegex(self, text):
        phone_number_pattern = r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        country_code_pattern = r'\+\d{1,4}[-.\s]?'
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ssn_pattern = r'\d{3}[-.\s]?\d{2}[-.\s]?\d{4}'
        zipcode_pattern = r'\d{5}'
        
        phone_numbers = re.findall(phone_number_pattern, text)
        email_addresses = re.findall(email_pattern, text)
        ssn_numbers = re.findall(ssn_pattern, text)
        country_code = re.findall(country_code_pattern, text)
        zip_code = re.findall(zipcode_pattern, text)

        pii_entities = phone_numbers + email_addresses + ssn_numbers + country_code + zip_code

        return pii_entities


# Main function call

# Call Redaction(morph = 1) if you want morphed values in text files
# Call Redaction() if you want to redact the PDF
# Call Redaction(onlyImages = 1) if you want to redact images directly(make sure to place the images in tempImages before this)
# Call Redaction(useAsApi = 1) if you want to use it as an API

if __name__ == "__main__":
    redact = Redaction()
