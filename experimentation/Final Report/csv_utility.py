import csv


def create_new_csv(input_filename):
    # Open the file in append mode
    file_name = input_filename + ".csv"
    with open(file_name, 'w', newline='') as f:
        headers = ['Test Map Name', 'Distance Threshold', 'Rate', 'Path Cost', 'Iterations',
                   'Time Cost', 'Canceled Iterations', 'No. Trials']
        # Create a csv writer
        writer = csv.writer(f)
        # Write the data
        writer.writerow(headers)


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
    # files = ['rrt_summary']
    # for file in files:
    #     file_name = file + '.csv'
    #     output = 'cleaned_' + file_name
    #     delete_even_rows(file_name, output)
    # file_name = "RRT Experimental Data\\rrt_summary"
    # create_new_csv(file_name)
    pass


if __name__ == '__main__':
    main()
