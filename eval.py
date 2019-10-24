import pickle
import string
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if __name__ == '__main__':
    with open("sentence_pred_tags.pickle","rb") as pickle_in:
        sentence_pred_tags = pickle.load(pickle_in)
    with open("dataset_labels.pickle","rb") as pickle_in:
        dataset_labels = pickle.load(pickle_in)
    with open("dataset_sentences.pickle","rb") as pickle_in:
        dataset_sentences = pickle.load(pickle_in)

    # print(dataset_labels)
    # print(dataset_sentences)
    # print(sentence_pred_tags)

    true_positive_count = 0
    false_positive_count = 0
    false_negative_count = 0
    similar_true_positive_count = 0
    similar_false_positive_count = 0
    similar_false_negative_count = 0
    for sentence in sentence_pred_tags.keys():
        id, s_position = dataset_sentences[sentence]
        # print("=====================")
        # print(sentence_pred_tags[sentence])
        # print(dataset_labels[id][s_position])
        ground_truth_names = []
        for entry in dataset_labels[id][s_position]:
            ground_truth_names.append(entry[3])

        pred_names = []
        for name_position in sentence_pred_tags[sentence].keys():
            pred_name = sentence[name_position[0]: name_position[1]]
            exclude = set(string.punctuation)
            pred_name_stripped = ''.join(ch for ch in pred_name if ch not in exclude)
            pred_names.append(pred_name_stripped)

        for pred_name in pred_names:
            if pred_name in ground_truth_names:
                true_positive_count += 1
            else:
                false_positive_count += 1

        for true_name in ground_truth_names:
            if true_name not in pred_names:
                false_negative_count += 1


        for pred_name in pred_names:
            has_similar = False
            for true_name in ground_truth_names:
                if similar(true_name, pred_name) > 0.5:
                    has_similar = True
                    # print('-----------------')
                    # print(sentence)
                    # print('Ground Truth: ', true_name)
                    # print('Predicted Label: ', pred_name)
                    break
            if has_similar:
                similar_true_positive_count += 1
            else:
                # print('-----------------')
                # print(sentence)
                # print('Predicted Label: ', pred_name)
                # print('True Labels: ', end = '')
                # for true_name in ground_truth_names:
                #     print(true_name, end = ', ')
                # print('')
                similar_false_positive_count += 1

        for true_name in ground_truth_names:
            has_similar = False
            for pred_name in pred_names:
                if similar(true_name, pred_name) > 0.5:
                    has_similar = True
                    break
            if not has_similar:
                print('-----------------')
                print(sentence)
                print('Ground Truth: ', true_name)
                print('Predicted Labels: ', end = '')
                for pname in pred_names:
                    print(pname, end = ', ')
                print('')

                similar_false_negative_count += 1

    print('\n>>>')
    precision = true_positive_count / (false_positive_count + true_positive_count)
    recall = true_positive_count / (false_negative_count + true_positive_count)
    f1_score = 2. / (1. / precision + 1. / recall)
    print('Precision: ', precision)
    print('Recall: ', recall)
    print('F1 score: ', f1_score)

    similar_precision = similar_true_positive_count / (similar_true_positive_count + similar_false_positive_count)
    similar_recall = similar_true_positive_count / (similar_true_positive_count + similar_false_negative_count)
    similar_f1_score = 2. / (1. / similar_precision + 1. / similar_recall)
    print('Similar Precision: ', similar_precision)
    print('Similar Recall: ', similar_recall)
    print('Similar F1 score: ', similar_f1_score)
