import hashlib
import re
from collections import defaultdict


def sanitize_seed(seed_keyword):
    cleaned = re.sub(r"[^a-zA-Z0-9\s\-]", "", seed_keyword or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    return cleaned[:80]


def stable_number(text, minimum, maximum):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    number = int(digest[:8], 16)
    return minimum + (number % (maximum - minimum + 1))


def classify_intent(keyword):
    if any(token in keyword for token in ["pricing", "cost", "buy", "hire", "near me", "consultant"]):
        return "Transactional"
    if any(token in keyword for token in ["best", "tools", "software", "platform", "service", "agency"]):
        return "Commercial"
    if any(token in keyword for token in ["dashboard", "system", "workflow", "automation"]):
        return "Operational"
    if any(token in keyword for token in ["how", "guide", "checklist", "examples", "strategy", "template"]):
        return "Informational"
    return "Exploratory"


def funnel_stage(intent):
    return {
        "Informational": "Top Funnel",
        "Exploratory": "Top Funnel",
        "Operational": "Middle Funnel",
        "Commercial": "Middle Funnel",
        "Transactional": "Bottom Funnel",
    }.get(intent, "Middle Funnel")


def competition_label(difficulty):
    if difficulty >= 70:
        return "High"
    if difficulty >= 45:
        return "Medium"
    return "Low"


def cluster_for_keyword(keyword):
    if any(token in keyword for token in ["tools", "software", "platform", "dashboard", "system"]):
        return "Platform Evaluation"
    if any(token in keyword for token in ["pricing", "cost", "service", "agency", "consultant", "hire"]):
        return "Buyer Intent"
    if any(token in keyword for token in ["guide", "how", "checklist", "examples", "template"]):
        return "Education And Enablement"
    if any(token in keyword for token in ["strategy", "workflow", "automation", "cloud", "ai"]):
        return "Operations Strategy"
    return "Core Demand"


def content_type(keyword, intent):
    if intent == "Transactional":
        return "Landing Page"
    if intent == "Commercial":
        return "Comparison Page"
    if "checklist" in keyword or "template" in keyword:
        return "Downloadable Resource"
    if intent == "Operational":
        return "Workflow Guide"
    return "Blog / Knowledge Article"


def calculate_opportunity(volume, difficulty, intent):
    volume_component = min(volume / 70, 45)
    difficulty_component = max(0, 35 - (difficulty * 0.35))
    intent_bonus = {
        "Transactional": 18,
        "Commercial": 15,
        "Operational": 13,
        "Informational": 9,
        "Exploratory": 7,
    }.get(intent, 8)

    score = round(volume_component + difficulty_component + intent_bonus)
    return max(1, min(score, 100))


def score_band(score):
    if score >= 75:
        return "High"
    if score >= 50:
        return "Medium"
    return "Low"


def priority_from_score(score, difficulty):
    if score >= 75 and difficulty < 65:
        return "P1 Revenue-Ready Opportunity"
    if score >= 60:
        return "P2 Build Content Cluster"
    if difficulty >= 70:
        return "P4 Long-Term Authority Bet"
    return "P3 Support Content"


def ai_workflow_status(score, intent):
    if score >= 75:
        return "Ready For AI Brief"
    if intent in {"Commercial", "Transactional"}:
        return "Human Review Recommended"
    return "Research Queue"


def forecast_visits(volume, difficulty, score):
    ctr_factor = 0.035
    difficulty_drag = max(0.35, 1 - (difficulty / 120))
    score_boost = 1 + (score / 220)
    return round(volume * ctr_factor * difficulty_drag * score_boost)


def generate_keyword_rows(seed, market, audience, content_goal):
    keyword_patterns = [
        "{seed}",
        "best {seed}",
        "{seed} tools",
        "{seed} software",
        "{seed} platform",
        "{seed} strategy",
        "{seed} checklist",
        "{seed} examples",
        "how to improve {seed}",
        "{seed} automation",
        "{seed} dashboard",
        "{seed} pricing",
        "{seed} workflow",
        "cloud {seed} solution",
        "ai {seed} planning",
        "{seed} content brief template",
    ]

    rows = []

    for pattern in keyword_patterns:
        keyword = pattern.format(seed=seed)
        intent = classify_intent(keyword)
        difficulty = stable_number(keyword + market, 24, 82)
        volume = stable_number(keyword + audience + content_goal, 320, 9700)
        score = calculate_opportunity(volume, difficulty, intent)

        rows.append(
            {
                "keyword": keyword.title(),
                "cluster": cluster_for_keyword(keyword),
                "intent": intent,
                "funnel_stage": funnel_stage(intent),
                "volume": volume,
                "competition": competition_label(difficulty),
                "difficulty": difficulty,
                "opportunity_score": score,
                "score_band": score_band(score),
                "forecast_visits": forecast_visits(volume, difficulty, score),
                "recommended_content_type": content_type(keyword, intent),
                "priority": priority_from_score(score, difficulty),
                "ai_workflow_status": ai_workflow_status(score, intent),
            }
        )

    return sorted(rows, key=lambda item: item["opportunity_score"], reverse=True)


def build_clusters(keywords):
    cluster_map = defaultdict(list)

    for row in keywords:
        cluster_map[row["cluster"]].append(row)

    clusters = []

    for cluster_name, items in cluster_map.items():
        total_volume = sum(item["volume"] for item in items)
        avg_score = round(sum(item["opportunity_score"] for item in items) / len(items))
        top_keyword = max(items, key=lambda item: item["opportunity_score"])

        clusters.append(
            {
                "name": cluster_name,
                "keyword_count": len(items),
                "total_volume": total_volume,
                "avg_opportunity": avg_score,
                "top_keyword": top_keyword["keyword"],
                "recommended_action": action_for_cluster(cluster_name, avg_score),
            }
        )

    return sorted(clusters, key=lambda item: item["avg_opportunity"], reverse=True)


def action_for_cluster(cluster_name, avg_score):
    if avg_score >= 75:
        return f"Build this {cluster_name.lower()} cluster first for near-term growth."
    if avg_score >= 55:
        return f"Add this {cluster_name.lower()} cluster to the next content sprint."
    return f"Keep this {cluster_name.lower()} cluster as supporting authority content."


def campaign_health_score(keywords):
    avg_opportunity = round(sum(row["opportunity_score"] for row in keywords) / len(keywords))
    avg_difficulty = round(sum(row["difficulty"] for row in keywords) / len(keywords))
    ready_for_ai = sum(1 for row in keywords if row["ai_workflow_status"] == "Ready For AI Brief")
    buyer_intent = sum(1 for row in keywords if row["intent"] in {"Commercial", "Transactional"})

    score = avg_opportunity + (ready_for_ai * 2) + (buyer_intent * 2) - max(0, avg_difficulty - 55)
    return max(1, min(round(score), 100))


def seo_risk_level(keywords):
    avg_difficulty = round(sum(row["difficulty"] for row in keywords) / len(keywords))
    high_competition = sum(1 for row in keywords if row["competition"] == "High")

    if avg_difficulty >= 68 or high_competition >= 7:
        return "High"
    if avg_difficulty >= 50 or high_competition >= 4:
        return "Medium"
    return "Low"


def build_campaign_recommendation(seed, keywords, clusters, summary):
    top_keyword = keywords[0]
    strongest_cluster = clusters[0]
    risk = seo_risk_level(keywords)
    health = campaign_health_score(keywords)

    if health >= 75 and risk != "High":
        verdict = "Launch First Content Sprint"
        executive_summary = f"Start with {top_keyword['keyword']} and build the {strongest_cluster['name']} cluster first."
    elif health >= 55:
        verdict = "Build Cluster With Review"
        executive_summary = f"Use {top_keyword['keyword']} as the lead asset, but review difficulty before scaling."
    else:
        verdict = "Research Before Production"
        executive_summary = f"Use {seed.title()} as a research theme before committing major content budget."

    first_sprint = [
        f"Publish one {top_keyword['recommended_content_type']} targeting {top_keyword['keyword']}.",
        f"Support it with two articles from the {strongest_cluster['name']} cluster.",
        "Move high-opportunity terms into the AI brief queue.",
        "Keep commercial pages under human review before publishing.",
    ]

    return {
        "verdict": verdict,
        "executive_summary": executive_summary,
        "best_starting_keyword": top_keyword["keyword"],
        "strongest_cluster": strongest_cluster["name"],
        "campaign_health": health,
        "seo_risk": risk,
        "first_sprint": first_sprint,
        "business_impact": f"Estimated organic traffic forecast: {summary['forecast']:,} monthly visits if the cluster gains traction.",
    }


def build_ai_brief(seed, market, audience, content_goal, keywords):
    top_keyword = keywords[0]
    commercial_terms = [item["keyword"] for item in keywords if item["intent"] in {"Commercial", "Transactional"}][:3]
    support_terms = [item["keyword"] for item in keywords if item["intent"] in {"Informational", "Operational"}][:4]

    return {
        "title": f"{seed.title()} Strategy Guide For {audience}",
        "target_market": market,
        "content_goal": content_goal,
        "primary_keyword": top_keyword["keyword"],
        "recommended_format": top_keyword["recommended_content_type"],
        "search_intent": top_keyword["intent"],
        "outline": [
            f"Define the main {seed} problem and why it matters.",
            "Show the workflow, operational risk, or business impact.",
            "Compare practical solutions and decision criteria.",
            "Add a checklist, dashboard view, or implementation plan.",
            "End with a conversion-focused next step."
        ],
        "commercial_terms": commercial_terms,
        "support_terms": support_terms,
        "ai_note": "This is a simulated AI-assisted brief for portfolio use. A production version could connect to keyword APIs, analytics platforms, and generative AI services."
    }


def build_cloud_pipeline(keywords):
    ready = sum(1 for item in keywords if item["ai_workflow_status"] == "Ready For AI Brief")
    review = sum(1 for item in keywords if item["ai_workflow_status"] == "Human Review Recommended")
    research = sum(1 for item in keywords if item["ai_workflow_status"] == "Research Queue")

    return [
        {
            "stage": "Keyword Intake API",
            "status": "Demo Ready",
            "detail": "Seed keyword transformed into structured opportunity data."
        },
        {
            "stage": "AI Brief Queue",
            "status": f"{ready} Ready",
            "detail": "High-opportunity terms can move into AI-assisted content briefs."
        },
        {
            "stage": "Human Review Gate",
            "status": f"{review} Needs Review",
            "detail": "Commercial terms should receive human review before publishing."
        },
        {
            "stage": "Research Backlog",
            "status": f"{research} Queued",
            "detail": "Lower-priority terms remain available for future content sprints."
        },
    ]


def build_security_panel(seed):
    return [
        {
            "control": "Input Sanitization",
            "status": "Active",
            "detail": f"Seed keyword processed as: {seed.title()}"
        },
        {
            "control": "No API Secrets In Repo",
            "status": "Protected",
            "detail": "Demo intelligence uses deterministic local scoring without stored provider credentials."
        },
        {
            "control": "Cloud Deployment Readiness",
            "status": "Planned",
            "detail": "Future version can connect to managed hosting, secret vaulting, cloud databases, and rate limits."
        },
        {
            "control": "Human Review Gate",
            "status": "Designed",
            "detail": "Commercial and transactional content is flagged for review before publishing automation."
        },
    ]


def build_campaign_summary(analysis):
    keywords = analysis["keywords"]
    total_volume = sum(row["volume"] for row in keywords)
    avg_difficulty = round(sum(row["difficulty"] for row in keywords) / len(keywords))
    avg_opportunity = round(sum(row["opportunity_score"] for row in keywords) / len(keywords))
    quick_wins = sum(1 for row in keywords if row["priority"] == "P1 Revenue-Ready Opportunity")
    forecast = sum(row["forecast_visits"] for row in keywords)

    return {
        "total_keywords": len(keywords),
        "total_volume": total_volume,
        "avg_difficulty": avg_difficulty,
        "avg_opportunity": avg_opportunity,
        "quick_wins": quick_wins,
        "forecast": forecast,
    }


def analyze_keywords(seed_keyword, market="Global", audience="Business decision makers", content_goal="Lead generation"):
    seed = sanitize_seed(seed_keyword) or "seo strategy"
    keywords = generate_keyword_rows(seed, market, audience, content_goal)
    clusters = build_clusters(keywords)
    base_summary = {
        "forecast": sum(row["forecast_visits"] for row in keywords),
    }

    analysis = {
        "keywords": keywords,
        "clusters": clusters,
        "ai_brief": build_ai_brief(seed, market, audience, content_goal, keywords),
        "cloud_pipeline": build_cloud_pipeline(keywords),
        "security_panel": build_security_panel(seed),
    }

    full_summary = build_campaign_summary(analysis)
    analysis["campaign_recommendation"] = build_campaign_recommendation(seed, keywords, clusters, full_summary)

    return analysis
