# 规则测试

测试以 `.go.txt` 保存，避免 XBuilder 把开发测试作为运行时 Go 源码编译。`tools/verify_logic.py` 提取实际 `main.spx` 规则，并把这些文件复制到 `.build/logic/` 与 `.build/storage/` 后执行。

| 文件 | 覆盖内容 |
| --- | --- |
| `logic_test.go.txt` | 移动、攻击、碰撞、道具和基础规则 |
| `campaign_test.go.txt` | 二十关、双人、Boss、预警和接触伤害 |
| `profession_test.go.txt` | 三职业、独立进化、TG3 与锁关 |
| `brain_test.go.txt` | 三秒屏障、中断、多目标啃咬、暂停与重建 |
| `progress_test.go.txt` / `checkpoint_test.go.txt` | 金币、旧档、检查点与语言 |
| `progress_web_test.go.txt` | 实际 Go / WebAssembly 存储桥接 |

在工程根目录运行 `python3 tools/project.py test`。测试生成的快照位于 `.build/snapshots/`，正式地图目录位于 `data/level-catalog.json`。
