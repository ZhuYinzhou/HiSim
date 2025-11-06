import os
import sys
import pickle


def preview_item(user: str, item, idx: int, max_len: int = 400):
    print(f"-- {user} | sample {idx} --")
    if isinstance(item, dict):
        # 常见键：rawContent / content / date / stance / behavior 等
        keys = list(item.keys())
        print("keys:", keys)
        text = str(item.get("rawContent", item.get("content", "")))
        if text:
            print("text:", text[:max_len] + ("..." if len(text) > max_len else ""))
        if "date" in item:
            print("date:", item["date"])
        # 若有标注字段也展示
        if "stance" in item:
            print("stance:", item["stance"])
        if "behavior" in item:
            print("behavior:", item["behavior"])    
    else:
        # 其它结构，直接打印摘要
        s = str(item)
        print(s[:max_len] + ("..." if len(s) > max_len else ""))
    print()


def main():
    default_path = "/home/wanghuajie/HiSim/data/hisim_with_tweet/roe_micro.pkl"
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HISIM_INPUT", default_path)

    if not os.path.exists(path):
        print(f"文件不存在: {path}")
        sys.exit(1)

    with open(path, "rb") as f:
        data = pickle.load(f)

    # 情况一：按用户分组的字典
    if isinstance(data, dict):
        users = list(data.keys())
        print(f"用户数量: {len(users)}\n")

        max_per_user = int(os.environ.get("HISIM_MAX_PER_USER", "3"))
        sample_users = users
        top_users = os.environ.get("HISIM_TOP_USERS")
        if top_users:
            try:
                k = int(top_users)
                sample_users = users[:k]
            except Exception:
                pass

        for user in sample_users:
            items = data.get(user, [])
            print(f"=== User: {user} | 条目数: {len(items)} ===")
            for i, item in enumerate(items[:max_per_user]):
                preview_item(user, item, i)

    # 情况二：样本列表（每条为一个推文样本，不区分用户分组）
    elif isinstance(data, list):
        print(f"样本数量: {len(data)}\n")
        max_items = int(os.environ.get("HISIM_MAX_ITEMS", "10"))

        def detect_user(obj):
            if isinstance(obj, dict):
                for k in ("user", "username", "sender", "author"):
                    if k in obj and obj[k]:
                        return str(obj[k])
            return "unknown"

        for i, item in enumerate(data[:max_items]):
            user = detect_user(item)
            preview_item(user, item, i)

    else:
        print("未知数据结构：", type(data))


if __name__ == "__main__":
    main()


