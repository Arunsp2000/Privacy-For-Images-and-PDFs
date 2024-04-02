# Imports
import re
import spacy
import fitz


# Model for english words
nlp = spacy.load("en_core_web_md")


# Redacting the PDF
# Takes an input pdf and output pdf as arguments
# Extracts the text from the PDF for each Page
# Searches the text for sensitive information
# Searches these instances and finds their coordinates in the PDF
# Draws the Rectangles over the PDF
def redact_pdf(input_pdf_path, output_pdf_path):
    
    pdf_document = fitz.open(input_pdf_path)
    coords = []
    for page in pdf_document:
        val = page.get_text()
        piiRegex = detect_pii_with_regex(val)
        piiSpacy = detect_pii_with_spacy(val)

        piiRegex = set(piiRegex)
        piiSpacy = set(piiSpacy)
        rect_options = {
            "width": 1,
            "color": (0, 0, 0),
            "fill": (0,0,0) 
        }
        pii = piiRegex | piiSpacy
        for redacted_text in pii:
            for redact_instance in page.search_for(redacted_text):
                coords.append(redact_instance)
                if not(page.is_wrapped):
                    page.wrap_contents()
                page.draw_rect(redact_instance, **rect_options)
    pdf_document.save(output_pdf_path)

    
    pdf_document.close()


# Detection of entities such as people names and geographical locations.
def detect_pii_with_spacy(text):
    doc = nlp(text)
    pii_entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "LOC"]:
            pii_entities.append((ent.text, ent.label_))
    
    return [x[0] for x in pii_entities]

# Detection of phone numbers, country code, email, ssn and zip codes.
def detect_pii_with_regex(text):
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


if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "redacted.pdf"
    redact_pdf(input_pdf, output_pdf)