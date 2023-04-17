# Import necessary Ghidra libraries
from ghidra.app.script import GhidraScript
from ghidra.framework.model import DomainFolder

class CreateFolderScript(GhidraScript):

    def create_folder(self, folder_name):
        # Get the project data (data tree) and the root folder
        project_data = self.state.getProject().getProjectData()
        root_folder = project_data.getRootFolder()

        # Check if the folder already exists
        existing_folder = root_folder.getFolder(folder_name)
        if existing_folder is not None:
            print("Folder '{}' already exists.".format(folder_name))
            return existing_folder

        # Create a new folder
        new_folder = root_folder.createFolder(folder_name)
        print("Folder '{}' has been created.".format(folder_name))
        return new_folder

    def run(self):
        folder_name = "MyNewFolder"
        self.create_folder(folder_name)

if __name__ == '__main__':
    script = CreateFolderScript()
    script.run()
