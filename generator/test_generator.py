from bs4 import BeautifulSoup
import json
import os


def test_html_file(dirpath, fname, entry_file):
    config_dict = generate_data_dicts(entry_file)
    config = fname.split('-')[1].split('.')[0][:-1]
    seqeunce = []
    for i in config:
        seqeunce.append(i)
    with open(dirpath + '\\' + fname, 'rb') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    mydivs = soup.find_all("div", {"class": "searchresult"})
    config_counter = 0
    pass_test = True
    if len(mydivs) != len(seqeunce):
        print('Number of entries in html file is ' + str(len(mydivs)) + ' but should be ' + str(len(seqeunce)))
    for div in mydivs:
        url = div.contents[1].contents[0].strip()
        config = seqeunce[config_counter]
        if not url in config_dict[config]:
            print('url ' + url + ' not in ' + config + ' list ' + 'in file ' + fname)
            for k in config_dict.keys():
                if url in config_dict[k]:
                    print('it is in the ' + k + ' list')
            pass_test = False
        else:
            if 'used' in  config_dict[config][url]:
                pass_test = False
                print((' Duplicate url ' + url + ' in ' + fname))
            else:
                config_dict[config][url]['used'] = True
        config_counter += 1
    return pass_test


def build_entry_dict(entry_list):
    ret = {}
    for entry in entry_list:
        ret[entry['URL']] = entry
    return ret


def generate_data_dicts(entry_file):
    with open(entry_file, 'rb') as f:
        data = json.load(f)

    config_dict = {}
    config_dict['Y'] = build_entry_dict(data['effective'])
    config_dict['M'] = build_entry_dict(data['inconclusive'])
    config_dict['N'] = build_entry_dict(data['ineffective'])
    return config_dict


def print_test_res(res, filename):
    if not res:
        print('Test failed for file:' + filename)


def test_all_files():
    test_pass = True

    for file in os.listdir("."):
        if file.endswith(".html"):
            if 'EEE' in file:
                continue
            if file.startswith('Does Omega Fatty Acids treat Adhd'):
                test_res = test_html_file('.', file, 'pufa_adhd_data_verified.json')
            elif file.startswith('Does Melatonin  treat jetlag'):
                test_res = test_html_file('.', file, 'melatonin_data_verified.json')
            elif file.startswith('Does Ginkgo Biloba treat tinnitus'):
                test_res = test_html_file('.', file,  'ginko_tinnitus_data_verified.json')
            else:
                print('no handler for file ' + file)
            print_test_res(test_res, file)
            test_pass = test_pass and test_res
    if test_pass:
        print('All tests pass!!')

test_all_files()



