from io import BytesIO
import eyed3
from hashlib import md5
import os
import abc
import sndhdr


class AudioFile(abc.ABC):
    files_temp_dir = os.getcwd() + "/temp/"

    def __init__(self, file: BytesIO) -> None:
        self.initial_name = file.name
        self.bytes = file
        file_buffer = file.getbuffer()
        file_name = md5(file_buffer).hexdigest()
        self.file_path = self.files_temp_dir + file_name
        with open(self.file_path, "wb") as f:
            f.write(file_buffer)

    def dispose(self):
        os.remove(self.file_path)

    @abc.abstractmethod
    def is_valid(self) -> bool:
        pass


class MP3File(AudioFile):
    def __init__(self, file: BytesIO) -> None:
        super().__init__(file)
        self.format = ".mp3"

    def is_valid(self):
        return bool(eyed3.load(self.file_path))


class WAVFile(AudioFile):
    def __init__(self, file: BytesIO) -> None:
        super().__init__(file)
        self.format = ".wav"

    def is_valid(self):
        return sndhdr.what(self.file_path) == "wav"


def load_audio_file(file: BytesIO) -> MP3File | WAVFile | None:
    if file.name.lower().endswith("mp3"):
        return MP3File(file)
    elif file.name.lower().endswith("wav"):
        return WAVFile(file)
