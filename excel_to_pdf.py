import os
import asyncio
import subprocess


def excel_to_pdf(event, context):
    excel_document_bytes = b'' # get the bytes from somewhere, like S3 or HTTP request

    # Download the Excel file from S3
    input_file_path = '/tmp/input.xlsx'
    output_file_path = '/tmp/output.pdf'

    with open(input_file_path, 'wb') as f:
        f.write(excel_document_bytes)

    # Convert the Excel file to PDF where each sheet is a page in the PDF
    # yes, we are using subprocess to run a python script that uses LibreOffice to convert the file
    # read the README.md to know more about the script
    result = subprocess.run(
        [f'/opt/libreoffice24.8/program/python', 'excel_to_pdf_runner.py'],
        capture_output=True,
        text=True
    )

    if not os.path.exists(output_file_path):
        return {
            'statusCode': 500,
            'body': 'Error converting Excel to PDF'
        }
    
    # The file is converted, you can read the file from path /temp/output.pdf
    # you can now upload it to S3 or do whatever you want with it
    # except from deleting it, that will be waste of resources you dumb dumb

    # Clean up temporary files
    os.remove(input_file_path)
    os.remove(output_file_path)

    # Return success response
    return {
        'statusCode': 200,
        'body': 'File converted and uploaded successfully'
    }


def handler(event, context):
    try:
        excel_to_pdf(event, context)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
