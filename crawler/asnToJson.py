


def asn_names_txt_to_json(input_file, output_file):
    with open(input_file, 'r') as asnFile:
        with open(output_file, 'w') as outFile:
            outFile.write("{\n")

            for txtLine in asnFile:
                splitLine = txtLine.split()
                outString = '"{}": "{}",\n'.format(splitLine[0], (' '.join(splitLine[1:])).replace('"', '').replace('\\', ''))
                outFile.write(outString)

            outFile.write("}")

if __name__ == '__main__':
    asn_names_txt_to_json('asn_names.txt', 'teste.json')