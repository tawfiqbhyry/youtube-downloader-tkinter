import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Progressbar
from pytube import YouTube, Playlist
from threading import Thread
from functools import partial


resolutions = ["144p", "240p", "360p",
               "480p", "720p", "1080p", "1440p", "2160p"]


def createwidgits():
    # creating a button
    link_label = Label(root, text="Paste URL: ", bg="#999999")
    # placing the label
    link_label.grid(row=1, column=0, pady=10, padx=10)

    # creating a entry point
    root.link_text = Entry(root, width=60, textvariable=video_link)
    # placing the point
    root.link_text.grid(row=1, column=1, pady=10, padx=10)

    # creating a destination label
    destination_label = Label(root, text="Destination: ", bg="#999999")
    # placing the label
    destination_label.grid(row=2, column=0, pady=10, padx=10)

    global pb, video_label, download_but
    pb = Progressbar(
        root,
        orient="horizontal",
        mode="determinate",
        length=280,
        value="0",
        style="text.Horizontal.TProgressbar",
    )
    pb.grid(row=4, column=1, pady=10, padx=10)

    video_label = Label(
        root, text="saving the videos.", bg="#999999", justify="center", wraplength=400
    )
    # placing the label
    video_label.grid(row=5, column=1, pady=10, padx=10)
    # creating a destination box
    root.destination_label = Entry(root, width=60, textvariable=Download_path)
    # placing the box
    root.destination_label.grid(row=2, column=1, pady=10, padx=10)

    # create a browse button
    browse_but = Button(root, text="Browse", command=browse,
                        width=10, bg="#ffffff")
    # place the button
    browse_but.grid(row=3, column=2, pady=10, padx=10)

    # create a download button
    download_but = Button(
        root, text="Download", command=download_video, width=15, bg="#ff0000"
    )
    # place the button
    download_but.grid(row=3, column=1, pady=3, padx=3)


# define browse button function
def browse():
    # set directory
    downlaod_dir = filedialog.askdirectory(initialdir="Downlaod path")
    Download_path.set(downlaod_dir)


def on_closing():
    root.destroy()
    sys.exit()


def progress_function(chunk, file_handle, bytes_remaining):
    global size, style
    remaining = (100 * bytes_remaining) / size
    step = 100 - int(remaining)
    pb.config(value=step)
    style.configure("text.Horizontal.TProgressbar", text="{:g} %".format(step))


# error detect and save the reason and video link with the counter of the video in playlist **youtube**
# label the downloading video **youtube**
# input any link whether playlist or video **youtube**
# add channel option
# add resolution option **youtube**
def download_video():
    global video_label, resolutions_menu

    def handle_resolution(res):
        global resolution_of_video
        resolution_of_video = res

    # download playlist function
    def downPlay(url):
        global size
        pb.config(value=0)
        style.configure("text.Horizontal.TProgressbar", text="0 %")
        try:
            os.listdir(Download_path.get())
            pl = Playlist(url)
            try:
                folder = (
                    Download_path.get() + "//" + "".join(e for e in pl.title if e.isalnum()
                                                         or e in " |*-+=)(#@!")
                )
                counter = 1
                ans = messagebox.askquestion(
                    "resolution of download",
                    "do you want to download this playlist on high resolution? answer yes if you need that and no to download on average speed",
                )
                foldername = (
                    "".join(e for e in pl.title if e.isalnum() or e in " |*-+=)(#@!"))

                if foldername not in os.listdir(
                    Download_path.get()
                ):
                    os.mkdir(folder)
                for video in pl.videos:
                    try:
                        pb.config(value=0)
                        video_label.config(
                            text="downloading: {}".format(video.title))
                        style.configure(
                            "text.Horizontal.TProgressbar", text="0 %")
                        video.register_on_progress_callback(progress_function)
                        if ans == "yes":
                            size = video.streams.get_highest_resolution().filesize
                            get_stream = video.streams.get_highest_resolution()
                            get_stream.download(
                                folder, filename="#{} - {}.mp4".format(counter, "".join(
                                    e for e in video.title if e.isalnum() or e in "- #"))
                            )
                        elif ans == "no":
                            all_res = video.streams.all()
                            available_res = []
                            video_resolution_final = ""
                            for res in all_res:
                                try:
                                    video.streams.get_by_resolution(
                                        res.resolution).filesize
                                    available_res.append(res.resolution)
                                except:
                                    pass
                            if len(available_res) < 1:
                                with open(
                                    "{}//errors.txt".format(folder), "a", encoding="utf-8"
                                ) as f:
                                    f.write(
                                        "count: {}\nvideo: {}\nerror: {}\nvideo url: {}\n{}\n".format(
                                            counter, video.title, error, video.watch_url, "*" * 50
                                        )
                                    )
                            elif len(available_res) % 2 == 0:
                                video_resolution_final = available_res[
                                    len((available_res) / 2)
                                ]
                            elif len(available_res) % 2 == 1:
                                video_resolution_final = available_res[
                                    int(len(available_res) / 2) + 1
                                ]
                            size = video.streams.get_by_resolution(
                                video_resolution_final
                            ).filesize
                            get_stream = video.streams.get_by_resolution(
                                video_resolution_final
                            )
                            get_stream.download(
                                folder, filename="#{} - {}.mp4".format(counter, "".join(
                                    e for e in video.title if e.isalnum() or e in "- #"))
                            )
                    except Exception as error:
                        if "main thread is not in main loop" in error:
                            sys.exit()
                        else:
                            with open(
                                "{}//errors.txt".format(folder), "a", encoding="utf-8"
                            ) as f:
                                f.write(
                                    "count: {}\nvideo: {}\nerror: {}\nvideo url: {}\n{}\n".format(
                                        counter, video.title, error, video.watch_url, "*" * 50
                                    )
                                )
                    counter += 1
                return True
            except Exception as e:
                if "main thread is not in main loop" in error:
                    sys.exit()
                else:
                    messagebox.showerror(
                        "Error downloading",
                        "an error occurred, because: {}".format(e),
                    )
                    return False
        except FileNotFoundError:
            messagebox.showerror("error", "enter a right folder path.")
            return False

    # download videos function
    def download_videos(url):
        global size, resolution_of_video
        folder = Download_path.get()
        try:
            os.listdir(folder)
            pb.config(value=0)
            style.configure("text.Horizontal.TProgressbar", text="0 %")
            video = YouTube(url)
            try:
                video_label.config(text="downloading: {}".format(video.title))
                video.register_on_progress_callback(progress_function)
                max_resolution = video.streams.get_highest_resolution().resolution
                indexOf_max_resolution = resolutions.index(max_resolution)
                resolutions_menu = Menu(root, tearoff=0)
                for i in range(indexOf_max_resolution + 1):
                    try:
                        video.streams.get_by_resolution(
                            resolution=resolutions[i]).filesize
                        resolutions_menu.add_command(
                            label=resolutions[i],
                            command=partial(handle_resolution, resolutions[i]),
                        )
                    except:
                        pass

                try:
                    resolutions_menu.tk_popup(200, 200)
                finally:
                    resolutions_menu.grab_release()
                try:
                    size = video.streams.get_by_resolution(
                        resolution=resolution_of_video
                    ).filesize
                    get_stream = video.streams.get_by_resolution(
                        resolution=resolution_of_video
                    )
                    get_stream.download(folder)
                    return True
                except AttributeError:
                    messagebox.showerror(
                        "Error", "This resolution is not available.")
                    return False
            except Exception as error:
                messagebox.showerror(
                    "Error downloading",
                    "the video: {}, with url: {}, couldn't be downloaded due to: {}".format(
                        video.title, url, error
                    ),
                )
                return False
        except FileNotFoundError:
            messagebox.showerror("error", "enter a right folder path.")
            return False

    # main check function
    def enable_disable(state):
        if state:
            download_but["state"] = "normal"
        else:
            download_but["state"] = "disabled"

    def main():
        url = video_link.get()
        checkPlayList = "/watch" in url and "list=" in url

        # check playlist
        if "/playlist?list=" in url:
            enable_disable(False)
            result = downPlay(url)
            if result:
                messagebox.showinfo(
                    "Playlist", "Your playlist was downloaded successfully"
                )
            enable_disable(True)

        # playlist or video in url
        elif checkPlayList:
            ans = messagebox.askquestion(
                "Playlist",
                "Do you want to download this playlist or only the video? answer yes for playlist or no for video",
            )
            if ans == "yes":
                enable_disable(False)
                result = downPlay(url)
                if result:
                    messagebox.showinfo(
                        "playlist downloaded",
                        "Your playlist is downloaded successfully",
                    )
                enable_disable(True)
            elif ans == "no":
                enable_disable(False)
                result = download_videos(url)
                if result:
                    messagebox.showinfo(
                        "video downloaded", "Your video is downloaded successfully"
                    )
                enable_disable(True)
            else:
                messagebox.showerror("Error", "Invalid choice. Try again!")

        # video check
        elif "/watch?v=" in url:
            enable_disable(False)
            result = download_videos(url)
            if result:
                messagebox.showinfo(
                    "video downloaded", "Your video is downloaded successfully"
                )
            enable_disable(True)

        # error in the url
        else:
            messagebox.showerror("Error", "Invalid URL")

    Thread(target=main).start()


# creating an instance
root = tk.Tk()
style = ttk.Style(root)
# size of the window
root.geometry("600x250")
root.resizable(False, False)
# name of the window
root.title("downloader")
# colors of the window
root.config(background="#999999")
style.layout(
    "text.Horizontal.TProgressbar",
    [
        (
            "Horizontal.Progressbar.trough",
            {
                "children": [
                    ("Horizontal.Progressbar.pbar", {
                     "side": "left", "sticky": "ns"})
                ],
                "sticky": "nswe",
            },
        ),
        ("Horizontal.Progressbar.label", {"sticky": ""}),
    ],
)

video_link = StringVar()
Download_path = StringVar()

createwidgits()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
