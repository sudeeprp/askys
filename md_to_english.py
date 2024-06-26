import os
import re
import sys

patterns_to_remove = [
    r'^#.*?\n',
    r'```shloka-sa\n(.*?)\n```',
    r'```shloka-sa-hk\n(.*?)\n```',
    r'`(.*?)`'
]


def md_to_english(md):
    english = md
    for pattern in patterns_to_remove:
        english = re.sub(pattern, '', english, flags=re.DOTALL)
    english = re.sub(r'\u200b', ' ', english)
    english = re.sub(r'<a[^>]*>.*?</a>', '', english, flags=re.DOTALL)  # no html tags
    english = re.sub(r'\n_(.*?)_', '', english, flags=re.DOTALL)  # no italics explanations
    english = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', english)  # replace links with text
    english = re.sub(r'[\t\f\v ]{2,}', ' ', english)  # 2 or more spaces become one
    return english.strip()


def md_paras_to_english_list(md):
    english = md_to_english(md)
    eng_no_space_bw_newlines = re.sub(r'\n\s*\n', '\n\n', english)
    english_list_with_newlines = re.split(r'\n\n', eng_no_space_bw_newlines)
    english_list_no_newlines = \
        list(map(lambda e: re.sub(r'\n', ' ', e), english_list_with_newlines))
    return english_list_no_newlines


def mds_to_english_dict(path):
    english_dict = {}
    for filename in os.listdir(path):
        if filename.endswith('.md'):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                english_dict[filename] = md_paras_to_english_list(f.read())
    return english_dict


if __name__ == '__main__':
    print(mds_to_english_dict(sys.argv[1]))
