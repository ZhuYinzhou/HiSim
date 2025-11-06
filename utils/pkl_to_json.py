import os
import sys
import json
import pickle


def to_jsonable(obj):
    try:
        json.dumps(obj)
        return obj
    except Exception:
        # 尝试将可能的自定义对象（如 Message）转为可打印字典
        if hasattr(obj, "__dict__"):
            d = {k: to_jsonable(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
            # 常见字段清洗
            for attr in ("sender", "content", "msg_type", "post_time"):
                if hasattr(obj, attr):
                    d[attr] = getattr(obj, attr)
            return d
        if isinstance(obj, (list, tuple)):
            return [to_jsonable(x) for x in obj]
        if isinstance(obj, dict):
            return {str(k): to_jsonable(v) for k, v in obj.items()}
        # 兜底为字符串
        return str(obj)


def convert(input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        data = pickle.load(f)

    jsonable = to_jsonable(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(jsonable, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 3:
        print("用法: python utils/pkl_to_json.py <input.pkl> <output.json>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}")
        sys.exit(1)
    convert(input_path, output_path)
    print(f"已生成: {output_path}")


if __name__ == "__main__":
    main()


