# Glados-Automatic-Check-In-Script

用于 GLaDOS 自动签到获取积分的脚本。

## 功能

- 使用 requests 发送签到请求
- 支持 Cookie 配置
- 输出清晰的签到结果（成功 / 重复 / Cookie 失效 / 请求失败）
- 支持 Server酱 推送通知

## 使用方法

1. 安装依赖

```bash
pip install requests
```

2. 配置 Cookie（任选其一）

- 方式一：编辑 `glados_checkin.py` 中的 `COOKIE` 变量
- 方式二：设置环境变量 `GLaDOS_COOKIE`

3. （可选）配置 Server酱 推送

- 设置环境变量 `SERVER_CHAN_SENDKEY`

4. 运行脚本

```bash
python glados_checkin.py
```

## 说明

- 签到接口：`https://glados.one/api/user/checkin`
- 成功签到时会尝试从接口返回数据中解析账号余额/剩余天数并推送
- Cookie 失效或请求失败会推送提醒更新 Cookie
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
