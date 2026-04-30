#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict, Optional, Tuple

import requests

CHECKIN_URL = "https://glados.one/api/user/checkin"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

# 预留 Cookie 设置位置（也可使用环境变量 GLaDOS_COOKIE 覆盖）
COOKIE = ""


class CheckinResult:
    def __init__(
        self,
        status: str,
        message: str,
        raw: Optional[Dict[str, Any]] = None,
        account_info: Optional[str] = None,
    ) -> None:
        self.status = status
        self.message = message
        self.raw = raw or {}
        self.account_info = account_info


class GladosClient:
    def __init__(self, cookie: str, timeout: int = 10, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.cookie = cookie
        self.timeout = timeout
        self.user_agent = user_agent

    def _headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
            "Cookie": self.cookie,
        }

    def checkin(self) -> CheckinResult:
        payload = {"token": "glados.one"}
        try:
            response = requests.post(
                CHECKIN_URL,
                json=payload,
                headers=self._headers(),
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return CheckinResult("error", "请求超时，请检查网络连接。")
        except requests.exceptions.RequestException as exc:
            return CheckinResult("error", f"请求失败：{exc}")

        if response.status_code != 200:
            return CheckinResult("error", f"请求失败，状态码：{response.status_code}")

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError):
            return CheckinResult("error", "响应不是有效的 JSON 数据。")

        status, message = self._interpret_result(data)
        account_info = self._extract_account_info(data)
        return CheckinResult(status, message, raw=data, account_info=account_info)

    @staticmethod
    def _interpret_result(data: Dict[str, Any]) -> Tuple[str, str]:
        message = str(data.get("message") or data.get("msg") or "未知响应")
        code = data.get("code")
        msg_lower = message.lower()

        if code == 0:
            return "success", message
        if any(keyword in msg_lower for keyword in ["already", "repeat", "重复", "已签到"]):
            return "repeat", message
        if any(keyword in msg_lower for keyword in ["login", "token", "cookie", "unauthorized", "无效", "验证"]):
            return "auth_failed", message
        return "error", message

    @staticmethod
    def _extract_account_info(data: Dict[str, Any]) -> Optional[str]:
        info = []
        payload = data.get("data")
        if isinstance(payload, dict):
            key_map = {
                "leftDays": "剩余天数",
                "left_days": "剩余天数",
                "days": "剩余天数",
                "balance": "账号余额",
                "points": "积分",
                "score": "积分",
                "money": "账号余额",
            }
            for key, label in key_map.items():
                if key in payload and payload[key] is not None:
                    info.append(f"{label}: {payload[key]}")
        return "，".join(info) if info else None


class ServerChanNotifier:
    def __init__(self, send_key: str) -> None:
        self.send_key = send_key

    def send(self, title: str, content: str) -> bool:
        if not self.send_key:
            return False
        url = f"https://sctapi.ftqq.com/{self.send_key}.send"
        try:
            response = requests.post(url, data={"title": title, "desp": content}, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


def build_notifier() -> Optional[ServerChanNotifier]:
    send_key = os.getenv("SERVER_CHAN_SENDKEY", "").strip()
    if not send_key:
        return None
    return ServerChanNotifier(send_key)


def main() -> None:
    cookie = (os.getenv("GLADOS_COOKIE") or os.getenv("GLaDOS_COOKIE") or COOKIE or "").strip()
    if not cookie:
        print("未设置 Cookie，请在脚本中填写 COOKIE 或设置环境变量 GLADOS_COOKIE。")
        sys.exit(1)

    client = GladosClient(cookie=cookie)
    result = client.checkin()

    notifier = build_notifier()
    if result.status == "success":
        info = result.account_info or "未获取到账户信息。"
        message = f"签到成功：{result.message}\n{info}"
        print(message)
        if notifier:
            notifier.send("GLaDOS 签到成功", message)
    elif result.status == "repeat":
        message = f"重复签到：{result.message}"
        print(message)
        if notifier:
            notifier.send("GLaDOS 重复签到", message)
    elif result.status == "auth_failed":
        message = f"Cookie 验证失败：{result.message}\n请更新 Cookie。"
        print(message)
        if notifier:
            notifier.send("GLaDOS Cookie 失效", message)
    else:
        message = f"签到失败：{result.message}"
        print(message)
        if notifier:
            notifier.send("GLaDOS 签到失败", message)


if __name__ == "__main__":
    main()
