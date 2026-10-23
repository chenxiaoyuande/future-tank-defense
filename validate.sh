#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/share/xbuilder-tools/go1.27.3/bin:$HOME/go/bin:/usr/bin:/bin"
export GOPROXY=https://goproxy.cn,direct
export XGOROOT="$HOME/go/pkg/mod/github.com/goplus/xgo@v1.7.5"
cd /mnt/e/Code/tank/garden-survival
xgo mod tidy
GOOS=js GOARCH=wasm xgo build -o /tmp/gardensurvival.wasm .
