import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = BASE_DIR + "\\Data\\"

RESULTS_FILES = [DATA_PATH + "okapi_tf_results",
                 DATA_PATH + "tf_idf_results",
                 DATA_PATH + "bm25_results",
                 DATA_PATH + "laplace_uni_LM_results",
                 DATA_PATH + "jm_uni_lm_results"]

FEATURES_FILES = [DATA_PATH + "okapi_tf_features",
                 DATA_PATH + "tf_idf_features",
                 DATA_PATH + "bm25_features",
                 DATA_PATH + "laplace_uni_LM_features",
                 DATA_PATH + "jm_uni_lm_features"]

QREL_FILE = DATA_PATH + "qrels.adhoc.51-100.AP89.txt"

TRAIN_DATA_ID_FILE = DATA_PATH + "train_data_id"
TEST_DATA_ID_FILE = DATA_PATH + "test_data_id"

TRAIN_DATA_FILE = DATA_PATH + "train_data"
TEST_DATA_FILE = DATA_PATH + "test_data"

MODEL_FILE = DATA_PATH + "model"

TEST_SIZE = 5

TEST_OUTPUT_FILE = DATA_PATH + "test_output"
TRAIN_OUTPUT_FILE = DATA_PATH + "train_output"

TEST_RESULTS_FILE = DATA_PATH + "test_results"
TRAIN_RESULTS_FILE = DATA_PATH + "train_results"