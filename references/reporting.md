# 报告写作规范

当 agent 基于 `scan.py` 输出编写 analysis JSON 时，按这份规范控制专业度和可读性。

## 1. 结论写法

- `summary.overview` 只写一句核心判断，格式建议为“当前主要占用集中在 X，按保守口径预计可释放约 Y，优先处理 Z”。
- `summary.priority` 只列 3-5 条，按收益 / 风险 / 操作成本排序。
- 优先写“为什么先做这件事”，再写“怎么做”。

## 2. 证据写法

- 每个绿 / 黄 / 红项都尽量给 `evidence`，写 1-3 条。
- 证据应来自可读路径、文件扩展名、bundle id、目录语义、子目录命名、应用名称，不要写模糊主观判断。
- 若只是推断，用 `confidence: low`；若通过目录结构或应用标识核实，用 `confidence: high`。

## 3. 影响面字段

- `impact_scope`：一句话说明删除后的影响边界，例如“仅影响本地缓存，应用会自动重建”“可能影响离线视频或聊天附件”“建议通过正式卸载路径处理”。
- `rollback`：一句话说明回滚方式，例如“废纸篓恢复后重启应用”“需从云端重新同步”“直接删除后不可恢复”。
- `verification`：一句话说明清理后如何确认，例如“重新打开浏览器并复扫”“确认应用可启动且离线内容无异常”。
- `recommended_window`：一句话说明操作时机，例如“空闲时段处理”“退出 Docker Desktop 后执行”“避开云盘同步高峰期”。

## 4. 用词要求

- 写“建议”“确认”“核实”“疑似”“已识别”，不要写“我猜”“我发现”“应该没事”。
- 风险描述要客观，不要夸张，也不要淡化。
- 对用户动作保持中性指引，避免命令式口吻。

## 5. 字段建议

- 绿灯建议补：`confidence`、`impact_scope`、`rollback`、`verification`、`recommended_window`、`evidence`
- 黄灯建议补：`confidence`、`impact_scope`、`rollback`、`verification`、`recommended_window`、`evidence`
- 红灯建议补：`confidence`、`impact_scope`、`verification`、`recommended_window`、`evidence`

## 5.1 双语报告

- 若报告要支持中英文切换，给可读文本补可选英文镜像字段，命名规则为 `<field>_en`。
- 常见可镜像字段：`overview_en`、`name_en`、`type_en`、`note_en`、`content_profile_en`、`why_manual_en`、`disposal_en`、`risk_en`、`why_keep_en`、`indirect_release_en`、`impact_scope_en`、`rollback_en`、`verification_en`、`recommended_window_en`、`evidence_en`。
- 列表型摘要也可镜像：`priority_en`、`decision_basis_en`、`cleanup_notes_en`、`risk_factors_en`、`post_cleanup_checks_en`、`long_term_en`。
- 如果英文镜像字段缺失，工作台可回退到中文；但面向最终交付时，建议补齐主要结论和高风险项的英文文本。

## 6. 不要这样写

- 不要把系统文件、APFS 快照、Windows 组件存储硬塞进红灯卡片。
- 不要把“可释放空间”写成绝对值承诺。
- 不要在 `size` 字段里写长句解释。
- 不要给没有核实路径边界的目录填 `trash_paths`。
