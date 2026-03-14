# 早安微信

每天早上自动发送早安问候到微信公众号

## 功能

- 🌤️ 天津天气查询
- 💕 结婚天数计算
- 🎂 生日倒计时
- 👔 穿衣指南
- 💌 每日寄言

## 配置

需要在 GitHub Secrets 中配置以下变量：

- `WECHAT_APPID` - 微信公众号 AppID
- `WECHAT_SECRET` - 微信公众号 AppSecret
- `TEMPLATE_ID` - 微信公众号模板 ID
- `USER_OPENID` - 接收者 OpenID

## 微信公众号模板

```
{{date.DATA}}

【今日天气】
天气：{{weather.DATA}}
最低气温：{{min_temp.DATA}}
最高气温：{{max_temp.DATA}}

【特殊日期】
💕 结婚第 {{marriage_days.DATA}} 天
🎂 距老婆生日还有 {{wife_days.DATA}} 天
🎂 距我生日还有 {{my_days.DATA}} 天

【穿衣指南】
{{clothing.DATA}}

【每日寄言】
{{quote.DATA}}
```

## 本地测试

```bash
pip install requests
python send_weixin.py
```
