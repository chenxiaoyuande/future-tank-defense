# 开发工具

从工程根目录运行 `python3 tools/project.py --help` 查看统一入口。

| 命令 | 用途 |
| --- | --- |
| `python3 tools/project.py test` | 74 项实际规则测试和 4 项网页存储测试 |
| `python3 tools/project.py build` | 生成文档、游戏资源和带版本号项目包 |
| `python3 tools/project.py compile` | 编译 WebAssembly 到 `.build/bin/game.wasm` |
| `python3 tools/project.py preview` | 生成首页、职业和脑子预览 SVG |
| `node tools/render_frontend.cjs` | 用 Sharp 把预览 SVG 渲染为 PNG |
| `python3 tools/project.py media` | 编码首页 / 进化 GIF，更新文档图片 |
| `python3 tools/project.py docs` | 同步中英文说明和版本索引 |
| `python3 tools/project.py package` | 打包已生成文件，不重新绘制资源 |
| `python3 tools/project.py check --releases` | 校验文档、项目包和历史版本 |

WSL 运行 Python 和 Go 流程；当前 Sharp 环境在 Windows 中，Node 渲染命令在 Windows 工程目录运行。依赖和完整顺序见 [开发指南](../docs/DEVELOPMENT.md)。

`project_paths.py` / `project_paths.cjs` 统一管理路径；美术生成模块保持单层布局，避免导入链过深。脚本之间的共用函数直接使用明确的模块导入，不通过当前工作目录查找文件。
