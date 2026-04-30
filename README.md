# Glados-Automatic-Check-In-Script
用于glados自动签到获取积分的应用程序

## GitHub Actions 定时签到
已提供 `.github/workflows/checkin.yml`，每天北京时间早上 8 点自动运行（对应 UTC 00:00）。
如你的脚本文件名不是 `checkin.py`，请在工作流中将 `python checkin.py` 改为实际脚本路径。

## 配置 GLADOS_COOKIE Secrets（必需）
Actions 需要从仓库 Secrets 中读取 Cookie。请按以下步骤操作：
1. 打开 GitHub 仓库页面，进入 **Settings**。
2. 在左侧菜单中选择 **Secrets and variables** → **Actions**。
3. 点击 **New repository secret**。
4. 在 **Name** 中填写 `GLADOS_COOKIE`。
5. 在 **Secret** 中粘贴你的真实 Cookie 字符串（不要加引号、不要换行）。
6. 点击 **Add secret** 保存。

完成后，Actions 会自动把 `GLADOS_COOKIE` 注入到运行环境中，你的脚本就可以通过 `os.environ.get('GLADOS_COOKIE')` 读取到它。
