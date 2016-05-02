from __future__ import print_function
from platform import uname, system, architecture
from sys import stdout, stderr
from os import listdir, getcwd, path

import requests

SC_VERSIONS_URL = "https://saucelabs.com/versions.json"
SC_MAIN_KEY = "Sauce Connect"
DOWNLOAD_URL = "download_url"
SHA1 = "sha1"


def get_sc_key():
    #print(uname(), file=stdout)
    #print(architecture(), file=stdout)
    host_system = system().lower()
    host_arch = architecture()[0].lower()
    if host_system == "darwin":
        return "osx"
    elif host_system == "windows" or host_system == "":
        return "win32"
    elif host_system == "linux":
        if host_arch == "64bit":
            return "linux"
        else:
            return "linux32"
    return None


def get_sc_latest_url():
    key = get_sc_key()
    res = requests.get(SC_VERSIONS_URL)
    url = None
    sha1 = None
    if res.status_code == 200:
        try:
            url = res.json()[SC_MAIN_KEY][key][DOWNLOAD_URL]
            sha1 = res.json()[SC_MAIN_KEY][key][SHA1]
            #print((url, sha1),  file=stdout)
        except Exception as e:
            print("Response was: " + str(res.json()), file=stderr)
            print(e.message, file=stderr)
    else:
        print(res, file=stderr)
        print(res.body(), file=stderr)

    return url, sha1


def get_sc_file():
    from glob import glob
    sc_files = glob(path.join(getcwd(), "sc-*"))
    sc_files = [sc_file for sc_file in sc_files if path.isfile(sc_file)]
    if sc_files:
        return sc_files[0], sha1_of_file(sc_files[0])
    else:
        return None, None


def download_file(url):
    import hashlib
    sha1 = hashlib.sha1()
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                sha1.update(chunk)
    return local_filename, sha1.hexdigest()


def sha1_of_file(filepath):
    import hashlib
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10)
            if not block: break
            sha.update(block)
        return sha.hexdigest()


def update_sc():
    sc_url = get_sc_latest_url()
    sc_file = get_sc_file()
    if sc_url[1] != sc_file[1]:
        dl_file = download_file(sc_url[0])
        if dl_file[1] != sc_url[1]:
            print("Checksum failed! Downloaded: " + dl_file[1] +
                  "Expected" + sc_url[1], file=stderr)
        return dl_file
    else:
        return sc_file


def decompress_file(filename):
    if filename.endswith(".tar.gz"):
        import tarfile
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall()
    elif filename.endswith(".zip"):
        import zipfile
        with zipfile.ZipFile(filename, "r") as zip:
            zip.extractall()


def main():
    fileInfo = update_sc()
    decompress_file(fileInfo[0])

if __name__ == '__main__':
    main()
