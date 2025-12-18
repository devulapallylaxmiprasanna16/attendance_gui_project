import tkinter as tk
from tkinter import messagebox, filedialog
import os

STUDENT_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"


def load_students():
    students = {}
    with open(STUDENT_FILE, "r") as f:
        for line in f:
            roll, name = line.strip().split(",")
            students[roll] = name
    return students


students = load_students()


def auto_fill_name(event):
    roll = roll_entry.get()
    name_entry.delete(0, tk.END)
    if roll in students:
        name_entry.insert(0, students[roll])


def browse_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, path)


def submit_absence():
    date = date_entry.get()
    roll = roll_entry.get()
    name = name_entry.get()
    reason = reason_entry.get()
    pdf = pdf_entry.get()

    if not date or not roll or not reason:
        messagebox.showerror("Error", "Date, Roll No and Reason are mandatory")
        return

    if roll not in students:
        messagebox.showerror("Error", "Invalid Roll Number")
        return

    with open(ATTENDANCE_FILE, "a") as f:
        f.write(f"{date},{roll},{name},{reason},{pdf}\n")

    messagebox.showinfo("Submitted", "Absence submitted successfully")

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    reason_entry.delete(0, tk.END)
    pdf_entry.delete(0, tk.END)

def view_absentees():
    date = view_date_entry.get().strip()
    result_box.delete(1.0, tk.END)
    found = False

    if not os.path.exists(ATTENDANCE_FILE):
        result_box.insert(tk.END, "No records found.")
        return

    with open(ATTENDANCE_FILE, "r") as f:
        lines = f.readlines()[1:]  # SKIP HEADER

        for line in lines:
            if not line.strip():
                continue

            d, roll, name, reason, pdf = line.strip().split(",")

            if d == date:
                found = True
                result_box.insert(
                    tk.END,
                    f"Roll No : {roll}\n"
                    f"Name    : {name}\n"
                    f"Reason  : {reason}\n"
                    f"PDF     : {pdf if pdf else 'Not Attached'}\n"
                    "------------------------\n"
                )

    if not found:
        result_box.insert(tk.END, "No absentees found for this date.")

# ---------- GUI ----------
root = tk.Tk()
root.title("Student Absence Submission - CSM A")
root.geometry("620x600")

tk.Label(root, text="Student Absence Submission", font=("Arial", 15, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(frame, width=25)
date_entry.grid(row=0, column=1)

tk.Label(frame, text="Roll Number:").grid(row=1, column=0, sticky="w")
roll_entry = tk.Entry(frame, width=25)
roll_entry.grid(row=1, column=1)
roll_entry.bind("<KeyRelease>", auto_fill_name)

tk.Label(frame, text="Student Name:").grid(row=2, column=0, sticky="w")
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=2, column=1)

tk.Label(frame, text="Reason for Absence:").grid(row=3, column=0, sticky="w")
reason_entry = tk.Entry(frame, width=25)
reason_entry.grid(row=3, column=1)

tk.Label(frame, text="Attach PDF (optional):").grid(row=4, column=0, sticky="w")
pdf_entry = tk.Entry(frame, width=25)
pdf_entry.grid(row=4, column=1)
tk.Button(frame, text="Browse", command=browse_pdf).grid(row=4, column=2)

tk.Button(root, text="Submit Absence", bg="green", fg="white", command=submit_absence).pack(pady=10)

# ---------- Mentor View ----------
tk.Label(root, text="Mentor View (Read Only)", font=("Arial", 14, "bold")).pack(pady=10)

view_frame = tk.Frame(root)
view_frame.pack()

tk.Label(view_frame, text="Select Date:").grid(row=0, column=0)
view_date_entry = tk.Entry(view_frame, width=20)
view_date_entry.grid(row=0, column=1)
tk.Button(view_frame, text="View Absentees", command=view_absentees).grid(row=0, column=2)

result_box = tk.Text(root, width=72, height=12)
result_box.pack(pady=10)

# ---------- Init ----------
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w") as f:
        f.write("date,rollno,name,reason,pdf_path\n")

root.mainloop()
