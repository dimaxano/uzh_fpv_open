import sys
import subprocess

from absl import flags

# some constants definition
ENV = ["indoor", "outdoor"]
CAMERA_SETUP = ["forward", "45"]
GT_STATUS = ["_with_gt", ""]
DATA_URL_WITH_GT = "http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/{}_{}_{}_{}_with_gt."
LEICA_URL = "http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/raw/{}_{}_{}.zip"

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "where to save data")
flags.DEFINE_enum("sensor", "snap", ["davis", "snap", "all"], "sensor type")
flags.DEFINE_enum("format", "bag", ["bag", "zip", "all"], "data format")
flags.DEFINE_bool("leica", False, "download raw Leica measurements")

def main():
    for env in ENV:
        for camera in CAMERA_SETUP:
            idx = 1
            while True:
                for gt_status in GT_STATUS:
                    urls = []
                    if FLAGS.sensor == "all":
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, "davis"))
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, "snap"))
                    else:
                        urls.append(DATA_URL_WITH_GT.format(env, camera, idx, FLAGS.sensor))

                    if FLAGS.format == "all":
                        urls = [[url + "bag", url + "zip"] for url in urls]
                        urls = [url for sublist in urls for url in sublist]
                    else:
                        urls = [url + FLAGS.format for url in urls]

                    if FLAGS.leica:
                        urls.append(LEICA_URL)
    
                print(urls)

                break

# def main():
#     # loading data
#     for env in ENV:
#         for camera in CAMERA_SETUP:
#             
#             
#                 # while True:
#                 
#                 #     break;


if __name__ == "__main__":
    # rr = subprocess.call("wget http://rpg.ifi.uzh.ch/datasets/uzh-fpv-newer-versions/v2/indoor_forward_13_davis.bag", shell=True)

    sys.argv = FLAGS(sys.argv)
    main()
