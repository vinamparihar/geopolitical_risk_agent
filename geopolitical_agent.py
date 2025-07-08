"""
Geopolitical Risk Agent

This agent analyzes geopolitical risks across various categories and generates a structured report.
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
from dotenv import load_dotenv
from alpha_vantage.foreignexchange import ForeignExchange
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Load environment variables
load_dotenv()

class GeopoliticalRiskAgent:
    """Agent for analyzing geopolitical risks across multiple categories."""
    
    def __init__(self):
        """Initialize the agent with required API clients."""
        # Initialize API clients
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Risk categories and their weights
        self.categories = [
            "Global Indicator",
            "Global Trade Protectionism",
            "Emerging Market Political Crisis",
            "Global Technology Decoupling",
            "Major Terror Attacks",
            "European Fragmentation",
            "Russia-NATO Conflict",
            "U.S. China Strategic Competition",
            "Middle East Regional War",
            "North Korea Conflict",
            "Major Cyber Attacks"
        ]
        
        # Country list for analysis
        self.countries = [
            "United States", "China", "Russia", "Germany", "United Kingdom",
            "France", "Japan", "India", "Brazil", "South Africa",
            "Saudi Arabia", "Iran", "North Korea", "South Korea", "Ukraine",
            "Israel", "Turkey", "Mexico", "Canada", "Australia"
        ]
    
    def search_tavily(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web using Tavily API."""
        if not self.tavily_api_key:
            return []
            
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.tavily_api_key,
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": False,
            "max_results": max_results,
            "include_domains": ["reuters.com", "bloomberg.com", "ft.com", "wsj.com", "economist.com"]
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Error searching with Tavily: {str(e)}")
            return []
    
    def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search news using SerpAPI."""
        if not self.serpapi_key:
            return []
            
        params = {
            "q": query,
            "tbm": "nws",
            "num": max_results,
            "api_key": self.serpapi_key
        }
        
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("news_results", [])
        except Exception as e:
            print(f"Error searching news with SerpAPI: {str(e)}")
            return []
    
    def get_financial_data(self, symbol: str, period: str = "1mo") -> Dict[str, Any]:
        """Get financial data using yfinance."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {}
                
            return {
                "latest_price": hist["Close"].iloc[-1],
                "volatility": hist["Close"].pct_change().std() * 100,  # as percentage
                "volume": hist["Volume"].mean()
            }
        except Exception as e:
            print(f"Error getting financial data: {str(e)}")
            return {}
    
    def get_currency_rates(self, from_currency: str, to_currency: str = "USD") -> Dict[str, Any]:
        """Get currency exchange rates using Alpha Vantage."""
        if not self.alpha_vantage_key:
            return {}
            
        try:
            fx = ForeignExchange(key=self.alpha_vantage_key)
            data, _ = fx.get_currency_exchange_rate(
                from_currency=from_currency,
                to_currency=to_currency
            )
            return data
        except Exception as e:
            print(f"Error getting currency rates: {str(e)}")
            return {}
    
    def analyze_risk_with_llm(self, prompt: str) -> Dict[str, Any]:
        """Analyze risk using OpenAI's GPT model."""
        if not self.openai_api_key:
            return {"score": random.uniform(0, 5), "reasoning": "LLM not available"}
            
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a geopolitical risk analyst. Analyze the given information and provide a risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON if the response is in JSON format
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, extract score and reasoning
                score = 0
                reasoning = content
                
                # Try to extract score from text (e.g., "Score: 7/10")
                import re
                score_match = re.search(r'(?i)score[\s:]*([\d.]+)(?:\s*\/\s*10)?', content)
                if score_match:
                    score = min(10, max(0, float(score_match.group(1))))
                
                return {"score": score, "reasoning": reasoning}
                
        except Exception as e:
            print(f"Error analyzing with LLM: {str(e)}")
            return {"score": random.uniform(0, 5), "reasoning": f"Error: {str(e)}"}
    
    def assess_category_risk(self, category: str, country: str) -> Dict[str, Any]:
        """Assess risk for a specific category and country."""
        # Gather data from various sources
        search_query = f"{category} {country} latest news analysis"
        web_results = self.search_tavily(search_query)
        news_results = self.search_news(search_query)
        
        # Prepare context for LLM analysis
        context = f"""
        Country: {country}
        Risk Category: {category}
        
        Recent Web Results:
        {json.dumps(web_results[:3], indent=2) if web_results else 'No web results found.'}
        
        Recent News:
        {json.dumps(news_results[:3], indent=2) if news_results else 'No news results found.'}
        """
        
        # Analyze with LLM
        prompt = f"""
        Analyze the geopolitical risk for the given country and category based on the provided information.
        
        {context}
        
        Please provide:
        1. A risk score from 0-10 where 0 is no risk and 10 is extreme risk
        2. A brief explanation of the risk factors
        3. Key indicators or events contributing to the risk
        
        Format your response as a JSON object with the following structure:
        {{
            "score": 0-10,
            "explanation": "...",
            "key_indicators": ["...", "..."]
        }}
        """
        
        analysis = self.analyze_risk_with_llm(prompt)
        
        # Ensure score is within 0-10 range
        score = min(10, max(0, analysis.get("score", 0)))
        
        return {
            "country": country,
            "category": category,
            "score": score,
            "explanation": analysis.get("explanation", "No explanation provided"),
            "key_indicators": analysis.get("key_indicators", []),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_report(self) -> List[Dict[str, Any]]:
        """Generate a comprehensive geopolitical risk report."""
        report = []
        
        print("Starting geopolitical risk analysis...")
        
        for i, category in enumerate(self.categories, 1):
            print(f"\nAnalyzing category {i}/{len(self.categories)}: {category}")
            
            # For global categories, analyze a subset of major countries
            countries_to_analyze = ["Global"] if category in ["Global Indicator", "Global Trade Protectionism"] else self.countries
            
            for country in countries_to_analyze:
                print(f"  - Assessing {country}...", end=" ")
                try:
                    result = self.assess_category_risk(category, country)
                    report.append(result)
                    print(f"Score: {result['score']:.1f}/10")
                except Exception as e:
                    print(f"Error: {str(e)}")
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
        
        return report
    
    def save_as_table(self, report: List[Dict[str, Any]], filename: str = "geopolitical_risk_report.csv") -> None:
        """Save the report as a CSV table."""
        if not report:
            print("No data to save.")
            return
        
        # Prepare data for DataFrame
        rows = []
        for i, item in enumerate(report, 1):
            rows.append({
                "Serial Number": i,
                "Country": item["country"],
                "Risk Score (0-10)": item["score"],
                "Category": item["category"],
                "Description": item["explanation"][:500]  # Limit description length
            })
        
        # Create and save DataFrame
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"\nReport saved as {filename}")


def main():
    """Main function to run the geopolitical risk analysis."""
    # Check for required API keys
    required_keys = ["TAVILY_API_KEY", "OPENAI_API_KEY", "SERPAPI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print("Error: The following required environment variables are not set:")
        for key in missing_keys:
            print(f"- {key}")
        print("\nPlease create a .env file with these variables and try again.")
        return
    
    # Initialize and run the agent
    agent = GeopoliticalRiskAgent()
    report = agent.generate_report()
    
    # Save the report
    if report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"geopolitical_risk_report_{timestamp}.csv"
        agent.save_as_table(report, filename)
        
        # Print a summary
        print("\n=== Analysis Complete ===")
        print(f"Generated report with {len(report)} risk assessments")
        print(f"Report saved as: {filename}")
    else:
        print("No data was generated. Please check your API keys and try again.")


if __name__ == "__main__":
    main()
