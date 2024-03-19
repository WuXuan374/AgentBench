import json

def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)

def dump_json(obj, fname, indent=4, mode='w' ,encoding="utf8", ensure_ascii=False):
    """
    @param: ensure_ascii: `False`, 字符原样输出；`True`: 对于非 ASCII 字符进行转义
    """
    if "b" in mode:
        encoding = None
    with open(fname, "w", encoding=encoding) as f:
        return json.dump(obj, f, indent=indent, ensure_ascii=ensure_ascii)

def get_subset_data():
    original_data = load_json("data/knowledgegraph/grailqa/grailqa_dev_0_1000.json")
    start = 0
    end = 260
    subset_data = original_data[start:end]
    dump_json(subset_data, f"data/knowledgegraph/grailqa/grailqa_dev_{start}_{end}.json")

if __name__=='__main__':
    get_subset_data()