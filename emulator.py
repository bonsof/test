# emulator.py

import argparse
from commands import CommandHandler
from filesystem import VirtualFileSystem

def main():
    parser = argparse.ArgumentParser(description='CLI Emulator')
    parser.add_argument('--username', required=True)
    parser.add_argument('--hostname', required=True)
    parser.add_argument('--filesystem', required=True)
    parser.add_argument('--log', required=True)
    parser.add_argument('--init_script', help='Path to the initialization script')

    args = parser.parse_args()

    vfs = VirtualFileSystem(args.filesystem)
    command_handler = CommandHandler(vfs, args.username, args.hostname, args.log)

    should_exit = False  # Флаг для выхода из эмулятора

    # Выполнение команд из скрипта инициализации, если он указан
    if args.init_script:
        try:
            with open(args.init_script, 'r', encoding='utf-8') as f:
                for line in f:
                    cmd = line.strip()
                    if cmd:
                        output = command_handler.execute(cmd)
                        if output:
                            print(output)
                        if cmd == 'exit' or output.strip() == 'exit':
                            should_exit = True
                            break
        except FileNotFoundError:
            print(f"Initialization script not found: {args.init_script}")

    # Если после выполнения скрипта нужно завершить эмулятор
    if should_exit:
        vfs.close()
        return

    # Основной цикл эмулятора
    while True:
        try:
            cmd = input(f"{args.username}@{args.hostname}:{vfs.cwd}$ ")
            output = command_handler.execute(cmd)
            if output:
                print(output)
            if cmd == 'exit' or output.strip() == 'exit':
                break
        except (KeyboardInterrupt, EOFError):
            print("\nСеанс завершён.")
            break

    vfs.close()

if __name__ == '__main__':
    main()
#Третье изменение
