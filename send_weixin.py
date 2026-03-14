#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import date, datetime

# ========== 配置区 ==========
WECHAT_APPID = "wx9d73e87308bda683"
WECHAT_SECRET = "8ba64b8e681e4dcce0d24fdc8f54937e"
TEMPLATE_ID = "你的模板ID"  # 需要填入微信公众号模板ID
USER_OPENID = "你的OpenID"  # 需要填入接收者的OpenID

# 日期配置
MARRIAGE_DATE = date(2022, 10, 5)
WIFE_BIRTHDAY = date(1990, 7, 24)
MY_BIRTHDAY = date(1992, 1, 27)
# ===========================

def get_weather():
    """获取天津天气"""
    try:
        url = "https://wttr.in/Tianjin?format=j1"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        today = data['weather'][0]
        
        temps = [int(h['tempC']) for h in today['hourly']]
        current = data['current_condition'][0]
        
        weather_desc = current['weatherDesc'][0]['value']
        min_temp = min(temps)
        max_temp = max(temps)
        
        return weather_desc, min_temp, max_temp
    except Exception as e:
        print(f"天气获取失败: {e}")
        return "晴", 4, 10

def get_access_token():
    """获取微信 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_SECRET}"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"获取token失败: {data}")

def send_template(token, openid, template_id, data):
    """发送模板消息"""
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    
    msg_data = {
        "touser": openid,
        "template_id": template_id,
        "data": {
            "date": {"value": data["date"]},
            "weather": {"value": data["weather"]},
            "min_temp": {"value": f"{data['min_temp']}°C"},
            "max_temp": {"value": f"{data['max_temp']}°C"},
            "marriage_days": {"value": str(data["marriage_days"])},
            "wife_days": {"value": str(data["wife_days"])},
            "my_days": {"value": str(data["my_days"])},
            "clothing": {"value": data["clothing"]},
            "quote": {"value": data["quote"]}
        }
    }
    
    resp = requests.post(url, json=msg_data, timeout=10)
    result = resp.json()
    if result.get("errcode") == 0:
        print("模板消息发送成功!")
    else:
        print(f"发送失败: {result}")

def calculate_days():
    """计算各种日期"""
    today = date.today()
    
    # 结婚天数
    marriage_days = (today - MARRIAGE_DATE).days
    
    # 距离老婆生日
    wife_bday_this_year = date(today.year, WIFE_BIRTHDAY.month, WIFE_BIRTHDAY.day)
    if today <= wife_bday_this_year:
        wife_days = (wife_bday_this_year - today).days
    else:
        wife_days = (date(today.year + 1, WIFE_BIRTHDAY.month, WIFE_BIRTHDAY.day) - today).days
    
    # 距离我的生日
    my_bday_this_year = date(today.year, MY_BIRTHDAY.month, MY_BIRTHDAY.day)
    if today <= my_bday_this_year:
        my_days = (my_bday_this_year - today).days
    else:
        my_days = (date(today.year + 1, MY_BIRTHDAY.month, MY_BIRTHDAY.day) - today).days
    
    return marriage_days, wife_days, my_days

def get_clothing_guide(min_temp, max_temp):
    """穿衣指南"""
    avg_temp = (min_temp + max_temp) / 2
    if avg_temp < 0:
        return "极寒天气，羽绒服 + 保暖内衣 + 围巾手套"
    elif avg_temp < 10:
        return "气温偏低，建议保暖内衣 + 厚外套，注意防寒"
    elif avg_temp < 20:
        return "早晚温差较大，建议薄外套 + 长袖"
    else:
        return "气温舒适，适合轻薄春装"

def get_quote():
    """每日寄言"""
    quotes = [
        "生活不是等待风暴过去，而是学会在雨中起舞。",
        "每一天都是新的开始，愿你保持好心情～",
        "简单的幸福，就是每天睁开眼看到阳光和你。",
        "心怀希望，脚步就会轻盈。",
        "珍惜当下，就是最好的生活态度。"
    ]
    import random
    return random.choice(quotes)

def main():
    print("=" * 40)
    print("🌤️ 每日问候自动发送")
    print("=" * 40)
    
    today = date.today()
    print(f"📅 日期: {today.strftime('%Y年%m月%d日')}")
    
    # 获取天气
    weather_desc, min_temp, max_temp = get_weather()
    print(f"🌤️ 天气: {weather_desc}")
    print(f"🌡️ 温度: {min_temp}°C ~ {max_temp}°C")
    
    # 计算日期
    marriage_days, wife_days, my_days = calculate_days()
    print(f"💕 结婚: 第{marriage_days}天")
    print(f"🎂 距老婆生日: {wife_days}天")
    print(f"🎂 距我生日: {my_days}天")
    
    # 穿衣指南
    clothing = get_clothing_guide(min_temp, max_temp)
    print(f"👔 穿衣: {clothing}")
    
    # 每日寄言
    quote = get_quote()
    print(f"💌 寄言: {quote}")
    
    # 发送模板消息
    print("\n📤 发送模板消息...")
    token = get_access_token()
    
    data = {
        "date": today.strftime('%Y年%m月%d日'),
        "weather": weather_desc,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "marriage_days": marriage_days,
        "wife_days": wife_days,
        "my_days": my_days,
        "clothing": clothing,
        "quote": quote
    }
    
    send_template(token, USER_OPENID, TEMPLATE_ID, data)
    print("✅ 完成!")

if __name__ == "__main__":
    main()
