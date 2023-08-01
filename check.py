import csv
import yaml
import argparse

FILE_DEF = dict
MISSING_RESULT = {}


def print_col_result(dataType):
    if len(FILE_DEF[dataType]['f_col']) > 0 or len(MISSING_RESULT[dataType]) > 0:
        print(f"{dataType}.csv got error...")
        if len(FILE_DEF[dataType]['f_col']) > 0:
            print(f"there are columns not be found, which are already in definition.yml:")
            for item in FILE_DEF[dataType]['f_col']:
                print(f"- {'/'.join(item)}")
        if len(MISSING_RESULT[dataType]) > 0:
            print(f"missing predefined colums:")
            for item in MISSING_RESULT[dataType]:
                print(f"- {item}")
    else:
        print(f"{dataType}.csv pass the validation!")
    print("="*40)


def check_file(folder: str, dataType: str):
    MISSING_RESULT[dataType] = []
    with open(f"{folder}/{dataType}.csv", newline='') as csvfile:
        file_dict = csv.DictReader(csvfile, delimiter=',')
        title_list = file_dict.fieldnames
        for title in title_list:
            find_col = False
            for idx, col in enumerate(FILE_DEF[dataType]['f_col']):
                if title.upper() in col:
                    FILE_DEF[dataType]['f_col'].pop(idx)
                    find_col = True
                    break
            if not find_col:
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
                        help="the input folder")

    args = parser.parse_args()
    folder_list = args.folder.split(',')
    module_list = args.module.split(',')

    with open("definition.yml") as file:
        FILE_DEF = yaml.safe_load(file)
    refine_def()

    print(
        f"start to check folder:{folder_list} with module:{module_list}...\n")
    for f_name in folder_list:
        print(f"folder:{f_name}")
        for dataType in module_list:
            check_file(f_name, dataType)
            print_col_result(dataType)
