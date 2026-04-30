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
