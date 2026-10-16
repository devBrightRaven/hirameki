"""Deterministic platform adaptation of the six translated reference guides.

Default is check-only. --write changes only allowlisted Codex generated assets,
never the shared command-native originals, a vault or installed runtime.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = tuple('hirameki-cmds-' + size + suffix + '.md'
              for size in ('short', 'full') for suffix in ('', '-zh-TW', '-ja'))
TEXT = {
    'en': {
        'banner': '> Generated Codex guide. Executable workflow contracts live in `references/`; this translated summary is not runtime configuration.',
        'resolve': 'Resolve current explicit settings or `~/.codex/hirameki-local.md` for vault root/language, then `<vault>/AGENTS.md` for canonical folders. Never read another agent configuration as fallback.',
        'lookup': '2. Read `vault:` from Codex configuration when present; missing values continue setup, not another agent file.',
        'ask': '4. If none found: ask for the vault, verify `.obsidian/`, present the exact proposal and obtain approval before writing Codex configuration.',
        'incomplete': 'Run setup when Codex configuration or required canonical vault layout is incomplete.',
        'detect': '**Step 1 — Vault detection:** Use explicit settings or Codex configuration; then CWD/Obsidian detection and user selection as defined in `references/__init.md`.',
        'policies': 'Policy deployment is outside init: do not create policy symlinks or load a policies vault as runtime configuration.',
        'guidance': 'applicable Codex personal/project guidance',
    },
    'zh': {
        'banner': '> Codex 版生成指南。實際工作流以 `references/` 為準；這份翻譯摘要不是 runtime 設定。',
        'resolve': '先用當前明示設定或 `~/.codex/hirameki-local.md` 取得 vault 路徑與語言，再從 `<vault>/AGENTS.md` 讀取共用資料夾配置。不得以其他 agent 設定作為退路。',
        'lookup': '2. 已有 Codex 設定時讀取 `vault:`；缺少值就接續初始化，不讀其他 agent 檔案。',
        'ask': '4. 都找不到時，詢問 vault 路徑並驗證 `.obsidian/`；展示精確變更、取得核准後才寫入 Codex 設定。',
        'incomplete': 'Codex 設定或必要的共用 vault 配置不完整時進行初始化。',
        'detect': '**第一步 — Vault 偵測：** 使用明示設定或 Codex 設定；後續 CWD、Obsidian 偵測與選擇依 `references/__init.md`。',
        'policies': '政策部署不屬於初始化：不建立政策 symlink，也不把 policies vault 當成 runtime 設定載入。',
        'guidance': '適用的 Codex 個人與專案指示',
    },
    'ja': {
        'banner': '> Codex 用の生成ガイド。実行時の契約は `references/` を参照してください。この翻訳要約は runtime 設定ではありません。',
        'resolve': '明示された設定または `~/.codex/hirameki-local.md` から vault と言語を解決し、共有フォルダーは `<vault>/AGENTS.md` から読みます。他の agent 設定へフォールバックしません。',
        'lookup': '2. Codex 設定がある場合は `vault:` を読みます。不足値は初期設定で補い、他の agent ファイルは読みません。',
        'ask': '4. 見つからない場合は vault を確認し、`.obsidian/` を検証します。正確な変更案を提示し、承認後にのみ Codex 設定へ書き込みます。',
        'incomplete': 'Codex 設定または必要な共有 vault 構成が不完全な場合に初期設定します。',
        'detect': '**ステップ 1 — Vault の検出：** 明示設定または Codex 設定を使い、CWD・Obsidian 検出と選択は `references/__init.md` に従います。',
        'policies': 'ポリシー配備は初期設定の対象外です。ポリシー symlink を作成せず、policies vault を runtime 設定として読み込みません。',
        'guidance': '適用される Codex 個人・プロジェクト指示',
    },
}


def render_asset(name, source):
    if name not in NAMES:
        raise ValueError('non-allowlisted-asset')
    text = TEXT['zh' if '-zh-TW' in name else 'ja' if '-ja' in name else 'en']
    lines = []
    for line in source.splitlines():
        if '~/.claude/rules/' in line:
            line = text['policies']
        elif line.startswith(('Every command reads', '每個指令先從', 'すべてのコマンドは、まず')):
            line = text['resolve']
        elif 'CLAUDE.md' in line and '## Vault Structure' in line:
            line = text['incomplete']
        elif line.startswith('2.') and 'CLAUDE.md' in line:
            line = text['lookup']
        elif line.startswith('4.') and 'CLAUDE.md' in line:
            line = text['ask']
        elif 'CLAUDE.md' in line and ('**Step 1' in line or '**第一步' in line or '**ステップ 1' in line):
            line = text['detect']
        line = line.replace('~/.claude/vault-local.md', '~/.codex/hirameki-local.md')
        line = line.replace('vault-local.md', 'hirameki-local.md')
        line = line.replace('CLAUDE.md', text['guidance'])
        line = line.replace('source: claude-code', 'source: codex')
        line = line.replace('`commands/`', '`references/`')
        lines.append(line)
    rendered = text['banner'] + '\n\n' + '\n'.join(lines) + '\n'
    if '~/.claude/' in rendered or 'CLAUDE.md' in rendered:
        raise ValueError('unadapted-agent-config')
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    pending = []
    for name in NAMES:
        canonical = (ROOT / '_hirameki_cmds' / name).read_bytes()
        target = ROOT / 'codex/skills/hirameki/assets/_hirameki_cmds' / name
        expected = render_asset(name, canonical.decode('utf-8')).encode('utf-8')
        actual = target.read_bytes()
        if actual != expected:
            if args.write and actual != canonical:
                raise ValueError('Refusing to overwrite noncanonical/local-edited asset: ' + name)
            pending.append((target, expected))
    if args.write:
        for target, expected in pending:
            target.write_bytes(expected)
    print(f'Codex assets: {len(NAMES)} checked, {len(pending)} '
          + ('regenerated' if args.write else 'out of date'))
    return 0 if args.write or not pending else 1


if __name__ == '__main__':
    raise SystemExit(main())
