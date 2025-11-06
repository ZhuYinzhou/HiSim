#!/usr/bin/env bash
set -euo pipefail

# 定位脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 载入环境变量
if [[ -f "${SCRIPT_DIR}/export_env.sh" ]]; then
  # shellcheck disable=SC1090
  source "${SCRIPT_DIR}/export_env.sh"
else
  echo "未找到 ${SCRIPT_DIR}/export_env.sh"
  exit 1
fi

if [[ -z "${OPENAI_API_BASE:-}" || -z "${OPENAI_API_KEY:-}" ]]; then
  echo "环境变量 OPENAI_API_BASE 或 OPENAI_API_KEY 未设置"
  exit 1
fi

echo "使用 OPENAI_API_BASE=${OPENAI_API_BASE} 测试连通性..."

TMP_BODY="$(mktemp)"
HTTP_STATUS=$(curl -sS \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  "${OPENAI_API_BASE%/}/models" \
  -o "${TMP_BODY}" -w "%{http_code}" || true)

echo "HTTP 状态码: ${HTTP_STATUS}"
echo "响应内容:"
sed 's/^/  /' "${TMP_BODY}"

if [[ "${HTTP_STATUS}" -ge 200 && "${HTTP_STATUS}" -lt 300 ]]; then
  echo "✅ API 可用"
  exit 0
else
  echo "❌ API 不可用或认证失败"
  exit 2
fi


