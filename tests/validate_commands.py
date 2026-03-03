#!/usr/bin/env python3
"""
Static validation for hirameki command files.

Checks:
1. YAML frontmatter (description field)
2. Universal required phrases (config read, error handling, language output)
3. Write commands have confirm-before-write rule
4. Per-command required sections/phrases
5. decide command explicitly does not write to file
"""

import sys
from pathlib import Path

COMMANDS_DIR = Path(__file__).parent.parent / "commands"

# Commands that write to files (must have confirm-before-write)
WRITE_COMMANDS = {"wrap", "explore", "harvest", "tidy", "journal"}

# Per-command required content (substring checks against file text)
REQUIRED_CONTENT = {
    "__init": [
        "Vault 偵測",
        "語言設定",
        "資料夾解析",
        "寫入設定",
        "參考文件同步",
        "_agent_analysis",
        "_agent_logs",
        "_claude_code_logs",
        "obsidian.json",
    ],
    "catchup": [
        "daily-notes",
        "inbox",
        "昨日進度銜接",
        "Inbox 待處理",
        "建議今日焦點",
    ],
    "wrap": [
        "寫入目標",
        "## Wrap [HH:MM]",
        "完成",
        "進行中",
        "下一步",
        "templates",
    ],
    "explore": [
        "模式偵測",
        "Arc 模式",
        "Bridge 模式",
        "Ghost 模式",
        "Stress-test 模式",
        "save",
        "analysis}/arc/",
        "analysis}/bridge/",
        "analysis}/ghost/",
        "analysis}/stress-test/",
    ],
    "status": [
        "無參數模式",
        "status week",
        "status patterns",
        "潛流",
        "落差分析",
    ],
    "harvest": [
        "可以寫的文章",
        "可以做的工具或專案",
        "值得研究的主題",
        "可以聯繫的人或社群",
        "適合換個媒介的想法",
        "尚未變現的價值",
        "可以畢業的想法",
        "畢業確認流程",
        "analysis}/harvest/",
    ],
    "tidy": [
        "tidy tags",
        "tidy fix",
        "tidy full",
        "缺漏檢查",
        "一致性檢查",
        "Tag 收斂分析",
        "修正邏輯",
        "analysis}/tidy/",
    ],
    "journal": [
        "HHMM",
        "建立模式",
        "追加模式",
        "language 為繁體中文",
        "language 為日本語",
        "language 為 English",
    ],
    "decide": [
        "現況",
        "卡點",
        "關鍵問",
        "雙向門",
        "單向門",
        "反轉法",
        "不寫入檔案",
        "一個問題",
    ],
}

# Must appear in every command file
UNIVERSAL_REQUIRED = [
    ("~/.claude/CLAUDE.md",     "config read path"),
    ("Vault Structure",          "config section name"),
    ("尚未完成初始設定",          "missing-init error message"),
    ("/hirameki:__init",         "recovery instruction"),
]

# Must appear in every command that writes files
WRITE_REQUIRED = [
    ("等確認後再執行", "confirm-before-write rule"),
    ("寫入後印出",     "print-path-after-write rule"),
]

# Language output instruction — at least one of these must appear
LANGUAGE_PHRASES = [
    "language",
    "語言",
]


def check_file(name: str, content: str) -> list[str]:
    errors = []

    # 1. Frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
    elif "description:" not in content:
        errors.append("Missing 'description' field in frontmatter")

    # 2. Universal required phrases
    for phrase, label in UNIVERSAL_REQUIRED:
        if phrase not in content:
            errors.append(f"Missing {label}: {phrase!r}")

    # 3. Write commands: confirm-before-write
    if name in WRITE_COMMANDS:
        for phrase, label in WRITE_REQUIRED:
            if phrase not in content:
                errors.append(f"Write command missing {label}: {phrase!r}")

    # 4. decide must not write to file
    if name == "decide":
        if "不寫入檔案" not in content and "不寫入" not in content:
            errors.append("decide must state it does not write to file")

    # 5. Per-command required content
    for phrase in REQUIRED_CONTENT.get(name, []):
        if phrase not in content:
            errors.append(f"Missing required content: {phrase!r}")

    # 6. Language output instruction
    if not any(p in content for p in LANGUAGE_PHRASES):
        errors.append("Missing language output instruction")

    return errors


def main() -> None:
    command_files = sorted(COMMANDS_DIR.glob("*.md"))

    if not command_files:
        print(f"ERROR: No command files found in {COMMANDS_DIR}")
        sys.exit(1)

    # Check no expected command is missing
    expected = set(REQUIRED_CONTENT.keys())
    found = {f.stem for f in command_files}
    missing_files = expected - found

    all_passed = True
    results = []

    for path in command_files:
        name = path.stem
        content = path.read_text(encoding="utf-8")
        errors = check_file(name, content)
        results.append((name, errors))
        if errors:
            all_passed = False

    # Print results
    for name, errors in results:
        if errors:
            print(f"FAIL  {name}.md")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"ok    {name}.md")

    if missing_files:
        all_passed = False
        print(f"\nMISSING command files: {sorted(missing_files)}")

    print()
    total = len(command_files)
    failed = sum(1 for _, e in results if e)
    print(f"{total - failed}/{total} passed")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
