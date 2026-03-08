#!/usr/bin/env python3
"""
Twitter Research Agent
يتابع ويحلل تغريدات المتداولين المختارين
الاستخدام: python twitter-agent.py --weekly
         python twitter-agent.py --link <url>
"""
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import re

# Accounts المختارين (ICT Traders)
ICT_ACCOUNTS = {
    "Liq_Sniper": {
        "username": "Liq_Sniper",
        "focus": "Liquidity + Breaker Blocks",
        "topics": ["breaker", "liquidity", "order block", "ict"]
    },
    "ICT_Strategy": {
        "username": "ICT_Strategy", 
        "focus": "ICT Concepts",
        "topics": ["fvg", "order block", "mss", "sweep"]
    },
    "TheInnerCircle": {
        "username": "TheInnerCircle",
        "focus": "Michael Hudson - ICT",
        "topics": ["kill zone", "smart money", "ict"]
    },
    "TraderSeymour": {
        "username": "TraderSeymour",
        "focus": "SMC + Price Action",
        "topics": ["smc", "supply demand", "structure"]
    }
}

class TwitterResearchAgent:
    def __init__(self):
        self.accounts = ICT_ACCOUNTS
        self.analysis_results = []
        
    def load_config(self):
        """Load custom accounts from config"""
        config_path = "config/accounts.json"
        if os.path.exists(config_path):
            with open(config_path) as f:
                custom = json.load(f)
                self.accounts.update(custom)
    
    async def search_account_tweets(self, username: str, keywords: List[str]) -> List[Dict]:
        """Search for tweets from specific account"""
        results = []
        for kw in keywords:
            query = f"from:{username} {kw}"
            # Use web search (simulated)
            results.append({
                "account": username,
                "keyword": kw,
                "query": query,
                "status": "ready_for_search"
            })
        return results
    
    async def analyze_weekly(self) -> Dict:
        """Perform weekly analysis from all accounts"""
        print("📊 جاري تحليل Twitter الأسبوعي...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "accounts_analyzed": [],
            "key_findings": [],
            "market_sentiment": {},
            "trade_ideas": []
        }
        
        for name, info in self.accounts.items():
            tweets = await self.search_account_tweets(
                info["username"], 
                info["topics"]
            )
            
            analysis["accounts_analyzed"].append({
                "name": name,
                "username": info["username"],
                "focus": info["focus"],
                "tweets_found": len(tweets)
            })
        
        # Generate summary
        analysis["summary"] = self._generate_summary(analysis)
        
        return analysis
    
    def _generate_summary(self, analysis: Dict) -> str:
        """Generate AI summary from analysis"""
        summary = f"""
📊 Twitter Weekly Analysis - {analysis['timestamp']}

📌 Accounts Analyzed: {len(analysis['accounts_analyzed'])}

"""
        for acc in analysis["accounts_analyzed"]:
            summary += f"• @{acc['username']}: {acc['focus']} ({acc['tweets_found']} tweets)\n"
        
        return summary
    
    async def summarize_link(self, url: str) -> Dict:
        """Summarize content from a shared link"""
        print(f"📝 جاري تحليل الرابط: {url}")
        
        # Extract key info
        result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "source": self._extract_source(url),
            "content_type": self._detect_content_type(url),
            "summary": "",
            "key_points": [],
            "ict_concepts_found": [],
            "actionable_ideas": []
        }
        
        # Detect ICT concepts in URL
        result["ict_concepts_found"] = self._detect_ict_concepts(url)
        
        return result
    
    def _extract_source(self, url: str) -> str:
        """Extract source platform from URL"""
        sources = {
            "twitter.com": "Twitter/X",
            "x.com": "Twitter/X",
            "tradingview.com": "TradingView",
            "youtube.com": "YouTube",
            "tiktok.com": "TikTok",
            "instagram.com": "Instagram"
        }
        
        for domain, name in sources.items():
            if domain in url:
                return name
        return "Unknown"
    
    def _detect_content_type(self, url: str) -> str:
        """Detect type of content"""
        url_lower = url.lower()
        
        if "video" in url or "watch" in url:
            return "video"
        elif "chart" in url or "idea" in url:
            return "chart_idea"
        elif "article" in url or "blog" in url:
            return "article"
        else:
            return "tweet"
    
    def _detect_ict_concepts(self, text: str) -> List[str]:
        """Detect ICT concepts in text"""
        concepts = {
            "FVG": ["fvg", "fair value gap", "imbalance"],
            "Order Block": ["order block", "ob", "bullish ob", "bearish ob"],
            "Breaker Block": ["breaker", "breaker block"],
            "Liquidity": ["liquidity", "sweep", "sl", "bsl", "ssl"],
            "Kill Zone": ["kill zone", "london open", "ny open"],
            "MSS": ["mss", "market structure shift", "bos"],
            "CHOCH": ["choch", "change of character"],
            "SMT": ["smt", "synthetic market tf"]
        }
        
        found = []
        text_lower = text.lower()
        
        for concept, keywords in concepts.items():
            if any(kw in text_lower for kw in keywords):
                found.append(concept)
        
        return found
    
    def save_results(self, analysis: Dict, filename: str):
        """Save analysis to file"""
        os.makedirs("data", exist_ok=True)
        
        with open(f"data/{filename}", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"✅ تم حفظ التحليل في: data/{filename}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitter Research Agent")
    parser.add_argument("--weekly", action="store_true", help="Perform weekly analysis")
    parser.add_argument("--link", type=str, help="Analyze specific link")
    parser.add_argument("--accounts", type=str, help="Custom accounts JSON file")
    
    args = parser.parse_args()
    
    agent = TwitterResearchAgent()
    
    if args.accounts:
        # Load custom accounts
        if os.path.exists(args.accounts):
            with open(args.accounts) as f:
                custom = json.load(f)
                agent.accounts.update(custom)
    
    if args.weekly:
        # Weekly analysis
        analysis = await agent.analyze_weekly()
        
        # Save
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"twitter-weekly-{date_str}.json"
        agent.save_results(analysis, filename)
        
        # Print summary
        print(analysis["summary"])
        
    elif args.link:
        # Analyze specific link
        result = await agent.summarize_link(args.link)
        
        # Save
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"link-analysis-{date_str}.json"
        agent.save_results(result, filename)
        
        # Print summary
        print("""
📝 تحليل الرابط:
URL: {}
Source: {}
Type: {}

🧠 المفاهيم المكتشفة:
{}
""".format(
            result['url'],
            result['source'],
            result['content_type'],
            ', '.join(result['ict_concepts_found']) if result['ict_concepts_found'] else 'None'
        ))
    
    else:
        print("""
🔧 Twitter Research Agent

الاستخدام:
  python twitter-agent.py --weekly          # تحليل أسبوعي
  python twitter-agent.py --link <url>     # تحليل رابط
  
خيارات:
  --weekly          تحليل أسبوعي من كل الحسابات
  --link <url>     تحليل رابط معين
  --accounts <file> ملف الحسابات المخصصة
""")


if __name__ == "__main__":
    asyncio.run(main())
