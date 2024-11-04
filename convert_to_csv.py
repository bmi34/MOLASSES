import os
import sys

def clean_txt_to_csv(input_file, output_file):
    """Cleans a TXT file and converts it to CSV format."""
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return
    
    start_index = next((i for i, line in enumerate(lines) if '# EAST' in line), -1)
    
    if start_index != -1:
        try:
            with open(output_file, 'w') as outfile:
                header = lines[start_index].replace('# ', '').strip().replace('\t', ',').replace(' ', ',')
                outfile.write(header + '\n')

                for line in lines[start_index + 1:]:
                    csv_line = line.strip().replace('\t', ',').replace(' ', ',')
                    outfile.write(csv_line + '\n')
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")
    else:
        print(f"No valid data found in {input_file}")

def remove_headers_from_csv(input_file, output_file):
    """Removes the header from the CSV file."""
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()[1:]
        
        with open(output_file, 'w') as outfile:
            outfile.writelines(lines)
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

if __name__ == "__main__":
    # Expecting input file and output file as command line arguments
    if len(sys.argv) != 3:
        print("Usage: python convert_to_csv.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Clean the input file and create a CSV
    clean_txt_to_csv(input_file, output_file)

    # Now remove the header from the created CSV
    final_output_path = f"no_header_{os.path.basename(output_file)}"
    remove_headers_from_csv(output_file, final_output_path)

    # Delete the no-header file after it is created
    try:
        os.remove(final_output_path)
    except Exception as e:
        print(f"Error deleting temporary file {final_output_path}: {e}")

    print(f"Converted and cleaned {input_file} to {output_file} and deleted temporary no-header file.")
