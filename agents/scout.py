def analyze_context(context: dict) -> str:
    summary = f"""
Weather Update:
{context['weather']}

Finance Update:
{context['finance']}

Top Headline:
{context['news']}
"""
    return summary
