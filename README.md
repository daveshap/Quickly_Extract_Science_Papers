# Quickly_Extract_Science_Papers

Scientific papers are coming out TOO DAMN FAST so we need a way to very quickly extract useful information.


## EXECUTIVE SUMMARY

This repository contains Python scripts that automate the process of generating reports from PDF files using OpenAI's
GPT-4 model. The scripts extract text from PDF files, send the text to the GPT-4 model for processing, and save the
generated reports as text files. The scripts also include functionality to render the generated reports as an HTML
document for easy viewing.

## SETUP

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt` in your terminal.
3. Obtain an API key from OpenAI and save it in a file named `key_openai.txt` in the root directory of the repository.
4. Place the PDF files you want to generate reports from in the `input/` directory.

## USAGE

1. Run the `generate_multiple_reports.py` script to generate reports from the PDF files in the `input/` directory. The
generated reports will be saved as text files in the `output/` directory.
2. Run the `render_report.py` script to render the generated reports as an HTML document. The HTML document will be
saved as `report.html` in the root directory of the repository.

## NOTE

The scripts are designed to handle errors and retries when communicating with the OpenAI API. If the API returns an
error due to the maximum context length being exceeded, the scripts will automatically trim the oldest message and retry
the API call. If the API returns any other type of error, the scripts will retry the API call after a delay, with the
delay increasing exponentially for each consecutive error. If the API returns errors for seven consecutive attempts, the
scripts will stop and exit.
