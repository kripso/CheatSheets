import logging
from PIL import Image
import unicodedata
import json
import os


class DataManager:
    def __init__(self) -> None:
        # self.logger = get_logger("data_managment")
        # self.logger.setLevel(logging.INFO)
        pass

    def remove_accent(self, text: str) -> str:
        """
        Remove accent from text
        :param text: text to remove accent from
        :return: text without accent
        """
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8", "ignore")

    def get_json_entries(self) -> dict:
        with open("./data/targets.nested.json", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                yield data

    def save_image(self, img_name: str, image: Image) -> None:
        directory = self.check_directory(f"./data/images/{self.remove_accent(img_name)}")
        index = len(os.listdir(directory))

        with open(f"{directory}/image_{index}.png", "wb") as f:
            image.save(f, "JPEG")

    def check_directory(self, directory: str) -> str:
        if not os.path.exists(directory):
            # self.logger.info(f"Creating folder: {directory}")
            os.makedirs(directory)
        return directory


if __name__ == "__main__":
    data_manager = DataManager()
    # data_manager.logger.info("test")
