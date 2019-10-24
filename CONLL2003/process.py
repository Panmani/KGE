# Used for CONLL2003 dataset processing
# Ian Y. Ma

import sys

dataset_name = sys.argv[1] # Type in test / train / valid in CLI
dataset_path = '{}.txt'.format(dataset_name)
text_path = '{}.words.txt'.format(dataset_name)
tag_path = '{}.tags.txt'.format(dataset_name)

with open(dataset_path) as dataset:
    content = dataset.readlines()
 # remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

with open(text_path,'w') as text_file:
    cur_line = ""
    for idx, line in enumerate(content):
        split = line.split()
        print(idx, split)
        if len(split) == 0:
            if cur_line != "":
                cur_line = cur_line[:-1] + '\n'
                text_file.write(cur_line)
                cur_line = ""
        elif split[0] != '-DOCSTART-':
            cur_line += split[0] + ' '

with open(tag_path,'w') as tag_file:
    cur_line = ""
    for idx, line in enumerate(content):
        split = line.split()
        print(idx, split)
        if len(split) == 0:
            if cur_line != "":
                cur_line = cur_line[:-1] + '\n'
                tag_file.write(cur_line)
                cur_line = ""
        elif split[0] != '-DOCSTART-':
            cur_line += split[3] + ' '
