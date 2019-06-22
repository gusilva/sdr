from abc import ABC, abstractmethod
from typing import Tuple

class FolderABS(ABC):
    """
    Abstract class to list folders.

    Methods
    -------
    listFolder(path)
        Retrieve folder files and directories.
    """

    @abstractmethod
    def listFolder(self, path) -> Tuple[list, list]:
        """
        Abstract method to list folders.

        Parameters
        -------
        path: str
            Folder that will be used to retrieve the info.

        Returns
        -------
        folder : list
            All folders of the given path.

        files: list
            All files of the given path.
        """
        pass