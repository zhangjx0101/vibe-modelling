# Claude Code 权限配置指南

> 适用于 VSCode 扩展环境下的 Claude Code。本文档包含推荐的权限配置模板和完整的确认类型说明。

## 设置作用域

| 设置文件 | 位置 | 作用域 | 提交到 Git？ |
|---|---|---|---|
| `~/.claude/settings.json` | 用户主目录 | **全局** — 所有项目生效 | 否 |
| `项目/.claude/settings.json` | 项目根目录 | **仅本项目** — 团队共享 | 是 |
| `项目/.claude/settings.local.json` | 项目根目录 | **仅本项目** — 仅自己 | 否（应加入 `.gitignore`） |

**优先级：** 项目 local > 项目 shared > 全局

**建议：** 通用安全命令放全局，项目特定工具放项目级。

---

## 推荐全局配置

文件：`~/.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Write",
      "Glob",
      "Grep",
      "WebFetch",
      "WebSearch",

      "Bash(ls*)",
      "Bash(pwd*)",
      "Bash(cat*)",
      "Bash(head*)",
      "Bash(tail*)",
      "Bash(wc*)",
      "Bash(echo*)",
      "Bash(which*)",
      "Bash(find*)",
      "Bash(grep*)",
      "Bash(cd*)",
      "Bash(mkdir*)",
      "Bash(cp*)",
      "Bash(mv*)",
      "Bash(touch*)",
      "Bash(diff*)",
      "Bash(sort*)",
      "Bash(uniq*)",
      "Bash(sed*)",
      "Bash(awk*)",

      "Bash(git status*)",
      "Bash(git log*)",
      "Bash(git diff*)",
      "Bash(git show*)",
      "Bash(git branch*)",
      "Bash(git add*)",
      "Bash(git commit*)",
      "Bash(git stash*)",
      "Bash(git tag*)",
      "Bash(git config*)",
      "Bash(git init*)",
      "Bash(git remote*)",

      "Bash(gh auth*)",
      "Bash(gh api*)",

      "Bash(python*)",
      "Bash(python3*)",
      "Bash(pip*)"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(rm -r*)",
      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Bash(git reset --hard*)",
      "Bash(git clean*)"
    ]
  }
}
```

### 配置说明

#### allow — 推荐默认允许

| 类别 | 命令 | 理由 |
|---|---|---|
| **内置工具** | Read, Edit, Write, Glob, Grep | 文件操作，可通过 Ctrl+Z / VSCode Timeline / git 回退 |
| **网络工具** | WebFetch, WebSearch | 只读操作；如研究方向敏感可移除 |
| **文件查看** | ls, cat, head, tail, wc, find, grep | 只读，零风险 |
| **文件操作** | mkdir, cp, mv, touch | 低风险，可逆 |
| **文本处理** | diff, sort, uniq, sed, awk | 常用管道工具 |
| **Git 本地** | status, log, diff, show, branch, add, commit, stash, tag, config, init, remote | 全部本地操作，可回退 |
| **GitHub CLI** | gh auth, gh api | API 查询 |
| **开发工具** | python, python3, pip | 运行脚本和管理依赖 |

#### deny — 永远拦截

| 命令 | 理由 |
|---|---|
| `rm -rf*` / `rm -r*` | 递归删除，不可逆 |
| `git push --force*` / `git push -f*` | 覆盖远程历史，不可逆 |
| `git reset --hard*` | 丢弃未提交修改，不可逆 |
| `git clean*` | 删除未跟踪文件，不可逆 |

#### 未列入 allow（每次需确认）

| 命令 | 理由 |
|---|---|
| `git push` | 推送到远程，他人可见 |
| `git merge` | 可能产生冲突 |
| `git checkout` / `git switch` | 切换分支可能丢失未保存修改 |
| `git rebase` | 改写提交历史 |
| `npm install` / `conda install` | 修改环境依赖 |
| `rm <单个文件>` | 非递归删除也需确认（不进回收站） |

---

## 推荐项目级配置

文件：`项目/.claude/settings.local.json`

按需添加项目特定的工具。以下是学术研究项目（Wolfram + LaTeX + Pandoc）的示例：

```json
{
  "permissions": {
    "allow": [
      "Bash(wolframscript*)",
      "Bash(pandoc*)",
      "Bash(pdflatex*)",
      "Bash(bibtex*)",
      "Bash(latexmk*)"
    ]
  }
}
```

如果工具路径较长（如 Windows 上的非标准安装），需要写完整路径：

```json
{
  "permissions": {
    "allow": [
      "Bash(\"/path/to/wolframscript\"*)",
      "Bash(\"/path/to/pandoc\"*)",
      "Bash(\"/path/to/pdflatex\"*)"
    ]
  }
}
```

---

## 确认类型完整清单

Claude Code 的确认分两层：

### 第一层：工具权限确认（系统弹窗）

系统级弹窗，可通过上述 `allow` / `deny` 配置控制。

| 工具 | 触发时机 | 可配置？ |
|---|---|---|
| Edit / Write | 修改或创建文件 | 是 |
| Bash | 执行 shell 命令 | 是（按命令模式） |
| WebFetch / WebSearch | 联网请求 | 是 |
| Agent | 启动子代理 | 是 |
| NotebookEdit | 编辑 Jupyter Notebook | 是 |

### 第二层：方案/决策确认（AI 对话中暂停）

Claude 自身逻辑判断后的确认，**无法通过配置跳过**，也不应该跳过。

| 确认类型 | 触发条件 | 示例 |
|---|---|---|
| **Plan Mode** | 复杂任务开始前 | "以下是执行计划，方向对吗？" |
| **AskUserQuestion** | 需求不明确 / 多种方案可选 | "目标期刊是哪个？" |
| **循环报告** | 多轮验算/审查完成后 | "Round 1 完成，质量分 85，继续？" |
| **质量门控** | 评分低于阈值 | "Score 78，建议修复后再提交" |
| **Git 语义确认** | commit/push/merge 前 | "准备提交这些修改，确认？" |
| **破坏性操作** | 覆盖未保存文件 / 大批量修改 | "8 个文件将被修改，先看清单？" |

---

## 配置后的日常体验

| 需要你做的事 | 频率 |
|---|---|
| 审核 `git push` | 每阶段 1-2 次 |
| 确认 Plan Mode 方向 | 复杂任务开始时 |
| 回答 Claude 提问 | 不定期 |
| 审核质量报告 | 验算/审查后 |
| 确认 `git merge / checkout` | 偶尔 |

其他操作全部自动执行，无需干预。

---

## 安全网层级

出错时按此顺序恢复：

| 优先级 | 方式 | 说明 |
|---|---|---|
| 1 | `Ctrl+Z` | 编辑器内撤销，最快 |
| 2 | VSCode Timeline | 右键文件 → Open Timeline，文件级历史 |
| 3 | `git diff` / `git stash` | 查看或恢复未 commit 的修改 |
| 4 | `git log` / `git revert` | 回退已 commit 的修改 |
| 5 | GitHub 远程仓库 | 本地全丢了还有远程备份 |

**核心原则：只要定期 commit，几乎所有操作都是可逆的。**
