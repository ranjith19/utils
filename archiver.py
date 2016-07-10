from __future__ import unicode_literals
import logging
import argparse
import tarfile
import os
import time
import datetime


log = logging.getLogger(__name__)

cwd = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG)

file_log_handler = logging.FileHandler(os.path.join(os.path.basename(os.path.realpath(__file__)) + '.log'))
log.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
log.addHandler(stderr_log_handler)

# nice output format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

parser = argparse.ArgumentParser(description='Generates some files')

parser.add_argument('-e', '--extension',
                    help='The extension of the file to watch',
                    required=False, default='.bkup',
                    type=str)

parser.add_argument('-m', '--minutes',
                    help='The interval between checking',
                    required=False, default=30,
                    type=int)

DEFAULT_DATETIME_FORMAT = '%I-%M-%p-%d-%b-%Y'

args = parser.parse_args()
log.info(args)


def archive():
    files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
    now = datetime.datetime.utcnow()
    outdir = os.path.join(cwd, now.strftime(DEFAULT_DATETIME_FORMAT))

    for file_name in files:
        if file_name.endswith(args.extension):
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            full_path = os.path.join(cwd, file_name)
            dst_file = os.path.join(outdir, file_name + ".tar.gz")

            log.info("Compressing {0} > {1}".format(full_path, dst_file))

            tar = tarfile.open(dst_file, "w:gz")
            tar.add(full_path, arcname=file_name)
            # log.info("Compressed {0} > {1}".format(full_path, dst_file))
            os.remove(full_path)
            tar.close()


if __name__ == "__main__":
    while True:
        archive()
        seconds = args.minutes * 60
        log.info("Shall sleep for :{0}".format(seconds))
        time.sleep(seconds)

