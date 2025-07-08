# Geopolitical Risk Agent

A standalone agent for analyzing geopolitical risks across various categories and generating structured reports.

## Features

- Analyzes 11 different geopolitical risk categories
- Gathers data from multiple sources (Tavily, SerpAPI, Alpha Vantage, Yahoo Finance)
- Uses AI to assess risk levels (0-10) for each category and country
- Generates comprehensive CSV reports
- Easy to extend with additional data sources or risk categories

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your API keys:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   OPENAI_API_KEY=your_openai_api_key
   SERPAPI_API_KEY=your_serpapi_key
   ```

## Usage

Run the agent with:
```bash
python geopolitical_agent.py
```

The agent will:
1. Analyze each risk category for relevant countries
2. Generate a detailed report in CSV format
3. Save the report as `geopolitical_risk_report_YYYYMMDD_HHMMSS.csv`

## Risk Categories

1. Global Indicator
2. Global Trade Protectionism
3. Emerging Market Political Crisis
4. Global Technology Decoupling
5. Major Terror Attacks
6. European Fragmentation
7. Russia-NATO Conflict
8. U.S. China Strategic Competition
9. Middle East Regional War
10. North Korea Conflict
11. Major Cyber Attacks

## Report Format

The generated CSV report will contain the following columns:
- Serial Number
- Country
- Risk Score (0-10)
- Category
- Description (summary of risk factors)

## Dependencies

- Python 3.8+
- See `requirements.txt` for Python package dependencies

## License

MIT
