package util

import (
    "time"
)

// 全局变量
var (
    // 根目录
    ROOT_DIR     = FileGetParentDirectory(FileGetCurrentDirectory())
    // 当前时间
    CURRENT_TIME = time.Now().String()
)