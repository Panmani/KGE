import os
import interact
from main import model_fn
from pathlib import Path
import functools
import json
import pickle

import tensorflow as tf
import pprint
pp = pprint.PrettyPrinter(indent=2)

dir_path = './SFM_dataset/annotated_sources'
DATADIR = 'CONLL2003'
PARAMS = './results/params.json'
MODELDIR = './results/model'

def get_sentence(doc, position):
    left = position[0]
    while left >= 0 and doc[left] != '\n':
        left -= 1
    right = position[1]
    while right <= len(doc) and doc[right] != '\n':
        right += 1
    sentence = " ".join(doc[left + 1: right].strip().split())
    s_position = (left, right)
    return sentence, s_position

# Predict
with Path(PARAMS).open() as f:
    params = json.load(f)
params['words'] = str(Path(DATADIR, 'vocab.words.txt'))
params['chars'] = str(Path(DATADIR, 'vocab.chars.txt'))
params['tags'] = str(Path(DATADIR, 'vocab.tags.txt'))
params['glove'] = str(Path(DATADIR, 'glove.npz'))
estimator = tf.estimator.Estimator(model_fn, MODELDIR, params=params)

def get_prediction(line):
    predict_inpf = functools.partial(interact.predict_input_fn, line)
    for pred in estimator.predict(predict_inpf):
        pred_tags = pred['tags']
        # interact.pretty_print(line, pred['tags'])
        break
    return pred_tags


if __name__ == '__main__':
    all_docs = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    doc_ids = []
    for doc in all_docs:
        filename, file_extension = os.path.splitext(doc)
        if file_extension == '.txt' and filename[-5:] != '_meta':
            doc_ids.append(filename)

    dataset_labels = {}
    dataset_sentences = {}
    for id in doc_ids:
        if id not in dataset_labels:
            dataset_labels[id] = {}
        with open(os.path.join(dir_path, id + '.txt'), 'r') as text_file:
            text = text_file.read()
        with open(os.path.join(dir_path, id + '.ann'), 'r') as meta_data:
            meta = meta_data.readlines()
        # print('+++++++++++++++++++++++++++ ' + id)
        for line in meta:
            # print(line)
            # print("=================================")
            entry = line.strip().split()
            T_R = entry[0]
            if T_R[0] == 'T':
                type = entry[1]
                position = (int(entry[2]), int(entry[3]))
                name = " ".join(entry[4:])
                # print(T_R, type, position, name)

                sentence, s_position = get_sentence(text, position)
                relative_position = (position[0] - s_position[0], position[1] - s_position[0])
                if s_position in dataset_labels[id]:
                    dataset_labels[id][s_position].append([T_R, type, relative_position, name])
                else:
                    dataset_labels[id][s_position] = [[T_R, type, relative_position, name]]
                    dataset_sentences[sentence] = [id, s_position]
                # print(get_sentence(text, position))
            elif T_R[0] == 'R':
                relation = entry[1]
                arg1 = entry[2][-2:]
                arg2 = entry[3][-2:]
                # print(T_R, relation, arg1, arg2)
    with open("dataset_labels.pickle","wb") as pickle_out:
        pickle.dump(dataset_labels, pickle_out)
    with open("dataset_sentences.pickle","wb") as pickle_out:
        pickle.dump(dataset_sentences, pickle_out)
    # pp.pprint(dataset_labels)
    # pp.pprint(dataset_sentences)


    sentence_pred_tags = {}
    test_count = 1
    for sentence in dataset_sentences.keys():
        pred_tags = get_prediction(sentence)
        # print(pred_tags)

        id, s_position = dataset_sentences[sentence]
        true_tags = dataset_labels[id][s_position]

        words = sentence.strip().split()
        cur_idx = 0
        entity_start = 0
        entity_end = 0
        prev_tag = None
        sentence_pred_tags[sentence] = {}
        for i in range(len(words)):
            word = words[i]
            tag = pred_tags[i].decode()
            # print(word, tag, entity_end)
            if tag[0] != 'O':
                # print(tag)
                if tag[0] == 'B':
                    entity_start = cur_idx
                entity_end = cur_idx + len(word)
                if i + 1 >= len(words) or pred_tags[i + 1].decode()[0] != 'I':
                    sentence_pred_tags[sentence][(entity_start, entity_end)] = tag[2:]
                    # print('+++++', sentence[entity_start: entity_end])

            # print(word, tag)
            cur_idx += len(word) + 1
            prev_tag = tag
        # print(sentence)
        # print(sentence_pred_tags[sentence])
        # print('-------- Progress', test_count, len(dataset_sentences))
        test_count += 1
        # break



    with open("sentence_pred_tags.pickle","wb") as pickle_out:
        pickle.dump(sentence_pred_tags, pickle_out)
