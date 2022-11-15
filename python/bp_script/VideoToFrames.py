import cv2
import csv
import random
from PIL import Image, ImageDraw
from cv2 import data


class VideoExtractor:
    def __init__(self, width=1280, height=1280) -> None:
        self.width = width
        self.height = height

    def retrieveFrames(self, frames, path='exports\\000\\world.mp4'):
        exportPath = 'exports\\000\\extracted\\frames'
        video = cv2.VideoCapture(path)
        success, image = video.read()

        aFrame = 0
        while success:
            if aFrame in frames:
                cv2.imwrite(exportPath+"\\frame%d.jpg" % aFrame, image)
            success, image = video.read()
            aFrame += 1

    def putFixationOnFrame(self, frames):
        for frame in frames:
            framePath = 'exports\\000\\extracted\\frames\\frame%d.jpg' % frame
            gazeDataPath = 'exports\\000\\extracted\\gaze_positions%d.csv' % frame
            image = cv2.imread(framePath)
            height, width, _ = image.shape

            image = Image.open(framePath)
            draw = ImageDraw.Draw(image)
            with open(gazeDataPath) as gazeData:
                csv_reader = csv.reader(gazeData, delimiter=',')
                firstRow = True
                for row in csv_reader:
                    if firstRow:
                        firstRow = False
                        continue

                    norm_pos_x = float(row[3])
                    norm_pos_y = 1 - float(row[4])
                    xCoordinate = width*norm_pos_x
                    yCoordinate = height*norm_pos_y

                    draw.ellipse((xCoordinate-7, yCoordinate-7, xCoordinate+7, yCoordinate+7), fill="red")

            image.save(framePath[:-4]+'_plus_fixation.jpg', quality=100)


class CSVExtractor:
    def __init__(self) -> None:
        self.columns = []
        self.data = []

    def readGasePositions(self, path="exports\\000\\gaze_positions.csv"):
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
        exportPath = 'exports\\000\\extracted'
        rows = []

        for index, gazePosition in enumerate(self.data):
            if int(gazePosition[1]) in frames:
                rows.append(index)

        for frame in frames:
            with open(exportPath+'\\gaze_positions%d.csv' % frame, mode='w', newline='') as gaze_positions:
                gaze_positions_writer = csv.writer(gaze_positions, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                gaze_positions_writer.writerow(self.columns[0])

                for row in rows:
                    if frame == int(self.data[row][1]):
                        gaze_positions_writer.writerow(self.data[row])


if __name__ == '__main__':
    csvExtractor = CSVExtractor()
    csvExtractor.readGasePositions()

    numberOfFrames = 5
    frames = random.sample(range(0, int(csvExtractor.data[len(csvExtractor.data)-1][1])+1), numberOfFrames)

    VideoExtractor().retrieveFrames(frames)
    csvExtractor.writeGazePositions(frames)

    VideoExtractor().putFixationOnFrame(frames)
