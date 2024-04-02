from tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas
import re

def validate_data(name, id_string, email, phone_no, clgname):
  error_message = ""

  if not name:
    error_message += "Name cannot be empty\n"
  def isValid(aicte):
    Pattern = re.compile("(S)(T)(U)?[6 & 5][0-9|a-z]{22}")
    return Pattern.match(aicte)
  aicte=id_string
  if not (isValid(aicte)):  
    
    error_message += "Enter valid AICTE id\n"
  if not email or "@" not in email:
    error_message += "Invalid email format\n"
  def isValid(s):
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)
  s = phone_no
  if not (isValid(s)):  
    error_message += "Enter valid phone number\n"
  def validate_college_name(collagename):
    
    pattern = r"^[A-Za-z '.,-]+$"
        
    if re.match(pattern, collagename):
        return True
    else:
        return False

  collagename= clgname
  if not validate_college_name(clgname):
    
  
    error_message += "Enter valid college name\n"

  return error_message  

def generate_pdf(name, id_string, email, phone_no, college_name):
  
  pdf = canvas.Canvas("student_registration.pdf")
  pdf.setFont("Helvetica", 12)

  pdf.drawString(100, 700, "Student Registration Details:")
  pdf.drawString(100, 680, f"Name: {name}")
  pdf.drawString(100, 660, f"aicte id:{id_string}")
  pdf.drawString(100, 640, f"Email: {email}")
  pdf.drawString(100, 620, f"phone_no: {phone_no}")
  pdf.drawString(100, 600, f"college_name : {college_name}")

  pdf.save()

  messagebox.showinfo("Success", "PDF report generated successfully!")

root = Tk()
root.title("Student Registration Form")

name_label = Label(root, text="Name:")
name_label.pack()

name_entry = Entry(root)
name_entry.pack()

id_string_label = Label(root, text="AICTE id:")
id_string_label.pack()

id_string_entry = Entry(root)
id_string_entry.pack()

email_label = Label(root, text="Email:")
email_label.pack()

email_entry = Entry(root)
email_entry.pack()

phone_no_label = Label(root, text="Phone no:")
phone_no_label.pack()

phone_no_entry = Entry(root)
phone_no_entry.pack()

college_name_label = Label(root, text="College name:")
college_name_label.pack()

college_name_entry = Entry(root)
college_name_entry.pack()


def submit_form():
  name = name_entry.get()
  id_string = id_string_entry.get()
  email = email_entry.get()
  phone_no = phone_no_entry.get()
  college_name = college_name_entry.get()

  error_message = validate_data(name, id_string, email, phone_no, college_name)
  if error_message:
    messagebox.showerror("Error", error_message)
    return

  generate_pdf(name, id_string, email, phone_no, college_name)

submit_button = Button(root, text="Submit", command=submit_form)
submit_button.pack()

root.mainloop()
