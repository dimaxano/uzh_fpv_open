import sys
from time import time
import subprocess

import requests
from requests.exceptions import HTTPError

from absl import flags

# some constants definition
ENV = ["indoor", "outdoor"]
CAMERA_SETUP = ["forward", "45"]
GT_STATUS = ["_with_gt", ""]
DATA_URL_WITH_GT = "http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/{}_{}_{}_{}_with_gt."
LEICA_URL = "http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/raw/{}_{}_{}.zip"

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "where to save data. Directory `uzh_fpv_open` will be created here")
flags.DEFINE_enum("sensor", "snap", ["davis", "snap", "all"], "sensor type")
flags.DEFINE_enum("format", "bag", ["bag", "zip", "all"], "data format")
flags.DEFINE_bool("leica", False, "download raw Leica measurements")


def download_file(url, save_file_path):
    """
        Args:
            url - what to download
            save_file_path  - in what file to save
    """
    print(f"Downloading {url} to {save_file_path}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    print(f"{save_file_path} finished!")


def unwrap_list(lst):
    """
        Convert list of lists into single list
    """

    return [l for sublist in lst for l in sublist]


def prepare_urls():
    """
        Return:
            list of data urls, not of all of them are valid
    """

    all_urls = []
    for env in ENV:
        for camera in CAMERA_SETUP:
            n = 16
            if env == "indoor" and camera == "forward":
                n = 12
            elif env == "outdoor" and camera == "forward":
                n = 10
            elif env == "outdoor" and camera == "45":
                n = 2

            for idx in range(n+1):
                for gt_status in GT_STATUS:
                    urls = []
                    if FLAGS.sensor == "all":
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, "davis"))
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, "snap"))
                    elif FLAGS.sensor == "snap":
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, "snapdragon"))
                    else:
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, FLAGS.sensor))

                    if FLAGS.format == "all":
                        urls = [[url + "bag", url + "zip"] for url in urls]
                        urls = unwrap_list(urls)
                    else:
                        urls = [url + FLAGS.format for url in urls]

                    if FLAGS.leica:
                        urls.append(LEICA_URL.format(env, camera, idx))
                    
                    all_urls.append(urls)

    return unwrap_list(all_urls)


def main():

    # ------------------- PREPARE URLS --------------------------------
    all_urls = prepare_urls()

    # ------------------- DOWNLOAD AND SAVE --------------------------------
    for url in urls:
        try:
            download_file(url, "some_save_path")
        except HTTPError:
            print(f"{url} doesn't exists.")
            continue


if __name__ == "__main__":
    # rr = subprocess.call("wget http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/indoor_forward_13_davis.bag", shell=True)

    sys.argv = FLAGS(sys.argv)
    main()

    # t1 = time()
    # response = requests.get('http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/outdoor_45_1_snapdragon_with_gt.bag')
    # print(time() - t1)
    # assert response.status_code < 400

    # try:
    #     download_file("http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/outdoor_45_1_snapdragon_with_gt.bag", "/home/dmitry/Documents/repos/uzh_fpv_open/bla.bag")
    # except HTTPError:
    #     print(f"bbbb doesn't exists.")