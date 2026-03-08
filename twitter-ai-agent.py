#!/usr/bin/env python3
"""
Twitter AI Agent - مع AI Summary
يتابع ويحلل تغريدات المتداولين باستخدام AI
"""
import os
import json
from datetime import datetime
from typing import Dict, List

# Import our base agent
from twitter_agent import TwitterResearchAgent

class TwitterAIAgent(TwitterResearchAgent):
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.environ.get("KIMI_API_KEY")
        
    async def summarize_with_ai(self, content: str) -> str:
        """Use AI to summarize content"""
        if not self.api_key:
            return "AI API key not configured"
        
        # Simulated AI summary (replace with actual API call)
        prompt = f"""
قم بتحليل المحتوى التالي واستخرج:
1. الفكرة الرئيسية
2. المفاهيم المذكورة (ICT, SMC, Trading)
3. فرص التداول المحتملة

المحتوى:
{content}
"""
        
        # Return prompt for AI processing
        return prompt
    
    async def analyze_with_ai(self, url: str) -> Dict:
        """Full AI analysis of a link"""
        # First get basic info
        basic = await self.summarize_link(url)
        
        # Add AI analysis
        basic["ai_summary"] = await self.summarize_with_ai(url)
        
        # Determine trading signal
        basic["signal"] = self._extract_signal(basic)
        
        return basic
    
    def _extract_signal(self, analysis: Dict) -> str:
        """Extract trading signal from analysis"""
        concepts = analysis.get("ict_concepts_found", [])
        
        signals = {
            "bullish": ["bullish ob", "bsl", "demand", "long"],
            "bearish": ["bearish ob", "ssl", "supply", "short"],
            "neutral": []
        }
        
        concepts_str = " ".join(concepts).lower()
        
        for signal, keywords in signals.items():
            if any(kw in concepts_str for kw in keywords):
                return signal.upper()
        
        return "NEUTRAL"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitter AI Research Agent")
    parser.add_argument("--weekly", action="store_true", help="Weekly analysis")
    parser.add_argument("--link", type=str, help="Analyze link with AI")
    parser.add_argument("--ai", action="store_true", help="Use AI for analysis")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = TwitterAIAgent()
    
    if args.link:
        result = asyncio.run(agent.analyze_with_ai(args.link))
        
        print("""
📊 نتيجة التحليل بالـ AI
═══════════════════════════════

🔗 الرابط: {}
📍 المصدر: {}
📋 النوع: {}

🧠 المفاهيم المكتشفة:
{}

📡 الإشارة: {}

🤖 ملخص AI:
{}

═══════════════════════════════
""".format(
            result.get('url', 'N/A'),
            result.get('source', 'N/A'),
            result.get('content_type', 'N/A'),
            ', '.join(result.get('ict_concepts_found', [])) or 'None',
            result.get('signal', 'NEUTRAL'),
            result.get('ai_summary', 'AI not configured')[:500]
        ))
    
    else:
        print("""
🔧 Twitter AI Agent

الاستخدام:
  python twitter-ai-agent.py --link <url>   # تحليل رابط بالـ AI
  python twitter-ai-agent.py --weekly        # تحليل أسبوعي

💡 ميزات AI:
  - ملخص ذكي للمحتوى
  - استخراج إشارات التداول
  - تحليل المفاهيم ICT
""")


if __name__ == "__main__":
    import asyncio
    main()
