# File-Compressor-Decompressor
Script written in Python that enables file compression and decompression.

# File-Compressor-Python
A small file and folder compressor written in Python. The bare minimum has been implemented so far: it shrinks a file or a whole folder into a single compressed file, and turns it back into the original later.

## (BETA)

A small command-line tool in Python 3 that compresses and decompresses single files and whole folders. It is run from a simple menu, and it uses zlib for the actual compression.

## Main files

- `squish.py` (the whole program, no extra libraries to install)

## Command to run (VS Code or any terminal)

```
python3 squish.py
```

## Menu

- `1` compress (a file or a folder)
- `2` decompress (a `.z` or `.zdir` file)
- `3` quit

The program asks for the name of the file or folder after you pick an option. Names with spaces work, and you can paste a path with quotes around it.

## COMPRESSING

```
> 1
what do you want to compress? (file or folder): notes.txt
done! notes.txt (6001 bytes) -> notes.txt.z (63 bytes)

> 1
what do you want to compress? (file or folder): photos
done! photos (6 files, 9019 bytes) -> photos.zdir (3275 bytes)
```

A single file becomes `name.z` and a folder becomes `name.zdir`. The original is never changed or deleted. Subfolders (and empty folders) are included when you compress a folder.

## DECOMPRESSING

```
> 2
which .z or .zdir file? notes.txt.z
done! notes.txt.z (63 bytes) -> notes.txt (6001 bytes)

> 2
which .z or .zdir file? photos.zdir
done! photos.zdir (3275 bytes) -> photos (6 files, 9019 bytes)
```

A `.z` file turns back into the file, and a `.zdir` file turns back into the folder with everything in it. If the file does not end in `.z` or `.zdir`, the result is saved with `.out` added to the name.

Normal name to compressed name:

```
notes.txt        ------>   notes.txt.z
photos           ------>   photos.zdir
notes.txt.z      ------>   notes.txt
photos.zdir      ------>   photos
```

## SAFETY

- It will not overwrite anything. If `notes.txt.z` (or the folder you are unpacking into) already exists, it says so and leaves it alone. This also means decompressing `notes.txt.z` next to the original `notes.txt` will not replace your original. Move or rename one of them first.
- Archives that try to write outside of their own folder (for example with `../` in a file name) are refused, and a broken `.zdir` file does not leave a half-built folder behind.
- Some files can get slightly bigger. Data that is already compressed or random (zip, jpg, mp4, and so on) has nothing left to squeeze out, so it can grow by a few bytes. This is normal for any compressor.

Compress and decompress one thing at a time. Quit any time with option `3` (or Ctrl+C).

## Not yet supported

This is a beta. Not yet supported:

- giving files and folders on the command line
- compressing several things at once
- restoring file permissions and dates
- symbolic links (they are saved as normal files or empty folders)
- password protection
- a progress display for very large files
