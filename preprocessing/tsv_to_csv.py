import csv
import os


def convert(directory):
    os.chdir(directory)
    for file in os.listdir('.'):
        if '.txt' in str(file):
            print file + '\t->\t' + file.replace('.txt', '.csv')
            in_txt = csv.reader(open(file, "r"), delimiter='\t')
            out_csv = csv.writer(open(file.replace('.txt', '.csv'), 'w'))
            out_csv.writerows(in_txt)
            os.system('rm \'' + file + '\'')


if __name__ == '__main__':
    convert('/home/gustaf/Downloads/17_july/Survey/')