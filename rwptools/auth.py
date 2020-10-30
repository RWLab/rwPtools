import os 
import time 
import subprocess
import tempfile
import platform

def _gcloud_login():
  """Call `gcloud auth login` with custom input handling."""
  # We want to run gcloud and provide user input on stdin; in order to do this,
  # we explicitly buffer the gcloud output and print it ourselves.
  gcloud_command = [
      'gcloud',
      'auth',
      'login',
      '--enable-gdrive-access',
      '--no-launch-browser',
      '--quiet',
      '--update-adc'
  ]
  f, name = tempfile.mkstemp()
  if platform.system() !='Windows':
    gcloud_process = subprocess.Popen(
        gcloud_command,
        stdin=subprocess.PIPE,
        stdout=f,
        stderr=subprocess.STDOUT,
        universal_newlines=True)
  else:
    gcloud_process = subprocess.Popen(
        gcloud_command,
        stdin=subprocess.PIPE,
        stdout=f,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True)

  try:
    while True:
      time.sleep(0.2)
      os.fsync(f)
      prompt = open(name).read()
      if 'https' in prompt:
        break


    get_code = input 
    # Combine the URL with the verification prompt to work around
    # https://github.com/jupyter/notebook/issues/3159
    prompt = prompt.rstrip()
    code = get_code(prompt + ' ')
    gcloud_process.communicate(code.strip())
  finally:
    os.close(f)
    os.remove(name)
  if gcloud_process.returncode:
    raise Exception("ERROR Authentication Failed!")



def authenticate():
  _gcloud_login()