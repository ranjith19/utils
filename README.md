To run archiver.py:

1. copy the file to the folder you would like to watch.
2. Run `nohup python archiver.py -e <extension> -m <minutes> &`

example: `nohup python archiver.py -e csv -m 10 &` would check for csv files and archive them in a folde once every ten minutes. The csv files will be deleted after being archived
