import csv
import yaml
import argparse

FILE_DEF = dict
MISSING_RESULT = {}
VALIDATE_RESULT = {}


def write_result(folder, module_list):
    f = open(f"{folder}/result.csv", "w")
    for m in module_list:
        module_result = []
        f.write(f"{m}\n")
        f.write(f"{','.join(FILE_DEF[m]['column'])},undefined\n")
        for col in FILE_DEF[m]['column']:
            if col not in VALIDATE_RESULT[m].keys():
                module_result.append('X')
            else:
                module_result.append('V')
        module_result.append(','.join(MISSING_RESULT[m]))
        f.write(f"{','.join(module_result)}\n")


def check_file(folder: str, dataType: str):
    VALIDATE_RESULT[dataType] = {}
    MISSING_RESULT[dataType] = []
    with open(f"{folder}/{dataType}.csv", newline='') as csvfile:
        file_dict = csv.DictReader(csvfile, delimiter=',')
        title_list = file_dict.fieldnames
        for title in title_list:
            find_title = False
            for idx, col in enumerate(FILE_DEF[dataType]['f_col']):
                if title.upper() in col:
                    VALIDATE_RESULT[dataType][FILE_DEF[dataType]
                                              ['column'][idx]] = 'V'
                    find_title = True
                    break
            if not find_title:
                MISSING_RESULT[dataType].append(title)


def refine_def():
    for key in FILE_DEF.keys():
        FILE_DEF[key]['f_col'] = []
        for col in FILE_DEF[key]['column']:
            FILE_DEF[key]['f_col'].append(
                [item.upper() for item in col.split('/')])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default="input",
                        help="the input folder")
    parser.add_argument("-m", "--module", default='crm,item,order',
                        help="the validation module")

    args = parser.parse_args()
    folder_list = args.folder.split(',')
    module_list = args.module.split(',')

    with open("definition.yml") as file:
        FILE_DEF = yaml.safe_load(file)
    refine_def()

    print(
        f"start to check folder:{folder_list} with module:{module_list}...\n")
    for f_name in folder_list:
        print(f"processing folder:{f_name}...")
        MISSING_RESULT = {}
        VALIDATE_RESULT = {}
        for dataType in module_list:
            check_file(f_name, dataType)
        write_result(f_name, module_list)

    print(f"finished.")
