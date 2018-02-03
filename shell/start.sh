#!/usr/bin/env bash

# 根目录
ENV_ROOT_DIR="$(cd "$(dirname "$0")" && cd .. && pwd)"
# src目录
ENV_SRC_DIR="$ENV_ROOT_DIR"/src

python "${ENV_SRC_DIR}"/main.py