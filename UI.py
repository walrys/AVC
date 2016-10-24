# import the necessary packages
import cv2
import utility.util as util
import preprocessing.extract_frame as ppf
import featureextracting.concat_input as fe
import classifier.SVM as svm
import numpy as np
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

temp_path = "./temp"
search_path = "./data"

class UI_class:
    def __init__(self, master, search_path, temp_storing_path):
        self.search_path = search_path
        self.master = master
        self.temp_storing_path = temp_storing_path
        self.model = svm.create_model(self.search_path)
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
        temp_frames = os.listdir(self.temp_storing_path + "/jpg")
        if len(temp_frames) > 0:
            for frames in temp_frames:
                os.remove(self.temp_storing_path + "/jpg/" + frames)
        
        # extract vid frames to temp storage
        ppf.frameExtract(self.temp_storing_path + "/jpg", self.filename)
        temp_frames = os.listdir(self.temp_storing_path + "/jpg")

        
        self.frames = []
        for frame in temp_frames:
            if frame.endswith(".jpg"):
                self.frames.append(self.temp_storing_path + "/jpg/" + frame)
        
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

        # extract wav file to temp storage
        if os.name == 'posix':
            print "extracting audio files..."
            video_path = 'queries/'+os.path.basename(self.filename)
            audio_path = "temp/wav/"+os.path.basename(self.filename)[:-3]+'wav'
            os.system('python ./preprocessing/extract_audio.py '+video_path+' '+audio_path)
            print "extracting audio features..."
            os.system('python ./featureextracting/acoustic/audioprocessor.py '+audio_path)
        else:
            import preprocessing.extract_audio as ppa
            import featureextracting.acoustic.audioprocessor as ap
            print "extracting audio files..."
            #ppa.getAudioClip(self.filename,self.temp_storing_path + "/wav/" + self.filename[-23:-3] + 'wav')
            ppa.getAudioClip(self.filename,self.temp_storing_path + "/wav/"+os.path.basename(self.filename)[:-3]+'wav')
            # extract audio features into temp storage
            print "extracting audio features..."
            ap.extractQuery(self.temp_storing_path + "/wav/"+os.path.basename(self.filename)[:-3]+'wav')
            
        
        self.query_img_frame.mainloop()


    def show_venue_category(self):
        if self.columns == 0:
            print("Please extract the key frames for the selected video first!!!")
        else:
            # extract audio to temp folder
            # assuming audio has been extracted

            # concatenate each feature
            #fe.combine_features(temp_path + "/wav", temp_path + "/jpg", temp_path + "/npy")

            # load temp.npy
            X_test = np.load(temp_path + "/npy/test_ms_zeropad.npy")
            # send for classification
            class_value = svm.predict(self.search_path, self.model, X_test)

            venue_list = util.get_venue_list(self.search_path)

            # with integer, get venue text
            print class_value[0]
            venue_text = venue_list[class_value[0]]

            venue_img = Image.open("venue_background.jpg")
            draw = ImageDraw.Draw(venue_img)

            font = ImageFont.truetype("./Fonts/impact.ttf",size=66)

           # draw.text((50,50), venue_text, (0, 0, 0))
            draw.text((50,50), venue_text, (0, 0, 0), font=font)

            resized = venue_img.resize((100, 100), Image.ANTIALIAS)
            tkimage =ImageTk.PhotoImage(resized)

            myvar = Label(self.query_img_frame, image=tkimage)
            myvar.image= tkimage
            myvar.grid(row=self.lastR, column=self.lastC+1)

            # clean up
            output_items = os.listdir(temp_path + "/npy")
            for items in output_items:
                if "zeropad" in items:
                    continue
                else:
                    os.remove(temp_path + "/npy/" + items)

        self.query_img_frame.mainloop()


root = Tk()
window = UI_class(root,search_path=search_path, temp_storing_path=temp_path)