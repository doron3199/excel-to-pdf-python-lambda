# This code was generated with the help of OpenAI's ChatGPT.

import sys
libreoffice_py_path = '/opt/libreoffice24.8/program'  # Adjust based on your Docker image
if libreoffice_py_path not in sys.path:
    sys.path.append(libreoffice_py_path)
import uno
from com.sun.star.beans import PropertyValue
import subprocess
import os
from time import sleep


def convert_excel_to_pdf():  
    input_file_path = '/tmp/input.xlsx'
    output_file_path = '/tmp/output.pdf'

    # Start LibreOffice in headless mode
    soffice_process = subprocess.Popen([
        f'{libreoffice_py_path}/soffice',
        '--headless',
        '--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager'
    ])

    # Wait for LibreOffice to start
    max_retries = 30
    for _ in range(max_retries):
        try:
            # Try to connect to the running LibreOffice instance
            local_ctx = uno.getComponentContext()
            resolver = local_ctx.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_ctx)
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            smgr = ctx.ServiceManager
            break
        except Exception as e:
            sleep(1)
    else:
        # If LibreOffice did not start within the max retries, terminate the process and raise an error
        soffice_process.terminate()
        soffice_process.wait()
        raise RuntimeError("LibreOffice did not start in time")

    document = None
    try:
        # Convert system paths to file URLs
        input_url = uno.systemPathToFileUrl(os.path.abspath(input_file_path))
        output_url = uno.systemPathToFileUrl(os.path.abspath(output_file_path))

        # Create the UNO component context
        local_ctx = uno.getComponentContext()

        # Create the UnoUrlResolver
        resolver = local_ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_ctx)

        # Connect to the running LibreOffice instance
        ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

        smgr = ctx.ServiceManager

        # Create the Desktop instance
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

        # Open the .xlsx document
        properties = (
            PropertyValue("Hidden", 0, True, 0),
        )
        document = desktop.loadComponentFromURL(input_url, "_blank", 0, properties)

        if not document:
            print({
                'statusCode': 500,
                'body': 'Failed to open document.'
            })

        # Ensure the document is a spreadsheet
        if not document.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            print({
                'statusCode': 400,
                'body': 'The document is not a spreadsheet.'
            })

        # Access the sheets
        sheets = document.getSheets()
        sheet_names = sheets.getElementNames()

        # Adjust page settings for each sheet
        for sheet_name in sheet_names:
            sheet = sheets.getByName(sheet_name)
            page_props = sheet.getPropertyValue('PageStyle')
            style_family = document.getStyleFamilies().getByName('PageStyles')
            page_style = style_family.getByName(page_props)

            # Set scaling to fit to one page both horizontally and vertically
            page_style.setPropertyValue('ScaleToPagesX', 1)
            page_style.setPropertyValue('ScaleToPagesY', 1)

        # Prepare PDF export properties
        pdf_properties = (
            PropertyValue("FilterName", 0, "calc_pdf_Export", 0),
            PropertyValue("FilterData", 0, uno.Any("[]com.sun.star.beans.PropertyValue", ()), 0),
        )

        # Export to PDF
        document.storeToURL(output_url, pdf_properties)

    finally:
        # Close the document
        if document:
            document.close(True)
        # Terminate LibreOffice process
        soffice_process.terminate()
        soffice_process.wait()

    print({
        'statusCode': 200,
        'body': 'File converted and uploaded successfully'
    })



if __name__ == '__main__':
    convert_excel_to_pdf()
    