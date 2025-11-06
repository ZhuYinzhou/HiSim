import os
import sys
import pickle


def to_int(s):
    try:
        return int(s)
    except Exception:
        return None


def preview_tweet(tweet, max_len: int = 300):
    if isinstance(tweet, dict):
        keys = list(tweet.keys())
        print("      tweet_keys:", keys)
        text = str(tweet.get("rawContent", tweet.get("content", tweet.get("text", ""))))
        if text:
            print("      text:", text[:max_len] + ("..." if len(text) > max_len else ""))
        if "date" in tweet:
            print("      date:", tweet["date"])
        if "stance" in tweet:
            print("      stance:", tweet["stance"])
        if "behavior" in tweet:
            print("      behavior:", tweet["behavior"])    
    else:
        s = str(tweet)
        print("      ", s[:max_len] + ("..." if len(s) > max_len else ""))


def preview_user(user: str, items, max_steps: int, max_tweets_per_step: int):
    print(f"=== User: {user} ===")

    # items 可能是 list[steps] 或 dict[step_idx]->list[tweets]
    steps_iter = []
    if isinstance(items, list) or isinstance(items, tuple):
        steps_iter = list(enumerate(items))
    elif isinstance(items, dict):
        # 尝试按数字键排序，否则按原有键顺序
        numeric_pairs = []
        non_numeric_pairs = []
        for k, v in items.items():
            ki = to_int(k)
            if ki is None:
                non_numeric_pairs.append((k, v))
            else:
                numeric_pairs.append((ki, v))
        if numeric_pairs:
            numeric_pairs.sort(key=lambda x: x[0])
            steps_iter = numeric_pairs
        else:
            steps_iter = list(items.items())
    else:
        print("  未知的用户数据结构:", type(items))
        return

    print("  步数:", len(steps_iter))
    for idx, step in steps_iter[:max_steps]:
        tweets = step
        step_idx = idx
        if isinstance(steps_iter[0], tuple) and len(steps_iter[0]) == 2:
            # steps_iter 中每个元素是 (idx, data)
            step_idx, tweets = idx, step
        print(f"  -- Step {step_idx} --")

        # 期望 tweets 是 list（该时间步的推文列表）
        if isinstance(tweets, list) or isinstance(tweets, tuple):
            print("    tweets_num:", len(tweets))
            if tweets:
                # README: 该时间步总体立场标注在第一条
                print("    第一条推文（含整体立场标注，若提供）:")
                preview_tweet(tweets[0])

                # 再预览其余几条
                for i, tw in enumerate(tweets[1: max(1, max_tweets_per_step)]):
                    print(f"    预览更多 {i+1}:")
                    preview_tweet(tw)
        else:
            # 有些数据可能是 dict/str 等，直接打印
            print("    非列表时间步数据:")
            preview_tweet(tweets)


def main():
    default_path = "/home/wanghuajie/HiSim/data/hisim_with_tweet/roe_macro_e1.pkl"
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HISIM_INPUT", default_path)
    if not os.path.exists(path):
        print(f"文件不存在: {path}")
        sys.exit(1)

    with open(path, "rb") as f:
        data = pickle.load(f)

    if not isinstance(data, dict):
        print("数据结构异常：期望为 dict[user] -> (list[steps] 或 dict[step]->list[tweets])")
        print(type(data))
        sys.exit(2)

    users = list(data.keys())
    print(f"用户数量: {len(users)}\n")

    # 环境变量控制展示范围
    top_users = os.environ.get("HISIM_TOP_USERS")
    max_steps = int(os.environ.get("HISIM_MAX_STEPS", "3"))
    max_tweets_per_step = int(os.environ.get("HISIM_MAX_TWEETS_PER_STEP", "3"))

    sample_users = users
    if top_users:
        try:
            k = int(top_users)
            sample_users = users[:k]
        except Exception:
            pass

    for user in sample_users:
        items = data.get(user)
        preview_user(user, items, max_steps=max_steps, max_tweets_per_step=max_tweets_per_step)
        print()


if __name__ == "__main__":
    main()


