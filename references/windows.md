# Windows 数据布局与分级参考

分析 Windows 扫描结果时读这份。讲"东西存在哪、怎么辨认、归哪一级"。
注意：Windows 代码路径在 macOS 上无法验证，分析时对路径存在性保持谨慎。

## 分析原则

- 系统盘优先：缓存、临时目录、AppData、Windows Update 残留通常集中在 C:。
- 用户资料保守：Documents、Desktop、Pictures、Videos、Downloads 中的工作资料默认 🟡，不要给直接删除。
- 应用数据保守：Roaming、浏览器 Profile、聊天软件数据库、同步盘目录默认 🟡 或 🔴，优先应用内清理。
- 系统目录不手删：`C:\Windows`、`System32`、`WinSxS`、驱动目录、ProgramData 中的安全软件/企业管控软件不要手工删除。
- 多盘符要区分：D:/E: 的游戏库、素材库、备份目录多为用户主动存放，给迁移/归档建议，不自动删。

## 多盘符

Windows 通常多个盘（C:、D:…）。磁盘总览会列出所有盘，但**分析和清理聚焦系统盘 C:**——缓存、AppData、临时文件几乎都在 C:。其他盘（D: 等）一般是用户自存的资料/游戏，归 🟡 让用户自己判断，不要自动给删除按钮。

## 关键目录

| 目录（环境变量） | 装什么 | 典型分级 |
|---|---|---|
| `%LOCALAPPDATA%`（`C:\Users\<u>\AppData\Local`） | 浏览器缓存、应用数据、Temp，最大头 | 缓存 🟢 / 应用数据 🟡 |
| `%LOCALAPPDATA%\Temp`、`%TEMP%` | 临时文件 | 🟢 |
| `%APPDATA%`（Roaming） | 应用配置/数据 | 🟡 |
| 浏览器缓存 `%LOCALAPPDATA%\Google\Chrome\User Data\*\Cache`、Edge 同构 | 浏览器缓存 | 🟢 |
| 浏览器 `User Data\<Profile>`（非 Cache 部分） | 书签/登录态 | 🟡 |
| `%USERPROFILE%\.cache`、`.npm`、`.gradle`、`.m2`、`.nuget\packages`、`%LOCALAPPDATA%\pip\Cache`、`Yarn` | 开发缓存 | 🟢 |
| `C:\Program Files`、`Program Files (x86)` | 应用本体 | 🔴 仅重复/想卸时上灯，否则归蓝色 |
| `%USERPROFILE%\Downloads` 的安装包 | exe/msi 残留 | 🟢 |
| `C:\$Recycle.Bin` | 回收站 | 🟡 提示用户清空 |
| `%LOCALAPPDATA%\Docker`、`%USERPROFILE%\.docker` | Docker 镜像、构建缓存、volume | 缓存 🟢 / volume 🟡 |
| Hyper-V / WSL / VirtualBox / VMware 镜像目录 | 虚拟磁盘 | 🟡 或 🔴 |
| OneDrive / Dropbox / iCloud Drive | 同步资料 | 🟡 |

## 系统占用（不上灯，归蓝色"系统及其他"，间接释放写 long_term）

- `C:\Windows\WinSxS`：组件存储，**绝不能手删**，用 `DISM /Online /Cleanup-Image /StartComponentCleanup`
- `C:\Windows\SoftwareDistribution\Download`：Windows Update 缓存，用磁盘清理处理
- `hiberfil.sys`（休眠）、`pagefile.sys`（虚拟内存）：系统管理，别手动删
- `C:\ProgramData\Microsoft\Windows Defender`、安全软件目录：不要手删，可能破坏防护和企业策略
- `System Volume Information`：还原点和卷影副本，走系统保护设置管理
- 间接释放：设置 > 系统 > 存储 > 存储感知；`cleanmgr`（磁盘清理）；扩展磁盘清理选 Windows 更新清理

## 清理前检查

- 确认是否有 OneDrive/Dropbox/企业同步盘：删除本地文件可能同步删除云端文件。
- 清浏览器或聊天软件前，先确认是否需要保留登录态、离线文件、聊天附件。
- 清 Docker/WSL/虚拟机前，确认容器、数据库、开发环境已停止，并区分 image/build cache 与 volume/虚拟磁盘。
- 清 Downloads 时按文件类型和日期筛选；安装包可清，工作交付件、压缩包原件需人工确认。
- 大规模清理后重新运行 `scan.py`，用复扫结果确认释放空间。

## 风险因素（写入报告）

- 直接删除绕过回收站，不可恢复。
- AppData 中很多目录看似缓存，实际可能含数据库、登录态、插件配置或聊天附件。
- 云盘同步目录删除会传播到其他设备和云端。
- Windows Update、驱动、安全软件目录必须走系统工具，不要手动删。
- Windows 回收站按盘符管理，移入回收站不等于释放空间，清空对应回收站后才释放。

## 删除机制

`server.py` 在 Windows 用 ctypes 调 `SHFileOperationW`(FOF_ALLOWUNDO) 送进回收站；纯标准库。🟢 项的 `trash_paths` 应在用户配置文件（`%USERPROFILE%`）目录内，便于白名单与 HOME 越界校验通过。
