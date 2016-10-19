# import the necessary packages
import cv2
import utility.util as util
import preprocessing.extract_frame as ppf
import classifier.classify as clf
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

frame_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset/mp4_temp_frame"
search_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset"

class UI_class:
    def __init__(self, master, search_path, frame_storing_path):
        self.search_path = search_path
        self.master = master
        self.frame_storing_path = frame_storing_path
        topframe = Frame(self.master, padx=240)
        topframe.pack()

        # initialize query_img_frame
        self.query_img_frame = 0

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose a video ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Estimate venue ", command=self.show_venue_category)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()


    def browse_query_img(self):
        if (self.query_img_frame != 0):
            self.query_img_frame.destroy()

        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose a Video File').name

        # clear temp folder storage
        temp_frames = os.listdir(self.frame_storing_path)
        if len(temp_frames) > 0:
            for frames in temp_frames:
                os.remove(self.frame_storing_path + "/" + frames)
        
        # extract vid frames to temp storage
        ppf.frameExtract(self.frame_storing_path, self.filename)
        temp_frames = os.listdir(self.frame_storing_path)

        self.frames = []
        for frame in temp_frames:
            if frame.endswith(".jpg"):
                self.frames.append(self.frame_storing_path + "/" + frame)

        COLUMNS = len(self.frames)
        self.columns = COLUMNS
        image_count = 0

        if COLUMNS == 0:
            self.frames.append("none.png")
            print("Please extract the key frames for the selected video first!!!")
            COLUMNS = 1

        for frame in self.frames:

            r, c = divmod(image_count, COLUMNS)
            try:
                im = Image.open(frame)
                resized = im.resize((100, 100), Image.ANTIALIAS)
                tkimage = ImageTk.PhotoImage(resized)

                myvar = Label(self.query_img_frame, image=tkimage)
                myvar.image = tkimage
                myvar.grid(row=r, column=c)

                image_count += 1
                self.lastR = r
                self.lastC = c
            except Exception, e:
                continue

        self.query_img_frame.mainloop()


    def show_venue_category(self):
        if self.columns == 0:
            print("Please extract the key frames for the selected video first!!!")
        else:
            # Please note that, you need to write your own classifier to estimate the venue category to show blow.
            venue_list = util.get_venue_list(self.search_path)

            # classify video in self.filename, returns an integer
            
            # for each feature, get an array

            # concatenate each feature and send it for classification

            class_value = 1

            # with integer, get venue text
            venue_text = venue_list[class_value]

            venue_img = Image.open("venue_background.jpg")
            draw = ImageDraw.Draw(venue_img)

            font = ImageFont.truetype("/Library/Fonts/Arial.ttf",size=66)

            draw.text((50,50), venue_text, (0, 0, 0), font=font)

            resized = venue_img.resize((100, 100), Image.ANTIALIAS)
            tkimage =ImageTk.PhotoImage(resized)

            myvar = Label(self.query_img_frame, image=tkimage)
            myvar.image= tkimage
            myvar.grid(row=self.lastR, column=self.lastC+1)

        self.query_img_frame.mainloop()


root = Tk()
window = UI_class(root,search_path=search_path, frame_storing_path=frame_path)