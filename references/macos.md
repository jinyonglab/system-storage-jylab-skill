# macOS 数据布局与分级参考

分析 macOS 扫描结果时读这份。讲"东西存在哪、怎么辨认、归哪一级"。

## 分析原则

- 用户资料保守：Documents、Desktop、Pictures、Movies、Downloads 中的业务资料默认 🟡，不要直接删除。
- App 沙盒保守：`~/Library/Containers`、`~/Library/Group Containers` 中可能是聊天记录、离线视频、数据库或插件数据，必须先识别 App 和子目录语义。
- 系统资产不手删：`/System`、`/Library`、APFS 快照、swap、Spotlight 索引、Time Machine 本地快照不进入红灯删除项，写入长期建议或系统工具入口。
- 云同步谨慎：iCloud Drive、Dropbox、OneDrive 目录中的删除可能同步到云端。
- 开发缓存可清，但需说明重建成本：首次构建、依赖下载、模拟器启动会变慢。

## 关键目录

| 目录 | 装什么 | 典型分级 |
|---|---|---|
| `~/Library/Caches/*` | 应用/工具缓存（浏览器、Homebrew、pip、playwright） | 🟢 可自动清 |
| `~/.cache/*`、`~/.npm`、`~/.cargo`、`~/.gradle`、`~/.m2` | 开发缓存 | 🟢 |
| `~/Library/Developer/Xcode/DerivedData`、`CoreSimulator` | Xcode 构建/模拟器 | 🟢 |
| `~/Library/Containers/<UUID 或 bundleid>` | 沙盒应用数据（聊天记录、离线视频、设置） | 🟡 多为用户数据 |
| `~/Library/Application Support/*` | 应用数据（Chrome Profile、Claude VM、飞书） | 🟡 |
| `~/Downloads` 里的 .dmg/.pkg | 安装包残留 | 🟢 |
| `/Applications/*.app` | 应用本体 | 🔴 仅当重复/想卸时上灯，否则归蓝色 |
| 系统文件、APFS 本地快照 | 系统 | 不上灯，归蓝色"系统及其他" |
| `~/.docker`、`~/Library/Containers/com.docker.docker` | Docker 镜像、构建缓存、volume | 缓存 🟢 / volume 🟡 |
| Parallels / VMware / UTM 虚拟机目录 | 虚拟磁盘 | 🟡 或 🔴 |
| `~/Library/Mobile Documents` | iCloud Drive | 🟡 |

## 辨认"神秘 UUID 容器"

`~/Library/Containers/` 下 UUID 命名的大目录，要查清属于哪个 App：
- `ls` 进 `Data/Documents/`、`Data/Library/`，找带 bundle id 的子目录（如 `com.bilibili.bbad` → 哔哩哔哩）
- 大头常藏在隐藏目录（如 `.Downloads/` 里的 `.bilitask` 离线视频）
- 看 `Container.plist`、`Data/Library/Preferences/*.plist`、明显的 bundle id、媒体扩展名、数据库文件名辅助判断
- 仍只读，别动文件

## 清理前检查

- 退出相关 App：浏览器、聊天软件、IDE、Docker Desktop、虚拟机、同步盘客户端。
- 对用户资料、App 数据库、虚拟机镜像先确认备份或可重新下载来源。
- 优先使用 App 内清理入口处理离线视频、聊天附件、浏览器下载、云盘本地缓存。
- 先移到废纸篓观察，确认 App 可正常启动、资料未丢，再清空废纸篓释放空间。
- 大规模清理后重新运行 `scan.py`，确认释放量和 Top5 是否变化。

## 风险因素（写入报告）

- 直接删除不可恢复；废纸篓清空后也不可恢复。
- `~/Library/Application Support` 和 `Containers` 中大量文件是应用数据库，不等同于缓存。
- iCloud/OneDrive/Dropbox 目录删除可能同步到云端和其他设备。
- 删除 Docker volume、虚拟机磁盘、IDE 工作区可能造成开发环境或业务数据丢失。
- APFS 可清除空间、Time Machine 本地快照、swap 不应手动硬删。

## 间接释放（写进 long_term，不上红灯）

- 系统"可清除空间"磁盘紧张时自动回收
- 重启释放部分 swap / 临时快照
- `brew cleanup --prune=all`、清 Xcode DerivedData
- 调整 Time Machine 本地快照保留策略

## 删除机制

`server.py` 在 macOS 用 osascript 调访达入废纸篓；首次弹自动化授权，点允许。
