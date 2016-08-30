from Constants import *
from FeaturesUtil import FeaturesUtil
from FileUtil import read_list_into_list, read_word_into_list, list_to_file
# from liblinearutil import *


# Execute Machine Learning algorithm of choice on ap_89 data set to yield better query results


def create_features(f_util):
    results_length = len(RESULTS_FILES)

    for i in range(0, results_length):
        f_util.create_feature_file(RESULTS_FILES[i], FEATURES_FILES[i])


def create_features_matrix(f_util):
    # write data_id for each data point in features matrix into a file
    f_util.write_data_ids(TRAIN_DATA_ID_FILE, TEST_DATA_ID_FILE)

    # read data_ids from data file
    # array of [query_id, doc_no] like [['60', 'AP890220-0084']...]
    train_data_ids = read_list_into_list(TRAIN_DATA_ID_FILE)
    test_data_ids = read_list_into_list(TEST_DATA_ID_FILE)
    f_util.create_features_matrix(train_data_ids, test_data_ids)


if __name__ == "__main__":
    # features_util = FeaturesUtil(QREL_FILE)

    # create features files
    # create_features(features_util)

    # create features matrix
    # also, split features matrix into training matrix and testing matrix
    # create_features_matrix(features_util)

    # train ML model on training matrix
    # y, x = svm_read_problem(TRAIN_DATA_FILE)

    # -s type : set type of solver (default 1)
    #   for multi-class classification
    # 	 0 -- L2-regularized logistic regression (primal)
    # 	 1 -- L2-regularized L2-loss support vector classification (dual)
    # 	 2 -- L2-regularized L2-loss support vector classification (primal)
    # 	 3 -- L2-regularized L1-loss support vector classification (dual)
    # 	 4 -- support vector classification by Crammer and Singer
    # 	 5 -- L1-regularized L2-loss support vector classification
    # 	 6 -- L1-regularized logistic regression
    # 	 7 -- L2-regularized logistic regression (dual)
    #   for regression
    # 	11 -- L2-regularized L2-loss support vector regression (primal)
    # 	12 -- L2-regularized L2-loss support vector regression (dual)
    # 	13 -- L2-regularized L1-loss support vector regression (dual)
    # model = train(y, x, '-s 11')
    # save_model(MODEL_FILE, model)

    # Testing Performance:
        # run ML model on testing matrix
        # rank and format results for IR(trec) evaluation
    test_data_ids = read_list_into_list(TEST_DATA_ID_FILE) # [[query_id, doc_no]...]
    test_output = read_word_into_list(TEST_OUTPUT_FILE) # [score, ...]
    test_length = len(test_data_ids)

    test_dict = dict()
    for i in range(0, test_length):
        query_id = test_data_ids[i][0]
        doc_no = test_data_ids[i][1]
        score = test_output[i]
        if query_id in test_dict:
            test_dict[query_id].update({doc_no: score})
        else:
            test_dict[query_id] = {doc_no: score}

    test_write_list = []
    for query in test_dict:
        sorted_values = sorted(test_dict[query].iteritems(), key=lambda x: x[1], reverse=True)[:1000]
        i = 1
        for element in sorted_values:
            doc_no = element[0]
            score = element[1]
            test_write_list.append(query + ' ' + 'Q ' + doc_no + ' ' + str(i) + ' ' + str(score) + ' Tirth')
            i += 1

    list_to_file(test_write_list, TEST_RESULTS_FILE)

    # Training Performance:
        # run ML model on training matrix
        # rank and format results for IR(trec) evaluation
    train_data_ids = read_list_into_list(TRAIN_DATA_ID_FILE) # [[query_id, doc_no]...]
    train_output = read_word_into_list(TRAIN_OUTPUT_FILE) # [score, ...]
    train_length = len(train_data_ids)

    train_dict = dict()
    for i in range(0, train_length):
        query_id = train_data_ids[i][0]
        doc_no = train_data_ids[i][1]
        score = train_output[i]
        if query_id in train_dict:
            train_dict[query_id].update({doc_no: score})
        else:
            train_dict[query_id] = {doc_no: score}

    train_write_list = []
    for query in train_dict:
        sorted_values = sorted(train_dict[query].iteritems(), key=lambda x: x[1], reverse=True)[:1000]
        i = 1
        for element in sorted_values:
            doc_no = element[0]
            score = element[1]
            train_write_list.append(query + ' ' + 'Q ' + doc_no + ' ' + str(i) + ' ' + str(score) + ' Tirth')
            i += 1

    list_to_file(train_write_list, TRAIN_RESULTS_FILE)