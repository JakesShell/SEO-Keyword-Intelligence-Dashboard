from flask import Flask, render_template, request, make_response
from io import StringIO
import csv

from utils import analyze_keywords, build_campaign_summary, sanitize_seed


app = Flask(__name__, template_folder='.')


@app.route('/styles.css')
def styles():
    with open('styles.css', 'r', encoding='utf-8') as css_file:
        response = make_response(css_file.read())
        response.headers['Content-Type'] = 'text/css'
        return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seed_keyword = sanitize_seed(request.form.get('seed_keyword', ''))
        market = request.form.get('market', 'Global').strip() or 'Global'
        audience = request.form.get('audience', 'Business decision makers').strip() or 'Business decision makers'
        content_goal = request.form.get('content_goal', 'Lead generation').strip() or 'Lead generation'

        if not seed_keyword:
            return render_template(
                'index.html',
                keywords=None,
                summary=None,
                clusters=None,
                ai_brief=None,
                cloud_pipeline=None,
                campaign_recommendation=None,
                security_panel=None,
                seed_keyword='',
                market=market,
                audience=audience,
                content_goal=content_goal,
                error='Please enter a seed keyword.'
            )

        analysis = analyze_keywords(seed_keyword, market, audience, content_goal)
        summary = build_campaign_summary(analysis)

        return render_template(
            'index.html',
            keywords=analysis['keywords'],
            summary=summary,
            clusters=analysis['clusters'],
            ai_brief=analysis['ai_brief'],
            cloud_pipeline=analysis['cloud_pipeline'],
            campaign_recommendation=analysis['campaign_recommendation'],
            security_panel=analysis['security_panel'],
            seed_keyword=seed_keyword,
            market=market,
            audience=audience,
            content_goal=content_goal,
            error=None
        )

    return render_template(
        'index.html',
        keywords=None,
        summary=None,
        clusters=None,
        ai_brief=None,
        cloud_pipeline=None,
        campaign_recommendation=None,
        security_panel=None,
        seed_keyword='',
        market='Global',
        audience='Business decision makers',
        content_goal='Lead generation',
        error=None
    )


@app.route('/download', methods=['POST'])
def download():
    seed_keyword = sanitize_seed(request.form.get('seed_keyword', ''))
    market = request.form.get('market', 'Global').strip() or 'Global'
    audience = request.form.get('audience', 'Business decision makers').strip() or 'Business decision makers'
    content_goal = request.form.get('content_goal', 'Lead generation').strip() or 'Lead generation'

    analysis = analyze_keywords(seed_keyword or 'seo strategy', market, audience, content_goal)
    keywords_data = analysis['keywords']

    output = StringIO()
    fieldnames = [
        'keyword',
        'cluster',
        'intent',
        'funnel_stage',
        'volume',
        'competition',
        'difficulty',
        'opportunity_score',
        'score_band',
        'forecast_visits',
        'recommended_content_type',
        'priority',
        'ai_workflow_status'
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for row in keywords_data:
        writer.writerow({field: row[field] for field in fieldnames})

    safe_name = seed_keyword.replace(' ', '-').lower() or 'searchops-keywords'
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={safe_name}-searchops-forecast.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


if __name__ == '__main__':
    app.run(debug=True)
