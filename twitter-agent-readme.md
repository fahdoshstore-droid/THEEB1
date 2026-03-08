# Twitter Research Agent 🤖

يتابع ويحلل تغريدات المتداولين المختارين

## الميزات

- 📊 **Weekly Analysis** - تحليل أسبوعي من كل الحسابات
- 🔗 **Link Analysis** - تحليل رابط معين
- 🧠 **ICT Concepts** - يكتشف مفاهيم ICT/SMC
- 📡 **Trading Signals** - يستخرج إشارات التداول

## الحسابات المختارة

| Account | التخصص |
|---------|--------|
| @Liq_Sniper | Liquidity + Breaker Blocks |
| @ICT_Strategy | ICT Concepts |
| @TheInnerCircle | Michael Hudson - ICT |
| @TraderSeymour | SMC + Price Action |
| @Paul_Trades | Price Action + ICT |

## الاستخدام

### تحليل رابط:
```bash
python twitter-agent.py --link https://x.com/Liq_Sniper/status/123456
```

### تحليل أسبوعي:
```bash
python twitter-agent.py --weekly
```

### مع AI:
```bash
python twitter-ai-agent.py --link <url>
```

## ملف الإعدادات

عدل `config/accounts.json` لإضافة حسابات جديدة:

```json
{
  "accounts": {
    "اسم_الحساب": {
      "username": "username",
      "focus": "التخصص",
      "topics": ["keyword1", "keyword2"]
    }
  }
}
```

## مثال على الناتج

```json
{
  "url": "https://x.com/.../status/123",
  "source": "Twitter/X",
  "content_type": "tweet",
  "ict_concepts_found": ["Breaker Block", "Liquidity", "Order Block"],
  "signal": "BEARISH"
}
```

## المتطلبات

```bash
pip install aiohttp requests
```

## المؤقت

--agent يشتغل يدوياً (مش تلقائي)
- يجمع من Web Search (ما يستخدم Twitter API)
- يحتاج AI API للملخص الذكي

---

🤖 Built for DHEEB Trading System
