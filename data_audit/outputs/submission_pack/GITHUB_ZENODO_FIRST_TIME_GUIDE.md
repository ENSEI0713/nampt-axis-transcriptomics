# GitHub 首次上传 + Zenodo DOI 创建 — 新手操作指南

> 适用对象：第一次上传 GitHub、第一次创建 Zenodo DOI 的作者。
> 本指南每一步都写到"点哪里"，照做即可。预计总耗时 20–40 分钟。
> 前提：本仓库已在本地提交完毕（33 个 commit，工作区干净），归档元数据（LICENSE / ARCHIVE_README / .zenodo.json / CITATION.cff / requirements.txt）已备好。

---

## 第 0 步：准备 GitHub 账号（若还没有）

1. 打开 https://github.com/signup
2. 填邮箱、设密码、起用户名（建议与研究相关，如 `yanjing-cupes` 或你的名字拼音）
3. 按提示完成邮箱验证（去邮箱点确认链接）
4. （可选但推荐）上传头像

> 已经有账号的直接跳到第 1 步。

---

## 第 1 步：在 GitHub 上创建空仓库（约 5 分钟）

1. 登录 GitHub，点右上角 **「+」** → **「New repository」**
2. **Repository name** 填：`nampt-axis-transcriptomics`（或你喜欢的名字，全小写、连字符分隔）
3. **Description**（可选）：`State-dependent NAMPT-axis transcriptional programs in obesity and exercise — public-data analysis code (GEO + GTEx + GWAS + Evo2-40B)`
4. **Visibility**：选 **Public**（论文投稿代码必须公开；Zenodo 也要求公开）
5. **重要**：下方 "Add a README file" / ".gitignore" / "license" **三项都不要勾选**（保持空仓库，因为本地已有全部内容，勾了会造成冲突）
6. 点绿色按钮 **「Create repository」**
7. 创建后页面会显示一段命令（"…or push an existing repository from the command line"），**先别关这个页面**，下一步要用里面的地址。

---

## 第 2 步：把本地仓库推上去（约 5 分钟）

在本机打开终端（Windows 建议用 Git Bash，右键桌面 → "Git Bash Here"；或 VS Code 终端），**先 cd 到项目目录**：

```bash
cd /c/Users/yanji/Documents/evo2-40b
```

### 2a. 设置 Git 身份（第一次用 Git 必须做）

把下面的名字和邮箱换成**你的 GitHub 用户名和注册邮箱**（这样提交记录会关联到你的账号，头像和贡献图才显示）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
```

> 注意：本地仓库之前用 `yanji@local` 提交过 33 次。改全局配置后**新提交**会用新身份；历史提交不变。如果想连历史一起改（可选，不建议新手操作），以后再说。

### 2b. 添加远程仓库并推送

回到第 1 步第 7 条的页面，复制里面 `git remote add origin` 开头那一行，粘贴执行；然后执行推送：

```bash
# 示例（实际地址以你 GitHub 页面显示的为准，不要照抄下面这行！）
git remote add origin https://github.com/你的用户名/nampt-axis-transcriptomics.git

git branch -M main
git push -u origin main
```

> 第一次 push 会弹窗要求登录 GitHub：
> - 方式一（推荐）：选 **"Sign in with your browser"**，浏览器自动打开，点 **Authorize** 授权即可
> - 方式二：选 **"Sign in with a token"** → 去 https://github.com/settings/tokens 生成一个 **classic token**（勾选 `repo` 权限）→ 粘贴回来
> - 方式三（备用）：如果弹窗没出现，GitHub 会提示用用户名 + 密码，但密码处要填 **token**（GitHub 已不支持密码直推）

### 2c. 验证上传成功

```bash
git status          # 应显示 "nothing to commit, working tree clean"
git remote -v       # 应显示 origin -> https://github.com/你的用户名/nampt-axis-transcriptomics.git
```

然后浏览器刷新你 GitHub 仓库页面，应能看到全部文件和 `README.md` 正常渲染。

---

## 第 3 步：检查 GitHub 仓库内容（约 3 分钟）

上传后打开仓库页面，确认这些都在（GitHub 网页左侧文件列表）：

- [ ] `scripts/`（21 个 .py + 1 个 .R）
- [ ] `data_audit/outputs/`（所有结果 CSV、图、报告）
- [ ] `README.md`（页面底部会自动渲染）
- [ ] `LICENSE`、`ARCHIVE_README.md`、`.zenodo.json`、`CITATION.cff`、`requirements.txt`
- [ ] 确认 **没有** `data_audit/downloads/`（原始 GEO 矩阵，按规定不重新分发）
- [ ] 确认 **没有** `__pycache__`、`.env`、任何 key 文件

> 如果看到不该出现的东西：在仓库页面删掉它，或本地 `git rm` 后重新 push（告诉我，我帮你）。

---

## 第 4 步：创建 Zenodo DOI（约 10–15 分钟）

Zenodo 的 DOI 机制：**先在 GitHub 建好仓库，再把 GitHub 仓库关联到 Zenodo**，Zenodo 自动抓取并分配 DOI。分两种路径：

### 路径 A：推荐 — 通过 GitHub 关联（自动抓取，最简单）

1. 打开 https://zenodo.org 并用 **GitHub 账号登录**（页面会引导 OAuth 授权；若没有账号，用 GitHub 登录即自动创建）
2. 登录后右上角头像 → **"GitHub"** 菜单（或直接访问 https://zenodo.org/account/settings/github/ ）
3. 页面列出你 GitHub 的所有仓库 → 找到 `nampt-axis-transcriptomics` → 把右侧开关 **拨到 ON**
4. 它会要求你确认启用，点 **Enable**（可能要求选择是否创建新版本等，保持默认即可）
5. 去你的 GitHub 仓库页面 → 顶部会多出 **"Create release"** 提示 → 点 **Releases** → **Create a new release**：
   - **Tag**：`v1.0.0`
   - **Title**：`Nampt-axis transcriptomics analysis — v1.0.0`
   - **Description**：可写 "Code and derived data for the NAMPT-axis manuscript"（可选）
   - 点 **Publish release**
6. 等 1–3 分钟，回到 Zenodo 的 GitHub 页面 → 你的仓库条目下会出现一个版本和 **DOI 徽章**（形如 `10.5281/zenodo.1234567`）
7. 点击 DOI 或徽章，进入 Zenodo 记录页，确认：
   - 标题、作者（4 位）、LICENSE (MIT) 已自动从仓库元数据读取
   - 若发现作者/描述不对：Zenodo 记录页点 **Edit** 手动修正后保存

### 路径 B：备用 — 直接上传（若不成功用 GitHub 关联）

1. 打开 https://zenodo.org → 右上角 **"Upload"**（绿色按钮）
2. **New upload** 页面：
   - **Type**：Software
   - **Title**：`State-dependent NAMPT-axis transcriptional programs in obesity and exercise (analysis code)`
   - **Authors**：逐条添加 — Chen, Yanjing；Shao, Zhenyu；Zhang, Min；Zhang, Yan
   - **Description**：粘贴 `.zenodo.json` 里的 description（或 ARCHIVE_README 开头一段）
   - **Access**：Public
   - **License**：MIT
   - **Files**：上传 zip（本地 `data_audit/outputs/NAMPT_manuscript_submission_pack_2026-09-20.zip`，或代码仓库 zip）
3. 点 **Submit** → 立刻获得 DOI

> 路径 A 更推荐：DOI 与 GitHub 版本自动绑定，以后更新代码只要发新 release，Zenodo 自动分配新 DOI。

---

## 第 5 步：把 URL / DOI 填回正文（约 5 分钟）

拿到两样东西后，告诉我（或自己改），填进正文 `data_audit/outputs/manuscript_full_en_v1.md` 的 3 处占位：

| 占位（原文） | 替换为 |
| --- | --- |
| `[GitHub repository URL to be provided upon archiving]`（第 185 行 Methods §7） | `https://github.com/你的用户名/nampt-axis-transcriptomics` |
| `[GitHub repository URL to be provided upon archiving]`（第 196 行 Code Availability） | 同上 |
| `DOI to be provided upon archiving`（第 185/193/196 行，共 3 处） | `10.5281/zenodo.XXXXXXXX` |

改完后再跑一遍数字/格式自检（我可以代劳），重新打包 zip 即可投稿。

---

## 常见问题（FAQ）

**Q1：push 时说 "remote origin already exists"？**
说明之前设置过远程。执行 `git remote set-url origin https://github.com/你的用户名/nampt-axis-transcriptomics.git` 再 push。

**Q2：push 报错 "failed to push some refs"？**
通常是远端有本地没有的提交（比如你勾了 README 初始化）。执行 `git pull origin main --rebase` 再 push。若已按第 1 步保持空仓库，不会遇到。

**Q3：Zenodo 页面没有出现我的仓库？**
确认：① 用 GitHub 登录的账号与仓库同一账号；② 仓库是 Public；③ 刷新 Zenodo 的 GitHub 设置页。GitHub 组织仓库需要在 Zenodo 单独授权。

**Q4：DOI 要等多久？**
release 发布后一般 1–3 分钟；Zenodo 高峰期可能 10 分钟。迟迟不出现可重新发一次 release 或联系 Zenodo 支持。

**Q5：上传后发现 key 泄漏怎么办？**
本仓库已复核零泄漏，但若未来发现任何疑似密钥：立即到 GitHub 仓库 Settings → Security → Secrets 处理 + 去 NVIDIA 后台吊销/重置该 key。告诉我，我帮你排查。

---

*本指南由 EvoX 为首次上传用户编写，2026-09-20。操作过程中任何一步卡住，把报错原文发给我即可。*
