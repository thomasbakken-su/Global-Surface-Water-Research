# Global-Surface-Water-Research

Research Project on Global Surface Water Datasets

Data_Information.txt

    This is the documentation of detailed data information for various attributes.

TIF2CSV.py

    This is the TIF file to CSV file converter, it will take in raw file(s) in TIF format from the `Data` directory and output the result(s) in `Result` directory.

    Each raw TIF file contains 40,000 x 40,000 pixels with various value-ranges, the output CSV file is a compressed file which contains 10 x 10 data points.

Data Folder

    Need manually create this folder at the same level as TIF2CSV.py

    Location for all input file(s)

Result Folder

    Need manually create this folder at the same level as TIF2CSV.py

    Location for all output file(s)

.DS_Store

    Ignore this file, it's a system generated artifact
