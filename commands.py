# commands.py
#Первое измение в первой ветке
# commands.py

import csv
from datetime import datetime


class CommandHandler:
    def __init__(self, vfs, username, hostname, log_file):
        self.vfs = vfs
        self.username = username
        self.hostname = hostname
        self.log_file = log_file

    def log_action(self, action):
        with open(self.log_file, "a", newline="") as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow([datetime.now().isoformat(), self.username, action])

    def execute(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return ""
        command = parts[0]
        args = parts[1:]

        commands = {
            "ls": self.ls,
            "cd": self.cd,
            "exit": lambda _: "exit",
            "rev": self.rev,
            "chmod": self.chmod,
            "tac": self.tac,
        }

        func = commands.get(command, lambda _: f"Command not found: {command}")
        output = func(args)
        self.log_action(command_line)
        return output

    def ls(self, args):
        dirs, files = self.vfs.list_dir()
        return "\n".join(dirs + files)

    def cd(self, args):
        if not args:
            return "cd: missing operand"
        try:
            self.vfs.change_dir(args[0])
        except FileNotFoundError as e:
            return str(e)
        return ""

    def rev(self, args):
        if not args:
            return "rev: missing operand"
        try:
            content = self.vfs.read_file(args[0])
            return "\n".join(line[::-1] for line in content.splitlines())
        except FileNotFoundError as e:
            return str(e)

    def chmod(self, args):
        if len(args) < 2:
            return "chmod: missing operand"
        try:
            self.vfs.chmod(args[1], args[0])
            return f"Changed permissions of {args[1]} to {args[0]}"
        except FileNotFoundError as e:
            return str(e)

    def tac(self, args):
        if not args:
            return "tac: missing operand"
        try:
            content = self.vfs.read_file(args[0])
            return "\n".join(reversed(content.splitlines()))
        except FileNotFoundError as e:
            return str(e)
