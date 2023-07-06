from bs4 import BeautifulSoup
import os

# Create a new BeautifulSoup object and define the basic structure of the HTML document
soup = BeautifulSoup("<html><head><title>Arxiv Paper Reports</title></head><body></body></html>", "html.parser")

# Get a list of all text files in the output directory
text_files = [f for f in os.listdir('output/') if f.endswith('.txt')]

# For each text file
for text_file in text_files:
    # Open the file and read its content
    with open('output/' + text_file, 'r') as file:
        content = file.read()

    # Create a new section in the HTML document for this file
    section = soup.new_tag('section')

    # Add a header with the name of the file (without the .txt extension)
    header = soup.new_tag('h1')
    header.string = text_file[:-4]
    section.append(header)

    # Split the content into Q&A pairs and add them to the section
    pairs = content.split('\n\n\n\n')
    for pair in pairs:
        # Split the pair into question and answer
        question, answer = pair.split('\n\n', 1)

        # Add the question and answer to the section
        q_tag = soup.new_tag('p')
        q_tag.string = question
        section.append(q_tag)

        a_tag = soup.new_tag('p')
        a_tag.string = answer
        section.append(a_tag)

    # Add the section to the body of the HTML document
    soup.body.append(section)

# Write the HTML document to a file
with open('report.html', 'w') as file:
    file.write(str(soup.prettify()))