import re
import json


def write_json_file(json_data, json_file):
    """
    Writes dictionary into json file

    :param json_data: dictionary to write
    :param json_file: file to dump json data into
    """

    print 'Writing - ', json_file

    with open(json_file, 'w') as out_file:
        json.dump(json_data, out_file)


def read_json_file(json_file):
    """
    Returns dictionary containing contents of given json file

    :param json_file: json file containing json data
    :return: dictionary containing json data
    """

    print 'Reading - ', json_file

    with open(json_file, 'r') as read_file:
        data = json.load(read_file)

    return data


def list_to_file(write_list, write_file):
    """
    Writes given list to a file as each list element in one line

    :param write_list: list to write
    :param write_file: destination file
    """

    with open(write_file, 'w') as out_file:
        for element in write_list:
            out_line = "{}\n".format(element)
            out_file.write(out_line)


def read_list_into_list(read_file):
    """
    Reads each line into file in an array where each elements in
    the array is an array of space separated elements in each line

    :param read_file: file to read
    :return: the list read from file
    """

    data_array = []

    with open(read_file, 'r') as in_file:
        lines = in_file.read().splitlines()
        for line in lines:
            split_array = re.split('\\s+', line.strip())
            data_array.append(split_array)

    return data_array


def read_word_into_list(read_file):
    """
        Reads each line into file in an array where each elements
        :param read_file: file to read
        :return: the list read from file
        """

    data_array = []

    with open(read_file, 'r') as in_file:
        lines = in_file.read().splitlines()
        for line in lines:
            data_array.append(line.strip())

    return data_array
