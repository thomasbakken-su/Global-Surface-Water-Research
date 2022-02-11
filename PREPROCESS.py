"""
TIFF2CSV.py
Convert and downsample TIF datasets to CSV files.
:Author: Zuyan He
:Version: v_01
:Date: 2021_12_04
"""

import numpy as np
import time
import os
from PIL import Image

# convert and downsample the original TIF file to csv file
# im: the original TIF image file
# ratio: the compression ratio (both horizontally and vertically)
# filename: the name of the TIF file
# output_dir: target output folder
# file_type: which data attribute type


def reduce(im, ratio, filename, output_dir, file_type):

    reduced_data = np.zeros((ratio, ratio), dtype=int)  # output file

    # config subsections parameter
    r, c = im.shape
    r_sub = int(r / ratio)  # sub_section row size
    c_sub = int(c / ratio)  # sub_section col size
    sub_size = int(r_sub * c_sub)  # total number of sub_section pixels
    current_r = 0
    current_c = 0

    # loop through the originala data and compute the reduced data
    for i in range(ratio):   # loop row

        for j in range(ratio):  # loop col

            # calculate the starting row, col position
            temp_sum = 0
            no_data_count = 0
            r_offset = int(i * r_sub)
            c_offset = int(j * c_sub)

            # loop through current sub_section
            for nr in range(r_sub):
                for nc in range(c_sub):
                    pix_val = int(im[nr + r_offset, nc + c_offset])

                    # handles "occurrence" at following:
                    # 255 - no data
                    # skip these data pixels and continue
                    if (file_type == 'occurrence'):
                        if (pix_val == 255):
                            no_data_count += 1
                            continue

                    # handles "change", at following:
                    # 253 - not water
                    # 254 - unable to calculate
                    # 255 - no data
                    # skip these data pixels and continue
                    elif (file_type == 'change'):
                        if (pix_val == 253 or pix_val == 254 or pix_val == 255):
                            no_data_count += 1
                            continue

                    # handles "seasonality", "recurrence", "transitions", and "extent"
                    # at following:
                    # 0 - not water
                    # 255 - no data
                    # skip these data pixels and continue
                    elif (file_type == 'seasonality' or file_type == 'recurrence' or file_type == 'transitions' or file_type == 'extent'):
                        if (pix_val == 0 or pix_val == 255):
                            no_data_count += 1
                            continue

                    temp_sum = temp_sum + pix_val

            # calculate the average, ignore the no data pixels
            # handle special case when all the region pixels are no data
            if ((sub_size - no_data_count) == 0):
                avg = 0
            else:
                # round to nearest int
                avg = round(temp_sum / (sub_size - no_data_count))

            # save the reduced data point
            reduced_data[i, j] = avg

            # proceed to next col
            current_c = current_c + c_sub

        # proceed to next row
        current_r = current_r + r_sub

    # save the reduced dataset to csv file in target folder
    file_out = output_dir + filename + ".csv"  # construct file name with path
    np.savetxt(file_out, reduced_data, fmt='%i', delimiter=",")


if __name__ == "__main__":

    Image.MAX_IMAGE_PIXELS = None  # remove pixel limitation
    start_t = time.time()
    ratio = 10  # number of sections reduced for each dimension

    # for each datasets folders, create a list of file names
    file_list = os.listdir('change')

    # set file output location
    output_dir = 'Result'

    # remove artifcats from system file when exists
    if ('.DS_Store' in file_list):
        file_list.remove('.DS_Store')

    total_file_count = len(file_list)  # update total file length
    completed = 0  # completed files

    print("\nStart converting, total files = " + str(total_file_count) + "\n")

    # process all the files in the sub_directory
    for filename in file_list:
        print(filename)
        # start time for current file
        start_t_sub = time.time()

        # determine the file type, and handle non-recognized file type
        file_type = ''
        if 'occurrence' in filename:
            file_type = 'occurrence'
        elif 'change' in filename:
            file_type = 'change'
        elif 'seasonality' in filename:
            file_type = 'seasonality'
        elif 'recurrence' in filename:
            file_type = 'recurrence'
        elif 'transitions' in filename:
            file_type = 'transitions'
        elif 'extent' in filename:
            file_type = 'extent'
        else:
            raise Exception('file type not recognized, source: ' + filename)

        # load in the raw data files
        current_path = os.path.abspath(os.getcwd())
        file_path = current_path + "/change/" + filename
        im = Image.open(file_path)
        print(im)
        im = np.array(Image.open(file_path), dtype=np.uint16)
        print(im.shape)
        reduce(im, ratio, filename, output_dir, file_type)

        # print current progress
        completed += 1
        print(str(completed) + " / " + str(total_file_count) + " completed.")

        # calculate current file elapsed time
        end_t_sub = time.time()
        elap_sub = round(end_t_sub - start_t_sub)
        print("    Elapsed time = " + str(elap_sub) + "sec.")

    # calculate total elapse time
    end_t = time.time()
    elap = round(end_t - start_t)
    print("\nTotal time = " + str(elap) + "sec.")
