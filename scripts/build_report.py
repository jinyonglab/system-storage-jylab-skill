#!/usr/bin/env python3
"""Inject an analysis JSON into the HTML template -> a standalone report.

Usage:
    build_report.py <analysis.json> [output.html]

The analysis JSON is produced by Claude after interpreting scan.py output.
Schema (all sections optional except system):

{
  "generated_at": "2026-05-28 12:00:00",
  "scan_seconds": 42.1,
  "system": {os, build, arch, user, home, filesystem,
             disk_total, disk_used, disk_free, purgeable},
  "top5": [{rank, tier(green|yellow|red), size, type, name, path, note}],
  "green":  [{
    name, path, size_estimate, kill_processes:[], trash_paths:[...], commands:[{label,cmd}],
    confidence, impact_scope, rollback, verification, recommended_window, evidence:[...]
  }],
  "yellow": [{
    name, path, size, content_profile, why_manual, disposal, risk, trash_paths:[...]?, open_note?,
    confidence, impact_scope, rollback, verification, recommended_window, evidence:[...]
  }],
  "red":    [{
    name, path, size, why_keep, indirect_release, auto_reclaim, app_paths:[...]?,
    confidence, impact_scope, verification, recommended_window, evidence:[...]
  }],
  "denied": ["/path/one", ...],
  "summary": {
    overview,
    tier_stats:{green,yellow,red},
    priority:[...],
    decision_basis:[...],  # 结论依据：例如缓存可再生、应用数据需保守、系统文件不纳入直删
    cleanup_notes:[...],   # 清理前注意事项：备份、关闭应用、废纸篓/回收站、云同步、复扫
    risk_factors:[...],    # 风险因素：误删、数据库损坏、同步删除、直接删除不可恢复、系统目录
    post_cleanup_checks:[...], # 清理后验证：复扫、应用启动、同步状态、磁盘空间变化
    long_term:[...]
  }
}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "report_template.html")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
        "~/Desktop/storage-report.html")

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    blob = json.dumps(data, ensure_ascii=False)
    # 静态报告不带删除能力（DELETE=null），删除按钮只在 server.py 服务时出现
    html = tpl.replace("__REPORT_DATA__", blob).replace("__DELETE_CONFIG__", "null")

    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"报告已生成: {out}")
    print(f"打开: open '{out}'")


if __name__ == "__main__":
    main()
