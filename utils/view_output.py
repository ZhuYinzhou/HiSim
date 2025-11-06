import os
import sys
import pickle


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        os.environ.get("HISIM_OUTPUT", "/home/wanghuajie/HiSim/output/roe_micro.pkl")
    if not os.path.exists(path):
        print(f"文件不存在: {path}")
        sys.exit(1)

    with open(path, "rb") as f:
        data = pickle.load(f)

    if isinstance(data, list):
        print(f"条目数量: {len(data)}\n")
        for idx, item in enumerate(data):
            print(f"=== 条目 {idx} ===")
            if isinstance(item, dict):
                prompt = item.get("prompt")
                response = item.get("response")
                context = item.get("context")
                parsed = item.get("parsed_response")
            else:
                print(str(item))
                print()
                continue

            if prompt is not None:
                s = str(prompt)
                print("[Prompt]", s[:600] + ("..." if len(s) > 600 else ""))

            if response is not None:
                print("[Response] sender:", getattr(response, "sender", ""))
                print("[Response] content:", getattr(response, "content", "")[:600])
                print("[Response] type:", getattr(response, "msg_type", ""))

            if context is not None:
                print("[Context] keys:", list(context.keys()) if isinstance(context, dict) else type(context))

            if parsed is not None:
                print("[Parsed] keys:", list(parsed.keys()) if isinstance(parsed, dict) else type(parsed))

            print()
    elif isinstance(data, dict):
        print(f"Agent 数量: {len(data)}\n")
        for agent_name, agent_dc in data.items():
            print(f"=== Agent: {agent_name} ===")
            if not isinstance(agent_dc, dict):
                print(str(agent_dc))
                print()
                continue
            for turn in sorted(agent_dc.keys()):
                entry = agent_dc[turn]
                print(f"-- Turn {turn} --")
                if isinstance(entry, dict):
                    prompt = entry.get("prompt")
                    response = entry.get("response")
                    parsed = entry.get("parsed_response")

                    if prompt is not None:
                        s = str(prompt)
                        print("[Prompt]", s[:600] + ("..." if len(s) > 600 else ""))

                    if response is not None:
                        print("[Response] sender:", getattr(response, "sender", ""))
                        print("[Response] content:", getattr(response, "content", "")[:600])
                        print("[Response] type:", getattr(response, "msg_type", ""))

                    if parsed is not None:
                        if isinstance(parsed, dict):
                            print("[Parsed] keys:", list(parsed.keys()))
                        else:
                            print("[Parsed]", str(parsed)[:600])
                else:
                    print(str(entry))
            print()
    else:
        print(str(data))


if __name__ == "__main__":
    main()


