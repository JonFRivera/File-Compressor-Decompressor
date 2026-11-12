import os
import shutil
import struct
import zlib


def ask(question):
    answer = input(question).strip()
    if len(answer) >= 2 and answer[0] == answer[-1] and answer[0] in "\"'":
        answer = answer[1:-1]
    return answer


def rel_name(full, folder):
    return os.path.relpath(full, folder).replace(os.sep, "/").encode("utf-8")


def pack_folder(folder):
    pieces = []
    how_many = 0
    total = 0
    for here, subdirs, files in os.walk(folder):
        subdirs.sort()
        files.sort()
        for d in subdirs:
            name = rel_name(os.path.join(here, d), folder)
            pieces.append(struct.pack(">cI", b"D", len(name)) + name)
        for f in files:
            full = os.path.join(here, f)
            name = rel_name(full, folder)
            with open(full, "rb") as fh:
                data = fh.read()
            pieces.append(struct.pack(">cI", b"F", len(name)) + name
                          + struct.pack(">Q", len(data)) + data)
            how_many += 1
            total += len(data)
    return b"".join(pieces), how_many, total


def unpack_folder(blob, out_dir):
    os.mkdir(out_dir)
    root = os.path.abspath(out_dir)
    how_many = 0
    total = 0
    try:
        pos = 0
        while pos < len(blob):
            kind, name_len = struct.unpack_from(">cI", blob, pos)
            pos += 5
            name = blob[pos:pos + name_len].decode("utf-8")
            pos += name_len

            target = os.path.abspath(os.path.join(root, *name.split("/")))
            if os.path.commonpath([root, target]) != root:
                raise ValueError("archive has a path that escapes the folder: " + name)

            if kind == b"D":
                os.makedirs(target, exist_ok=True)
            elif kind == b"F":
                (size,) = struct.unpack_from(">Q", blob, pos)
                pos += 8
                data = blob[pos:pos + size]
                pos += size
                if len(data) != size:
                    raise ValueError("archive is cut off")
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "wb") as fh:
                    fh.write(data)
                how_many += 1
                total += size
            else:
                raise ValueError("archive has an entry I don't understand")
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise
    return how_many, total


def compress_something():
    name = ask("what do you want to compress? (file or folder): ")
    if name == "":
        print("you didn't type anything")
        return
    name = os.path.normpath(name)
    if not os.path.exists(name):
        print("can't find", name)
        return

    is_folder = os.path.isdir(name)
    out = name + (".zdir" if is_folder else ".z")
    if os.path.exists(out):
        print(out, "already exists, so I'm leaving it alone")
        return

    try:
        if is_folder:
            raw, how_many, total = pack_folder(name)
            before = f"{how_many} files, {total} bytes"
        else:
            with open(name, "rb") as f:
                raw = f.read()
            before = f"{len(raw)} bytes"
        small = zlib.compress(raw, 9)
        with open(out, "wb") as f:
            f.write(small)
    except Exception as err:
        print("something went wrong:", err)
        return
    print(f"done! {name} ({before}) -> {out} ({len(small)} bytes)")


def decompress_something():
    name = ask("which .z or .zdir file? ")
    if name == "":
        print("you didn't type anything")
        return
    name = os.path.normpath(name)
    if not os.path.isfile(name):
        print("can't find a file called", name)
        return

    is_folder = name.endswith(".zdir")
    if is_folder:
        out = name[:-5]
    elif name.endswith(".z"):
        out = name[:-2]
    else:
        out = name + ".out"
    if os.path.exists(out):
        print(out, "already exists, so I'm leaving it alone")
        return

    try:
        with open(name, "rb") as f:
            packed = f.read()
        raw = zlib.decompress(packed)
        if is_folder:
            how_many, total = unpack_folder(raw, out)
            after = f"{how_many} files, {total} bytes"
        else:
            with open(out, "wb") as f:
                f.write(raw)
            after = f"{len(raw)} bytes"
    except Exception as err:
        print("something went wrong:", err)
        return
    print(f"done! {name} ({len(packed)} bytes) -> {out} ({after})")


print("squish - a tiny file and folder compressor")
try:
    while True:
        print()
        print("1. compress")
        print("2. decompress")
        print("3. quit")
        choice = input("> ").strip()
        if choice == "1":
            compress_something()
        elif choice == "2":
            decompress_something()
        elif choice == "3":
            break
        else:
            print("please type 1, 2 or 3")
except (EOFError, KeyboardInterrupt):
    print()
print("bye!")
