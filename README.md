# system-storage-jylab

面向 macOS / Windows 的专业只读存储治理技能包。它帮助 Codex 在用户磁盘空间不足时完成只读扫描、目录语义分析、风险分级、证据化处置建议生成，并输出可交互 HTML 工作台。

该仓库版本按“可直接发布到个人 GitHub 仓库”整理：默认不包含运行产物、缓存文件、机器本地路径快照或样例隐私数据。

## 核心能力

- 自动识别 macOS / Windows。
- 扫描阶段严格只读，不删除、不移动、不改权限。
- 按系统管理员视角识别缓存、临时文件、用户资料、App 数据、开发缓存、虚拟机镜像、系统资产等类型。
- 将可处理项目分为三类：🟢 可自动清理、🟡 需人工判断、🔴 谨慎清理。
- 生成专业 HTML 工作台，包含磁盘总览、重点占用条目、执行摘要、结论依据、执行边界、处置分组和后续治理建议。
- 可用本地服务模式提供受保护的一键操作：打开文件夹、移到废纸篓/回收站、绿灯直接删除。
- 内置 `validate_analysis.py`，在报告生成前校验关键字段、容量格式和删除边界。

## 架构

```text
system-storage-jylab/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── report_template.html
├── references/
│   ├── macos.md
│   ├── reporting.md
│   └── windows.md
└── scripts/
    ├── validate_analysis.py
    ├── scan.py
    ├── build_report.py
    └── server.py
```

## 工作流

1. 运行 `scripts/scan.py` 生成只读扫描 JSON。
2. Codex 根据 `references/macos.md` 或 `references/windows.md` 做目录语义分析。
3. Codex 按 `references/reporting.md` 生成 analysis JSON，补齐 Top5、三色分级、证据、影响面、回滚方式、清理注意事项、风险因素和长期建议。
4. 运行 `scripts/validate_analysis.py` 校验 analysis JSON。
5. 用 `scripts/server.py` 启动本地交互工作台，或用 `scripts/build_report.py` 生成静态 HTML。

## 安全模型

- 扫描脚本只读。
- 本地服务绑定 `127.0.0.1`，使用随机端口和随机 token。
- 删除 API 只接受报告中白名单路径，并执行 `realpath` 校验。
- `rm` 仅允许绿灯 `trash_paths`。
- `trash` 允许绿灯和橙灯中明确核实过的 `trash_paths`。
- `open` 允许打开橙灯路径和红灯应用路径，但不执行破坏性操作。
- 每次浏览器操作都需要用户确认。
- 红灯项只做风险提示和正规处理引导，不提供直接删除入口。
- 混合目录若同时含缓存、数据库、同步数据或程序本体，默认不授予整目录清理权限。

## 隐私与发布边界

- `scan.py` 生成的扫描结果会包含当前机器的环境信息，例如用户名、主目录路径、磁盘信息和目录结构摘要。
- `analysis.json` 与最终 HTML 报告会继承上述环境信息，并进一步写入本机目录证据、清理建议和风险判断。
- 这些运行产物适合本地使用，不适合作为公开仓库样例直接提交。
- 本仓库的 `.gitignore` 已默认忽略常见扫描结果、分析结果、工作台报告和缓存文件；发布前仍应人工确认没有把临时产物复制进仓库。
- 若确实需要公开展示报告样例，应先人工脱敏，去除用户名、主目录、真实磁盘卷标、业务项目路径和聊天/同步软件痕迹。

## 运行方式

macOS:

```bash
cd system-storage-jylab
python3 scripts/scan.py > /tmp/storage_scan.json
```

Windows:

```powershell
cd system-storage-jylab
py -3 scripts\scan.py > $env:TEMP\storage_scan.json
```

analysis JSON 校验：

```bash
python3 scripts/validate_analysis.py /tmp/storage_analysis.json
```

生成 analysis JSON 后启动交互报告：

```bash
python3 scripts/server.py /tmp/storage_analysis.json
```

生成静态报告：

```bash
python3 scripts/build_report.py /tmp/storage_analysis.json ~/Desktop/storage-report.html
```

## 清理注意事项

- 大规模清理前确认关键资料有备份。
- 关闭浏览器、IDE、Docker、虚拟机、聊天软件和同步盘客户端后再处理相关目录。
- 优先使用“移到废纸篓/回收站”，确认系统和应用正常后再清空。
- 云盘同步目录、聊天记录、虚拟机镜像、Docker volume、App 数据库不得自动删除。
- 清理后重新扫描，核对释放空间和新的 Top5。

## 风险因素

- 直接删除不可恢复。
- AppData、Application Support、Containers 中可能包含数据库和用户资料。
- 云盘目录删除可能同步到云端和其他设备。
- 系统目录、组件存储、APFS 快照、虚拟内存文件不应手工删除。
- 开发缓存可再生，但会带来重新下载依赖、重新构建、重新索引的时间成本。

## 平台状态

- macOS：扫描、报告、本地服务和删除白名单机制已实现。
- Windows：扫描与回收站机制已实现，首次在真实 Windows 环境使用时应重点验证路径枚举、权限、回收站行为和多盘符展示。

## 依赖

仅使用 Python 3 标准库，无第三方依赖。

## 发布前检查

- 确认仓库内不存在 `storage_scan*.json`、`storage_analysis*.json`、`*-workbench.html`、`*-report.html` 等运行产物。
- 确认不存在 `__pycache__/`、`.pyc`、临时日志、系统缩略图等无关文件。
- 确认 README、SKILL、references 中只保留通用路径示例，不包含个人用户名、个人目录、企业内网地址或真实业务路径。
- 若准备演示报告截图，先核对截图内是否出现用户名、磁盘名称、项目目录名、聊天软件目录、云盘目录或客户数据。
- 首次公开发布前，建议在一个干净目录重新打包或重新克隆后再检查一次文件列表。

## 引用与来源说明

- 本项目中的能力边界、目录分级规则、风险提示和报告写法，来源于仓库内的自有说明文件：`SKILL.md`、`references/macos.md`、`references/windows.md`、`references/reporting.md`。
- 代码与模板的直接实现来源于本仓库文件：`scripts/*.py`、`assets/report_template.html`、`agents/openai.yaml`。
- README 中若提到平台行为、目录语义或操作建议，默认以本仓库上述文件为准；对外引用或二次分发时，应注明来源为 `system-storage-jylab` 仓库，并保留这类边界说明。
- 本仓库不附带第三方商业资料、真实用户扫描数据或生产环境样本；如后续补充案例、截图或报告样例，需单独标注数据来源、脱敏方式和适用范围。
