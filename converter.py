from pypdf import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox
import os

pdf_path = ""
output_path = ""
num_of_validations = 0


def convert_validations(pdf_path, output_path, num_of_validations):
    ## Defining variables needed
    pageCount = 0
    pagesAdded = 0
    num_of_validations = int(num_of_validations)
    ## Assigning Reader and Writer
    pdf = PdfReader(pdf_path)
    writer = PdfWriter()
    ## Construct the file name (original download name + "-lottery" at the end)
    filename = os.path.basename(pdf_path)
    file = os.path.splitext(filename)
    filename = file[0] + "-lottery.pdf"
    ## How many pages
    print("amount of pages ", len(pdf.pages))
    ## For each page do this loop
    while pageCount < len(pdf.pages):
        print("On page ", pageCount+1)
        page = pdf.pages[pageCount]
        
        ## Defining height for validations
        height = page.mediabox.height
        while pagesAdded < num_of_validations or pagesAdded < 30:
            pagesAdded += 1
            ## Defining upper left and lower right hand corners of each validations
            page.mediabox.upper_left = [10+208*(pagesAdded%3), height-90-79*(pagesAdded%10)]
            page.mediabox.lower_right = [175+208*(pagesAdded%3), height-30-79*(pagesAdded%10)]

            ## Add newly defined "page" (validation) to the new pdf
            writer.add_page(page)
            print("Pages Added So Far ", pagesAdded)
        num_of_validations = num_of_validations - 30
        pageCount+= 1
    if (num_of_validations <= 0):
        print("Number of Validations: 0")
    else:
        print("Number of Validations: ", num_of_validations)
    ## Combining new pdf name to output_path
    final_output_path = output_path+"/"+filename
    ## Finish writing to pdf
    with open(final_output_path, "wb+") as f:
        writer.write(f)

##################################################################################
#
#
# MAKE SURE YOU PRINT WITH PAPER SIZE REGULAR 82.5 x 82.5 
# 
#                   DO NOT USE 
#           THE ROLL OR ROLL SHORT 82.5 x 82.5
#
#
##################################################################################
    
    

## Input path tkinter
def browse_input_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_input_pdf.delete(0, tk.END)
        entry_input_pdf.insert(0, file_path)

## Output path tkinter
def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(0, folder_path)

## Actions after hitting submit
def submit():
    pdf_path = entry_input_pdf.get()
    output_path = entry_output_folder.get()
    num_of_validations = entry_integer.get()
    
    if not pdf_path or not output_path or not num_of_validations:
        messagebox.showwarning("Missing Information", "Please provide all required inputs.")
        return

    # Testing to ensure correct paths and beginning conversion
    try:
        print(f"Input PDF: {pdf_path}")
        print(f"Output Folder: {output_path}")
        print(f"Integer Input: {num_of_validations}")
        convert_validations(pdf_path, output_path, num_of_validations)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer.")

# Create the main window
root = tk.Tk()
root.title("Validation Processor")

# Create and place the widgets
tk.Label(root, text="Input PDF File:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
entry_input_pdf = tk.Entry(root, width=50)
entry_input_pdf.grid(row=0, column=1, padx=10, pady=5)
btn_browse_pdf = tk.Button(root, text="Browse", command=browse_input_pdf)
btn_browse_pdf.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
entry_output_folder = tk.Entry(root, width=50)
entry_output_folder.grid(row=1, column=1, padx=10, pady=5)
btn_browse_folder = tk.Button(root, text="Browse", command=browse_output_folder)
btn_browse_folder.grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Number of Validations:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
entry_integer = tk.Entry(root, width=50)
entry_integer.grid(row=2, column=1, padx=10, pady=5)

btn_submit = tk.Button(root, text="Submit", command=submit)
btn_submit.grid(row=3, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()