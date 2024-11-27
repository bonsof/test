# filesystem.py
# filesystem.py

import tarfile


# filesystem.py

import tarfile

class VirtualFileSystem:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.tar = tarfile.open(archive_path, "r")
        first_member = self.tar.getmembers()[0]
        if first_member.isdir():
            self.base_path = first_member.name.rstrip('/') + '/'
        else:
            self.base_path = ''
        self.cwd = "."
        #print(f"DEBUG: self.base_path = '{self.base_path}'")

    def list_dir(self, path=None):
        import os
        path = path or self.cwd
        if path == ".":
            abs_path = self.base_path.rstrip('/')
        else:
            abs_path = os.path.normpath(os.path.join(self.base_path, path.lstrip("./")))
        abs_path += '/'

        dirs = set()
        files = set()

        for member in self.tar.getmembers():
            member_path = member.name
            if member_path.startswith(abs_path) and member_path != abs_path:
                relative_path = member_path[len(abs_path):].lstrip("/")
                if '/' in relative_path:
                    dirs.add(relative_path.split('/')[0])
                elif relative_path:
                    if member.isdir():
                        dirs.add(relative_path)
                    else:
                        files.add(relative_path)

        return sorted(dirs), sorted(files)

    def change_dir(self, path):
        import os
        if path == "..":
            if self.cwd != ".":
                self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1]) or "."
        elif path == ".":
            pass
        else:
            new_cwd = os.path.normpath(os.path.join(self.cwd, path))
            abs_path = os.path.normpath(os.path.join(self.base_path, new_cwd.lstrip("./")))
            abs_path += '/'

            if any(member.name.startswith(abs_path) for member in self.tar.getmembers()):
                self.cwd = new_cwd
            else:
                raise FileNotFoundError(f"No such directory: {path}")

    def read_file(self, path):
        import os
        if self.cwd == ".":
            abs_path = path
        else:
            abs_path = os.path.normpath(os.path.join(self.cwd, path))
        possible_paths = []

        # Проверяем различные варианты путей
        for base in [self.base_path, '', './', self.base_path + './']:
            full_path = os.path.normpath(os.path.join(base, abs_path))
            possible_paths.append(full_path)

        for full_path in possible_paths:
            if full_path in self.tar.getnames():
                try:
                    file_obj = self.tar.extractfile(full_path)
                    return file_obj.read().decode("utf-8")  # Используем кодировку 'utf-8'
                except Exception as e:
                    break

        raise FileNotFoundError(f"No such file: {path}")

    def chmod(self, path, permissions):
        # Заглушка, так как tar-архивы не поддерживают изменение прав
        pass

    def close(self):
        self.tar.close()
