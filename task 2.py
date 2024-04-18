import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os

HOST = '192.168.54.212'  
PORT = 65432

class FileSharingApp:
    def __init__(self, master):
        self.master = master
        master.title("File Sharing App")

        
        self.file_path = tk.StringVar()
        self.file_label = tk.Label(master, text="Selected File:")
        self.file_label.pack()
        self.file_entry = tk.Entry(master, textvariable=self.file_path, state='disabled')
        self.file_entry.pack()
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()
        self.download_button = tk.Button(master, text="Download", command=self.download_file, state='disabled')
        self.download_button.pack()

        
        self.share_button = tk.Button(master, text="Share", command=self.share_file)
        self.share_button.pack()

        self.delete_button = tk.Button(master, text="Delete", command=self.delete_file, state='normal')
        self.delete_button.pack()

    def browse_file(self):
        self.file_path.set(filedialog.askopenfilename())
        self.download_button.config(state='normal')  

    def download_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file to download.")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))

                
                request_msg = f"DOWNLOAD,{os.path.basename(file_path)}".encode()
                s.sendall(request_msg)

                
                confirmation = s.recv(1024).decode()
                if confirmation != 'OK':
                    messagebox.showerror("Error", "Download not confirmed by target device.")
                    return

                
                file_size = int(s.recv(1024).decode())

                
                save_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(file_path)[1])
                if not save_path:
                    return

                with open(save_path, 'wb') as f:
                    received_bytes = 0
                    while received_bytes < file_size:
                        data = s.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        received_bytes += len(data)

                messagebox.showinfo("Success", f"File downloaded to: {save_path}")

        except ConnectionRefusedError:
            messagebox.showerror("Error", "Connection refused. Make sure the target device is running the app and on the same network.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found on the target device.")
        except OSError:  
            messagebox.showerror("Error", "Error saving downloaded file.")

    def share_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file to share.")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                file_size = os.path.getsize(file_path)
                s.sendall(f"{file_size},{os.path.basename(file_path)}".encode())

                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        s.sendall(data)

                messagebox.showinfo("Success", "File shared successfully!")
                self.delete_button.config(state='disabled')  

        except ConnectionRefusedError:
            messagebox.showerror("Error", "Connection refused. Make sure the target device is running the app and on the same network.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")

    def delete_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file to delete.")
            return
        confirmation = messagebox.askquestion("Confirm", "Are you sure you want to delete this file?")
        if confirmation == 'yes':
            try:
                os.remove(file_path)
                self.file_path.set('')  
                self.delete_button.config(state='disabled')  
                messagebox.showinfo("Success", "File deleted successfully!")
            except PermissionError:
                messagebox.showerror("Error", "You don't have permission to delete this file.")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")

      

if __name__ == '__main__':
    root = tk.Tk()
    app = FileSharingApp(root)
    root.mainloop()
