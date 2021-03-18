import json


def extractJson(srcData, extractPath):
    with open(extractPath, 'w') as f:
        json.dump(srcData, f, ensure_ascii=False, indent='\t')
