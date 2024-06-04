import subprocess
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.restart_bot()

    def restart_bot(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(['python', self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f'{event.src_path} has been modified, restarting bot...')
            self.restart_bot()

if __name__ == "__main__":
    path = "."  # Директория для наблюдения
    script_name = "bot_main.py"  # Имя файла с скриптом вашего бота

    event_handler = ChangeHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f'Started watching for changes in {path}')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()