import argparse
import os
import sys
import zipfile
import wave
import logging
import tempfile

logger = logging.getLogger('dsdwrapper')

def parse_arguments():
    """
    prase command line arguments
    :return:  parsed arguments object
    """
    parser = argparse.ArgumentParser(description='Signal demodulation.')
    parser.add_argument('-f', '--filename', help='filename to parse the data', required=True)

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    return parser.parse_args()


def collect_files_to_zip(destinationFile, filesToZip):
    """
    zip output files and attach a metadata from wav
    :return:
    """
    with zipfile.ZipFile('%s.zip' %(destinationFile), 'w') as myzip:
        for f in filesToZip:
            myzip.write(f)
            logger.debug('Archiving %s' %(f,))

def main():
    """
    cat 417.285.wav | padsp dsd -i - -w out.wav
    :param args:
    :return:
    """

    args = parse_arguments()

    # analise file
    outfilename = tempfile.NamedTemporaryFile()
    commandLine = "cat {filename} | padsp dsd -i - -w {outputfile}".format(filename=args.filename, outputfile=outfilename.name)

    logging.debug(commandLine)
    if os.system(commandLine):
        logger.error('command line failed to execute')
        sys.exit(1)

    # parse input file metadata

    # pack to zip archive
    collect_files_to_zip(outfilename.name, [args.filename])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("test")
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
