import os
import random
import shutil
import inquirer
import time


def confirm():
    try:
        print(f"""
     _____ _            __  __ _           
    /  ___| |          / _|/ _| |          
    \ `--.| |__  _   _| |_| |_| | ___ _ __ 
    `--. \ '_ \| | | |  _|  _| |/ _ \ '__|
    /\__/ / | | | |_| | | | | | |  __/ |   
    \____/|_| |_|\__,_|_| |_| |_|\___|_|   
        Poor's man music shuffler               
        
            OPTIONS:
        - Shuffle: will prepend a random string at the beggining of each audio file (.mp3 or .flac)
        - Revert: will revert all audio files back to their original names
        - Quit: will quit the program                             
            """)
        print(
            f"--> Working directory is: \"{os.getcwd()}\",\n\n>>>WARNING: make sure this is the right directory!<<<\n(if not move the script to the same directory as the files to rename)\n")
        choices = [
            inquirer.List("choice",
                          message="Choose an operation",
                          choices=["Shuffle the files",
                                   "Revert changes",
                                   "Quit"],
                          ),
        ]
        return inquirer.prompt(choices)["choice"]
    except KeyboardInterrupt:
        print("\nQuitting...")
        exit()
    except Exception as e:
        print(f"confirm(): An error occured: {e}")
        exit()


def getAllFiles(path):
    try:
        files = []
        # idk why i need two underscores but it doesnt work without
        for _, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".mp3") or filename.endswith(".flac"):
                    files.append(filename)
        return files
    except Exception as e:
        print(f"getAllFiles(): An error occured: {e}")
        exit()


def generateRandomName(filename):
    if "~" in filename:
        filename = filename.split("~")[-1]

    random_string = "".join(random.choice(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(5))

    new_filename = f"{random_string}~{filename}"

    return new_filename


def getOriginalName(filename):
    if "~" in filename:
        filename = filename.split("~")[-1]

    return filename


if __name__ == "__main__":
    confirm = confirm()
    if confirm == "Quit":
        exit()

    else:
        files = getAllFiles(os.getcwd())

        counter = 0
        for file in files:
            fullPath = os.path.join(os.getcwd(), file)

            if confirm == "Revert changes":
                newName = getOriginalName(file)
            else:
                newName = generateRandomName(file)

            fullNewPath = os.path.join(os.getcwd(), newName)
            try:
                shutil.move(fullPath, fullNewPath)
            except Exception as e:
                print(f"An error occured when renaming \"{file}\": \n{e}")
                exit()
            counter += 1
            print(f"Replaced: {file} -> {newName}\r")

        print(
            f"Renamed: {counter} files. To revert the changes run this script again!")
        time.sleep(0.5)
