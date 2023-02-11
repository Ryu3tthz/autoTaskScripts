import mutagen
import os

def get_bitrate(filename):
    audio = mutagen.File(filename)
    bitrate = audio.info.bitrate
    return bitrate

def get_music_files(directory):
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.m4a'):
                music_files.append(os.path.join(root, file))
    return music_files

def main():
    directory = input("Enter the directory path: ")
    music_files = get_music_files(directory)
    if music_files:
        print("Bitrate information for music files:")
        for file in music_files:
            bitrate = get_bitrate(file)
            if bitrate < 257000:
                print("{}: {} kbps".format(file, bitrate/1000))
    else:
        print("No music files found in the specified directory.")

if __name__ == '__main__':
    main()
