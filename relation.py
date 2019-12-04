import sys
import pred
from process import inv_label_mapping
from eval import *

HAS_RANK = 'has_rank'
HAS_TOR = 'has_title_or_role'
# HAS_TITLE = 'has_title'
IS_POSTED = 'is_posted'
all_relation_types = [HAS_RANK, HAS_TOR, IS_POSTED]

class NameEntity():
    def __init__(self, id, name, type, span):
        self.id = id
        self.name = name
        self.type = type
        self.span = span

    def __str__(self):
        return str(self.id) + " |||| " + self.name + " |||| " + inv_label_mapping[self.type] + " |||| " + str(self.span)

    def get_ann_str(self):
        return "T{}	{} {} {}	{}".format(self.id, \
            inv_label_mapping[self.type], self.span[0], self.span[1], self.name)


class Relation():
    def __init__(self, id, arg1, arg2, type):
        if type in all_relation_types:
            self.type = type
        else:
            raise NameError(relationship, ': such relationship does not exist!')
        self.id = id
        self.arg1 = arg1 # class NameEntity
        self.arg2 = arg2 # class NameEntity

    def __str__(self):
        return str(self.id) + ': ' + self.arg1.name + ' <--- ' + self.type + ' --- ' + self.arg2.name

    def get_ann_str(self):
        return "R{}	{} Arg1:T{} Arg2:T{}".format(self.id, \
            self.type, self.arg1.id, self.arg2.id)

def get_relations(rel_count, pred_entities):
    person_entities = []
    for entity in pred_entities:
        if entity.type == "PER":
            person_entities.append(entity)

    if len(person_entities) == 0:
        return rel_count, None

    relations = []
    for entity in pred_entities:
        idx = 0
        while idx < len(person_entities) - 1:
            if entity.span[0] >= person_entities[idx].span[1]:
                idx += 1
            else:
                break

        if entity.type == "TOR":
            relations.append(Relation(rel_count, person_entities[idx], entity, HAS_TOR))
            rel_count += 1
        elif entity.type == "RNK":
            relations.append(Relation(rel_count, person_entities[idx], entity, HAS_RANK))
            rel_count += 1
        elif entity.type == "ORG":
            relations.append(Relation(rel_count, person_entities[idx], entity, IS_POSTED))
            rel_count += 1
    # print(relations)
    if len(relations) == 0:
        return rel_count, None
    return rel_count, relations


if __name__ == '__main__':
    # From 0a33bba3-ef02-46e0-897c-0195d43ab626
    if len(sys.argv) < 2:
        print("Type in the name of the input data file")
        exit()

    doc_file = sys.argv[1]
    with open(doc_file) as test_file:
        doc = test_file.read()
    with open(doc_file) as test_file:
        test_sentences = test_file.readlines()
    # doc_sentences = []
    # for stn in test_sentences:
    #     print(repr(stn))
    #     if stn != "":
    #         doc_sentences.append(stn.strip())
    doc_sentences = [sentence.strip() for sentence in test_sentences if sentence.strip() != '']


    # print(doc_sentences)
    # pred_tags = pred.get_prediction(sentence)
    # print(doc_sentences)
    sentence_pred_tags = pred.build_pred_dict(doc_sentences)
    # print(sentence)
    # print(pred_tags)
    # print(sentence_pred_tags)

    name_entity_count = 1
    rel_count = 1
    cur_sentence_start = 0
    cur_doc = ''
    doc_entities = []
    doc_relations = []
    for sentence in doc_sentences:
        # print("\n\n================\n"+sentence)
        cur_doc += sentence + '\n\n'

        # pred_names = []
        # pred_tags = []
        pred_entities = []
        for name_position in sentence_pred_tags[sentence].keys():
            pred_name = sentence[name_position[0]: name_position[1]]
            pred_tag = sentence_pred_tags[sentence][name_position]
            doc_name_position = [cur_sentence_start + name_position[0], \
                                cur_sentence_start + name_position[1]]
            # print(cur_doc[doc_name_position[0] : doc_name_position[1]])
            # pred_names.append(pred_name)
            # pred_tags.append(sentence_pred_tags[sentence][name_position])
            pred_entities.append(NameEntity(name_entity_count, pred_name, pred_tag, doc_name_position))
            name_entity_count += 1
            # print(pred_entities[-1])
        doc_entities += pred_entities



        # import pdb; pdb.set_trace()
        rel_count, relations = get_relations(rel_count, pred_entities)
        # print(relations)
        if relations is not None:
            # print('--- relations')
            # # print("----From sentence:\n" + sentence)
            # for rel in relations:
            #     print(rel)
            doc_relations += relations
        cur_sentence_start += len(sentence) + 2

    ann_path = sys.argv[1][:-4] + '.ann'
    ann_file = open(ann_path,'w')
    for e in doc_entities:
        ann_file.write(e.get_ann_str() + '\n')
    for r in doc_relations:
        ann_file.write(r.get_ann_str() + '\n')
    ann_file.close()
