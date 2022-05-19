import os

def parse_line(line):
    """
    Example annotation format
    T4	Title 44 70	General Officer Commanding
    R1	has_rank Arg1:T1 Arg2:T2
    """
    # print(line)
    line_split = line.strip().split("\t")
    id = line_split[0]
    if id[0] == "T":
        content_split = line_split[1].split(" ")
        type = content_split[0]
        start = content_split[1]
        end = content_split[2]
        ne = line_split[2]
        return type, start, end, ne
    else:
        content_split = line_split[1].split(" ")
        type = content_split[0]
        arg1 = content_split[1]
        arg2 = content_split[2]
        return type, arg1, arg2

dataset_dir = "SFM_STARTER/annotated_sources"
ann_files = [f for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f)) and f[-3:] == "ann"]
print(ann_files)

ne_dict = {
         'Person':       [],
         'Rank':         [],
         'Organization': [],
         'Title':        [],
         'Role':         [],
         'Title_Role':   [],
         'Location':     [],
         'Misclass':     [],
         }

rel_dict = {'has_rank'          : 0,
            'has_title_or_role' : 0,
            'has_title'         : 0,
            'has_role'          : 0,
            'is_posted'         : 0}
# HAS_RANK = 'has_rank'
# HAS_TOR = 'has_title_or_role'
# HAS_TITLE = 'has_title'
# HAS_ROLE = 'has_role'
# IS_POSTED = 'is_posted'
# all_relation_types = [HAS_RANK, HAS_TOR, IS_POSTED, HAS_TITLE, HAS_ROLE]

for ann in ann_files:
    with open(os.path.join(dataset_dir, ann)) as ann_f:
        for line in ann_f:
            parsed_line = parse_line(line)
            if len(parsed_line) == 4:
                type, start, end, ne = parsed_line
                # if ne not in ne_dict[type]:
                ne_dict[type].append(ne)
            elif len(parsed_line) == 3:
                type, arg1, arg2 = parsed_line
                rel_dict[type] += 1


for type in ne_dict:
    print(type, len(ne_dict[type]))

print(rel_dict)
