from src.service.folderabs import FolderABS
from typing import Tuple
from os import listdir, path, sep

class FolderLister(FolderABS):
    """
    A class to list folders from filesystem.

    Methods
    -------
    listFolder(rootfolder)
        Retrieve folder files and directories.
    """
    def listFolder(self, rootfolder) -> Tuple[list, list]:
        """
        List folders from a given os path.

        Parameters
        -------
        rootfolder: str
            Folder that will be used to retrieve the info.

        Returns
        -------
        folder : list
            All folders of the given path.

        files: list
            All files of the given path.
        """
        f = listdir(rootfolder)
        folders = []
        files = []
        for it in f:
            if path.isdir(f'{rootfolder}{sep}{it}'):
                folders.append(f'{rootfolder}{sep}{it}')
            else:
                files.append(f'{rootfolder}{sep}{it}')
        return folders, files