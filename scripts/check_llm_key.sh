#!/usr/bin/env bash
# Verify the Hackstudio 2026 LLM key works. Reads LLM_KEY from the environment
# or from a gitignored .env file. Never prints the key value.
set -euo pipefail

LLM_URL="${LLM_URL:-https://llm-router-qa.qa.us-west-2.aws.wfk8s.com}"

# Load LLM_KEY from .env if not already exported.
if [[ -z "${LLM_KEY:-}" && -f .env ]]; then
  LLM_KEY="$(grep -E '^LLM_KEY=' .env | tail -n1 | cut -d= -f2- | tr -d '"'"'"'')"
fi

if [[ -z "${LLM_KEY:-}" ]]; then
  echo "✗ No LLM_KEY found (checked \$LLM_KEY and .env). Add LLM_KEY=... to .env and retry."
  exit 2
fi

echo "→ Endpoint: $LLM_URL"

# 1) Auth + model list
models_code="$(curl -sS -m 20 -o /tmp/llm_models.json -w '%{http_code}' \
  "$LLM_URL/v1/models" -H "Authorization: Bearer $LLM_KEY")"
if [[ "$models_code" != "200" ]]; then
  echo "✗ /v1/models returned HTTP $models_code (key likely invalid or lacks access)."
  exit 1
fi
echo "✓ Auth OK. Models available:"
python3 -c 'import json,sys; d=json.load(open("/tmp/llm_models.json")); [print("   -",m["id"]) for m in d.get("data",[])]' 2>/dev/null \
  || echo "   (could not parse model list, but auth succeeded)"

# 2) Live chat completion round-trip
chat_code="$(curl -sS -m 30 -o /tmp/llm_chat.json -w '%{http_code}' \
  "$LLM_URL/v1/chat/completions" \
  -H "Authorization: Bearer $LLM_KEY" -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-8","user":"sss-firecode-keycheck","max_tokens":16,
       "messages":[{"role":"user","content":"Reply with exactly: OK"}]}')"
if [[ "$chat_code" != "200" ]]; then
  echo "✗ /v1/chat/completions returned HTTP $chat_code."
  exit 1
fi
reply="$(python3 -c 'import json; print(json.load(open("/tmp/llm_chat.json"))["choices"][0]["message"]["content"].strip())' 2>/dev/null || echo '?')"
echo "✓ Chat round-trip OK. Model replied: $reply"
echo "✓ KEY WORKS."
