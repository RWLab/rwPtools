from enum import Enum
import os
import time
import subprocess
import tempfile
import platform

# this should live in the config
GCP_COMMANDS = [
    'gcloud',
    'auth',
    'login',
    '--enable-gdrive-access',
    '--no-launch-browser',
    '--quiet',
    '--update-adc'
]


# this should be in utils
class Platform(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'


class AuthenticateGCP:

    def __init__(self):
        self.fd, self.name = tempfile.mkstemp()
        self.gcloud_process = self.get_gcloud_process()

    def get_gcloud_process(self):
        """fd is the file descriptor returned by os.open"""
        return subprocess.Popen(
            GCP_COMMANDS,
            stdin=subprocess.PIPE,
            stdout=self.fd,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True if platform.system() != Platform.WINDOWS else False
        )

    def login(self):
        while True:
            time.sleep(0.2)
            os.fsync(self.fd)

            with open(self.name) as fp:
                prompt = fp.read()
                if 'https' in prompt:
                    break

        get_code = input
        # Combine the URL with the verification prompt to work around
        # https://github.com/jupyter/notebook/issues/3159
        prompt = prompt.rstrip()
        code = get_code(prompt + ' ')
        self.gcloud_process.communicate(code.strip())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.close(self.fd)
        os.remove(self.name)

        if self.gcloud_process.returncode:
            raise Exception("ERROR Authentication Failed!")
        else:
            print('Account is authenticated!')


if __name__ == '__main__':
    with AuthenticateGCP() as gcp:
        gcp.login()
