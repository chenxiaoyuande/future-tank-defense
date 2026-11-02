#!/usr/bin/env bash
set -euo pipefail
task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$task_script_dir/.."
export PATH="$HOME/.local/share/xbuilder-tools/go1.27.3/bin:$HOME/go/bin:$PATH"
export GOPROXY="${GOPROXY:-https://goproxy.cn,direct}"
export XGOROOT="$HOME/go/pkg/mod/github.com/goplus/xgo@v1.7.5"
export GOOS=js
export GOARCH=wasm
mkdir -p .build/bin
xgo mod tidy
xgo build -o .build/bin/game.wasm .
