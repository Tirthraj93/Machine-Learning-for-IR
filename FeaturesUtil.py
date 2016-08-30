import re, random
from FileUtil import write_json_file, list_to_file, read_json_file
from Constants import FEATURES_FILES, TRAIN_DATA_FILE, TEST_DATA_FILE, TEST_SIZE


class FeaturesUtil:
    def __init__(self, qrel_file):
        """
        :param qrel_file: qrel file to use for filtering and labeling
        """
        # read qrel
        # query_id: {document: label}
        self.qrel_data = self.read_qrel(qrel_file)
        self.feature_dict_list = []

    def write_data_ids(self, train_data_id_file, test_data_id_file):
        """
        write testing data ids in a separate file and training data ids
        in a separate file

        :param train_data_id_file: file to write training data ids in
        :param test_data_id_file: file to write testing data ids in
        """
        train_write_list = []
        test_write_list = []

        self.read_features()

        query_id_list = self.feature_dict_list[0].keys()
        test_query_list = random.sample(query_id_list, TEST_SIZE)

        for query in self.qrel_data:
            if query in test_query_list:
                query_string = query + ' '
                for document in self.qrel_data[query]:
                    test_write_list.append(query_string + document)
            elif query in query_id_list:
                query_string = query + ' '
                for document in self.qrel_data[query]:
                    train_write_list.append(query_string + document)

        list_to_file(train_write_list, train_data_id_file)
        list_to_file(test_write_list, test_data_id_file)

    def read_features(self):
        """
        Read features from features files

        """
        feature_dict_list = []

        for feature_file in FEATURES_FILES:
            feature_dict_list.append(read_json_file(feature_file))

        self.feature_dict_list = feature_dict_list

    def create_features_matrix(self, train_data_ids, test_data_ids):
        """
        create features matrix from feature files in order of data_id_list
        and store the matrix in a file

        :param data_id_list:
        :return:
        """
        train_matrix_list = self.get_feature_matrix_list(train_data_ids)
        test_matrix_list = self.get_feature_matrix_list(test_data_ids)

        list_to_file(train_matrix_list, TRAIN_DATA_FILE)
        list_to_file(test_matrix_list, TEST_DATA_FILE)

    def get_feature_matrix_list(self, data_ids):
        """
        Get list of feature matrix tuples with each element below format.
        <label> <feature>:<value> ... <feature>:<value>

        :param data_ids: data ids for which features are to be recorded
        :return: the list of features matrix
        """
        matrix_list = []

        for element in data_ids:
            query_id = element[0]
            doc_no = element[1]
            label = self.qrel_data[query_id][doc_no]
            label_string = str(label) + ' '

            i = 1
            data_point_string = label_string

            for feature_dict in self.feature_dict_list:
                if query_id in feature_dict and doc_no in feature_dict[query_id]:
                    score = feature_dict[query_id][doc_no]
                    data_point_string += str(i) + ':' + str(score) + ' '
                    i += 1

            matrix_list.append(data_point_string)

        return matrix_list

    def create_feature_file(self, source_file, feature_file):
        """
        Reads IR model results file and creates a feature file
        by removing documents not in qrel file and adding labels

        :param source_file: IR model results file
        :param feature_file: feature based on IR model in json format as
        {
            query_id:
                {
                    doc_no: score
                }
        }
        """

        feature_data = dict()

        # read results and create feature data
        print 'Reading - ', source_file

        with open(source_file, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                split_array = re.split('\\s+', line.strip())

                query_id = split_array[0]
                doc_no = split_array[2]
                score = split_array[4]

                label = self.qrel_data[query_id].get(doc_no, None)

                if label is not None:
                    if query_id in feature_data:
                        feature_data[query_id].update({doc_no: score})
                    else:
                        feature_data[query_id] = {doc_no: score}

        # write feature data into a json file
        write_json_file(feature_data, feature_file)

    def read_qrel(self, qrel_file):
        """
        Reads qrel file

        :param qrel_file: qrel file to read
        :return: query_id: {document: label}
        """

        print 'reading qrel...'

        output = {}
        scores_list = []

        with open(qrel_file, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                split_array = re.split('\\s+', line.strip())
                query_id = split_array[0]
                document = split_array[2]
                grade = split_array[3]

                scores_list.append(float(grade))

                current_dict = output.get(query_id, dict())
                current_dict[document] = float(grade)

                output[query_id] = current_dict

        return output
