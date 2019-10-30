import os
from pathlib import Path
import functools
import json
import pickle
import tensorflow as tf
import pprint
pp = pprint.PrettyPrinter(indent=2)

dir_path = './SFM_STARTER/annotated_sources'
pickle_path = './SFM_STARTER'
out_path = './SFM_STARTER'

label_mapping = {'Person':       'PER',
                 'Rank':         'RAN',
                 'Organization': 'ORG',
                 'Title':        'TIT',
                 'Role':         'ROL'}

def get_sentence(doc, position):
    left = position[0]
    while left >= 0 and doc[left] != '\n':
        left -= 1
    right = position[1]
    while right <= len(doc) and doc[right] != '\n':
        right += 1
    left += 1
    sentence = doc[left: right]
    s_position = (left, right)
    return sentence, s_position

def get_name(sentence, label):
    relative_position = label[2]
    return sentence[relative_position[0]: relative_position[1]]

def get_tag(sentence, labels, position):
    for label in labels:
        if label[2][0] <= position[0] and position[1] <= label[2][1] + 1:
            name_split = sentence[label[2][0]: label[2][1]].split()
            cur_token = sentence[position[0]: position[1]].strip()
            if name_split[0] == cur_token:
                return 'B-' + label_mapping[label[1]]
            else:
                return 'I-' + label_mapping[label[1]]
    return 'O'


if __name__ == '__main__':
    # ====================== Read SFM text and annotation files ======================
    all_docs = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    doc_ids = []
    for doc in all_docs:
        filename, file_extension = os.path.splitext(doc)
        if file_extension == '.txt' and filename[-5:] != '_meta':
            doc_ids.append(filename)

    dataset_labels = {}
    dataset_sentences = {}
    for id in doc_ids:
        # print('+++++++++++++++++++++++++++ ' + id)
        with open(os.path.join(dir_path, id + '.txt'), 'r') as text_file:
            text = text_file.read()
        with open(os.path.join(dir_path, id + '.ann'), 'r') as meta_data:
            meta = meta_data.readlines()

        if id not in dataset_labels:
            dataset_labels[id] = {}

        for line in meta:
            entry = line.strip().split()
            T_R = entry[0]
            if T_R[0] == 'T':
                tag = entry[1]
                position = (int(entry[2]), int(entry[3]))
                name = " ".join(entry[4:])
                sentence, s_position = get_sentence(text, position)
                relative_position = (position[0] - s_position[0], position[1] - s_position[0])
                if s_position in dataset_labels[id]:
                    dataset_labels[id][s_position].append([T_R, tag, relative_position])
                else:
                    dataset_labels[id][s_position] = [[T_R, tag, relative_position]]
                    dataset_sentences[sentence] = [id, s_position]

            elif T_R[0] == 'R':
                relation = entry[1]
                arg1 = entry[2][-2:]
                arg2 = entry[3][-2:]

    # pp.pprint(dataset_labels)
    # pp.pprint(dataset_sentences)
    with open(os.path.join(pickle_path, "dataset_labels.pickle"),"wb") as pickle_file:
        pickle.dump(dataset_labels, pickle_file)
    with open(os.path.join(pickle_path, "dataset_sentences.pickle"),"wb") as pickle_file:
        pickle.dump(dataset_sentences, pickle_file)

    # ====================== Generate training files ======================
    # len(dataset_sentences) == 478
    train_text = os.path.join(out_path, 'train.words.txt')
    train_tags = os.path.join(out_path, 'train.tags.txt')
    train_text_file = open(train_text,'w')
    train_tags_file = open(train_tags,'w')
    valid_text = os.path.join(out_path, 'valid.words.txt')
    valid_tags = os.path.join(out_path, 'valid.tags.txt')
    valid_text_file = open(valid_text,'w')
    valid_tags_file = open(valid_tags,'w')
    test_text = os.path.join(out_path, 'test.words.txt')
    test_tags = os.path.join(out_path, 'test.tags.txt')
    test_text_file = open(test_text,'w')
    test_tags_file = open(test_tags,'w')

    line_count = 0
    for sentence in dataset_sentences.keys():
        id, s_position = dataset_sentences[sentence]
        labels = dataset_labels[id][s_position]

        s_split = sentence.split()
        tag_line = ''
        cur_idx = 0
        prev_tag = None
        for token in s_split:
            position = (cur_idx, cur_idx + len(token))
            tag_line += get_tag(sentence, labels, position) + ' '
            cur_idx += len(token) + 1

        if line_count < 400:
            train_text_file.write(sentence + '\n')
            train_tags_file.write(tag_line[:-1] + '\n')
        elif line_count < 450:
            valid_text_file.write(sentence + '\n')
            valid_tags_file.write(tag_line[:-1] + '\n')
        else:
            test_text_file.write(sentence + '\n')
            test_tags_file.write(tag_line[:-1] + '\n')
        line_count += 1

    train_text_file.close()
    train_tags_file.close()
    valid_text_file.close()
    valid_tags_file.close()
    test_text_file.close()
    test_tags_file.close()
