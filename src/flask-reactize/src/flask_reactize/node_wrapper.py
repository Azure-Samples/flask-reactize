import atexit
import subprocess
import threading


class NodeWrapper:

    _node_process: subprocess.Popen = None

    def __init__(self):
        # Register an event so when the Python app is killed we can
        # kill also the underlying node process
        atexit.register(self.on_exit)

    def start(self, port: int, source_folder_path: str, stdout_handler) -> None:
        """
        Starts a new nodejs server for the given react app source folder and
        port

        :param port: Port to listen to (int)
        :param source_folder_path: Source code of the react app (str)
        :param stdout_handler: Handler to redirect the nodejs stdout
        :return: None
        """

        self._node_process = subprocess.Popen(
            [
                "env",
                f"PORT={port}",
                "env",
                "BROWSER=none",
                "npm",
                "start",
                "--prefix",
                source_folder_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Redirect in a Thread the stdout of the nodejs process
        t = threading.Thread(target=stdout_handler, args=(self._node_process,))
        t.start()

    def on_exit(self) -> None:
        """
        Event handler when the Python is stopped
        """

        if self._node_process is not None:
            self._node_process.kill()
            self._node_process.wait()
