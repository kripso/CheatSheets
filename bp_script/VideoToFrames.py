import cv2
import csv
import random
from PIL import Image, ImageDraw
from cv2 import data

# TODO: calculate Random Frames 10%


class VideoExtractor:
    def __init__(self, width=1280, height=1280) -> None:
        self.width = width
        self.height = height

    def retrieveFrames(self, frames, path='exports\\001\\world.mp4'):
        exportPath = 'exports\\001\\extracted\\frames'
        video = cv2.VideoCapture(path)
        success, image = video.read()

        aFrame = 0
        while success:
            if aFrame in frames:
                cv2.imwrite(exportPath+"\\frame%d.jpg" % aFrame, image)
            success, image = video.read()
            aFrame += 1

    def putFixationOnFrame(self):
        # width = 1280
        # height = 720
        # x = 0.44
        # y = 1-0.32
        # xCoordinate = width*x
        # yCoordinate = height*y

        # image = Image.open("exports\\001Extracted\\frame1.jpg")
        # draw = ImageDraw.Draw(image)
        # draw.ellipse((width*x-7, height*y-7, width*x+7, height*y+7), fill="red")
        # image.save("exports\\001Extracted\\frame.jpg", quality=95)
        pass


class CSVExtractor:
    def __init__(self) -> None:
        self.columns = []
        self.data = []

    def readGasePositions(self, path="exports\\001\\gaze_positions.csv"):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    self.columns.append(row)
                    print(f'Column names are {", ".join(row)}')
                else:
                    self.data.append(row)
                line_count += 1

    def writeGazePositions(self, frames):
        exportPath = 'exports\\001\\extracted'
        rows = []

        for index, gazePosition in enumerate(self.data):
            if int(gazePosition[1]) in frames:
                rows.append(index)

        with open(exportPath+'\\gaze_positions.csv', mode='w', newline='') as gaze_positions:
            gaze_positions_writer = csv.writer(gaze_positions, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            gaze_positions_writer.writerow(self.columns[0])

            for index in rows:
                gaze_positions_writer.writerow(self.data[index])


if __name__ == '__main__':
    csvExtractor = CSVExtractor()
    csvExtractor.readGasePositions()

    numberOfFrames = 10
    frames = random.sample(range(0, int(csvExtractor.data[len(csvExtractor.data)-1][1])+1), numberOfFrames)

    VideoExtractor().retrieveFrames(frames)
    csvExtractor.writeGazePositions(frames)
