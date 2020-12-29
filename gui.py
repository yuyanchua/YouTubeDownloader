import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from pathlib import Path


def widgets():
    link_label = Label(root,
                       text='YouTube link :', bg="#E8D579")
    link_label.grid(row=1, column=0, padx=5, pady=5)
    root.linkText = Entry(root, width=55, textvariable=video_link)
    root.linkText.grid(row=1, column=1, pady=5, padx=5, columnspan=2)

    destination_label = Label(root,
                              text='Destination :',
                              bg='#E8D579')
    destination_label.grid(row=2, column=1, pady=5, padx=5)
    bt_browse = Button(root,
                       text="Browse",
                       command=browse,
                       width=10,
                       bg="#05E8E0")
    bt_browse.grid(row=2, column=2,
                   padx=1, pady=1)

    bt_download = Button(root,
                         text='Download',
                         command=download,
                         width=20,
                         bg="#05E8E0")
    bt_download.grid(row=3,
                     column=1,
                     pady=3, padx=3)


def browse():
    download_dir = filedialog.askdirectory(initialdir=Path.cwd())

    download_path.set(download_dir)


def download():
    youtube_url = video_link.get()
    download_folder = download_path.get()

    messagebox.showinfo("Download", f"Download Video : {youtube_url} in {download_folder}")


root = tkinter.Tk()

root.geometry("600x120")
root.title = 'YouTube Video Downloader'
root.config(background="#000000")

video_link = StringVar()
download_path = StringVar()

widgets()
root.mainloop()
