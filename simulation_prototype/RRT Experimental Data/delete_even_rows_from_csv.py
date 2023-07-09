import csv


def delete_even_rows(input_filename, output_filename):
    # Open the input file and the output file
    with open(input_filename, 'r') as ifile, open(output_filename, 'w', newline='') as ofile:
        # Create a csv reader and writer
        reader = csv.reader(ifile)
        writer = csv.writer(ofile)

        # Loop over the input file
        for i, row in enumerate(reader):
            # Write only the odd rows (since index starts at 0 in Python)
            if (i+1) % 2 != 0:
                writer.writerow(row)


def main():
    files = ['rrt_summary', 'test_1', 'test_2', 'test_3', 'test_4', 'test_5', 'test_6']
    for file in files:
        file_name = file + '.csv'
        output = 'cleaned_' + file_name
        delete_even_rows(file_name, output)

if __name__ == '__main__':
    main()