from pathlib import Path
import re

index_path = Path("index.html")
css_path = Path("styles.css")

index_text = index_path.read_text(encoding="utf-8")
css_text = css_path.read_text(encoding="utf-8")

old_hero_console = r'''                <aside class="hero-console">
                    <div class="console-pulse"></div>
                    <p class="eyebrow">Campaign Health</p>
                    {% if campaign_recommendation %}
                        <strong>{{ campaign_recommendation.campaign_health }}%</strong>
                        <span>{{ campaign_recommendation.verdict }}</span>
                    {% else %}
                        <strong>AI</strong>
                        <span>Search intelligence prepared for cloud deployment and AI-assisted workflows</span>
                    {% endif %}
                </aside>'''

new_hero_console = r'''                <aside class="hero-console">
                    <div class="ai-search-visual" aria-hidden="true">
                        <div class="scan-grid"></div>
                        <div class="scan-beam"></div>

                        <div class="ai-core">
                            <span></span>
                            <strong>AI</strong>
                        </div>

                        <div class="orbit orbit-one">
                            <i></i>
                        </div>

                        <div class="orbit orbit-two">
                            <i></i>
                        </div>

                        <div class="orbit orbit-three">
                            <i></i>
                        </div>

                        <div class="signal-chip chip-one">Intent</div>
                        <div class="signal-chip chip-two">Forecast</div>
                        <div class="signal-chip chip-three">Cluster</div>
                    </div>

                    <div class="console-copy">
                        <p class="eyebrow">Campaign Health</p>
                        {% if campaign_recommendation %}
                            <strong>{{ campaign_recommendation.campaign_health }}%</strong>
                            <span>{{ campaign_recommendation.verdict }}</span>
                        {% else %}
                            <strong>AI Search</strong>
                            <span>Scanning keyword signals, clustering demand, and preparing cloud-ready content workflows.</span>
                        {% endif %}
                    </div>
                </aside>'''

if old_hero_console not in index_text:
    raise SystemExit("Could not find the hero console block. No changes made.")

index_text = index_text.replace(old_hero_console, new_hero_console)

css_text = re.sub(
    r'''\.hero-copy h2 \{
    max-width: 980px;
    margin-bottom: 18px;
    font-size: clamp\(2\.4rem, 5\.2vw, 5\.8rem\);
    line-height: 0\.94;
    letter-spacing: -0\.075em;
\}''',
    '''.hero-copy h2 {
    max-width: 930px;
    margin-bottom: 22px;
    font-size: clamp(2.55rem, 4.55vw, 5.05rem);
    line-height: 1.03;
    letter-spacing: -0.055em;
    text-wrap: balance;
}''',
    css_text
)

css_text = re.sub(
    r'''\.hero-grid \{
    display: grid;
    grid-template-columns: 1\.45fr 0\.7fr;
    gap: 28px;
\}''',
    '''.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(360px, 0.68fr);
    gap: 32px;
    align-items: stretch;
}''',
    css_text
)

css_text = re.sub(
    r'''\.hero-console \{
    position: relative;
    overflow: hidden;
    display: grid;
    align-content: end;
    min-height: 430px;
    padding: 28px;
    border-radius: 28px;
    color: #ffffff;
    background:
        radial-gradient\(circle at 25% 20%, rgba\(255, 255, 255, 0\.26\), transparent 30%\),
        linear-gradient\(145deg, #0d344a, #2f82a7\);
\}''',
    '''.hero-console {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-rows: 1fr auto;
    min-height: 430px;
    padding: 28px;
    border-radius: 28px;
    color: #ffffff;
    background:
        radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.24), transparent 32%),
        radial-gradient(circle at 78% 18%, rgba(140, 215, 239, 0.24), transparent 28%),
        linear-gradient(145deg, #0d344a, #2f82a7);
}''',
    css_text
)

css_text = re.sub(
    r'''\.console-pulse \{
    position: absolute;
    top: 32px;
    right: 34px;
    width: 150px;
    height: 150px;
    border-radius: 999px;
    border: 18px solid rgba\(255, 255, 255, 0\.18\);
    animation: pulseRing 2\.7s ease-in-out infinite;
\}''',
    '''.console-pulse {
    display: none;
}''',
    css_text
)

extra_css = r'''

.ai-search-visual {
    position: relative;
    min-height: 250px;
    margin-bottom: 24px;
    border-radius: 26px;
    overflow: hidden;
    background:
        radial-gradient(circle at center, rgba(255, 255, 255, 0.16), transparent 34%),
        linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.scan-grid {
    position: absolute;
    inset: 0;
    opacity: 0.32;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(circle at center, black, transparent 72%);
}

.scan-beam {
    position: absolute;
    inset: -40%;
    background: conic-gradient(
        from 0deg,
        transparent 0deg,
        transparent 290deg,
        rgba(255, 255, 255, 0.34) 320deg,
        transparent 350deg,
        transparent 360deg
    );
    animation: rotateScan 4.8s linear infinite;
}

.ai-core {
    position: absolute;
    top: 50%;
    left: 50%;
    display: grid;
    place-items: center;
    width: 118px;
    height: 118px;
    border-radius: 999px;
    transform: translate(-50%, -50%);
    background:
        radial-gradient(circle at 35% 28%, rgba(255, 255, 255, 0.82), rgba(255, 255, 255, 0.16) 24%, rgba(11, 38, 55, 0.84) 72%);
    box-shadow:
        0 0 0 18px rgba(255, 255, 255, 0.08),
        0 0 0 42px rgba(255, 255, 255, 0.045),
        0 28px 70px rgba(0, 0, 0, 0.22);
    animation: corePulse 2.4s ease-in-out infinite;
}

.ai-core span {
    position: absolute;
    inset: -18px;
    border-radius: inherit;
    border: 1px dashed rgba(255, 255, 255, 0.35);
    animation: rotateScan 8s linear infinite reverse;
}

.ai-core strong {
    margin: 0;
    font-size: 2rem;
    letter-spacing: -0.06em;
}

.orbit {
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.16);
    transform: translate(-50%, -50%);
}

.orbit i {
    position: absolute;
    top: -6px;
    left: 50%;
    width: 12px;
    height: 12px;
    border-radius: 999px;
    background: #ffffff;
    box-shadow: 0 0 18px rgba(255, 255, 255, 0.9);
}

.orbit-one {
    width: 178px;
    height: 178px;
    animation: rotateScan 7s linear infinite;
}

.orbit-two {
    width: 226px;
    height: 226px;
    animation: rotateScan 10s linear infinite reverse;
}

.orbit-three {
    width: 278px;
    height: 278px;
    animation: rotateScan 14s linear infinite;
}

.signal-chip {
    position: absolute;
    padding: 8px 11px;
    border-radius: 999px;
    color: rgba(255, 255, 255, 0.9);
    background: rgba(11, 38, 55, 0.46);
    border: 1px solid rgba(255, 255, 255, 0.12);
    font-size: 0.72rem;
    font-weight: 950;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    backdrop-filter: blur(14px);
    animation: chipFloat 3.4s ease-in-out infinite alternate;
}

.chip-one {
    top: 24px;
    left: 22px;
}

.chip-two {
    right: 24px;
    top: 82px;
    animation-delay: 0.4s;
}

.chip-three {
    left: 36px;
    bottom: 28px;
    animation-delay: 0.8s;
}

.console-copy {
    position: relative;
    z-index: 2;
}

.hero-console .console-copy strong {
    display: block;
    margin-bottom: 8px;
    font-size: clamp(2.5rem, 4.2vw, 4.65rem);
    letter-spacing: -0.075em;
    line-height: 0.95;
}

.hero-console .console-copy span {
    display: block;
    max-width: 320px;
    color: rgba(255, 255, 255, 0.78);
    line-height: 1.55;
}

@keyframes rotateScan {
    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

.scan-beam {
    transform-origin: center;
}

@keyframes corePulse {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        filter: brightness(1);
    }
    50% {
        transform: translate(-50%, -50%) scale(1.055);
        filter: brightness(1.16);
    }
}

@keyframes chipFloat {
    from {
        transform: translateY(0);
        opacity: 0.72;
    }
    to {
        transform: translateY(-8px);
        opacity: 1;
    }
}

@media (max-width: 1180px) {
    .hero-grid {
        grid-template-columns: 1fr;
    }

    .ai-search-visual {
        min-height: 280px;
    }
}

@media (max-width: 760px) {
    .hero-copy h2 {
        font-size: 2.55rem;
        line-height: 1.05;
        letter-spacing: -0.045em;
    }

    .ai-search-visual {
        min-height: 240px;
    }

    .orbit-three {
        width: 238px;
        height: 238px;
    }
}
'''

if ".ai-search-visual" not in css_text:
    css_text += extra_css

index_path.write_text(index_text, encoding="utf-8")
css_path.write_text(css_text, encoding="utf-8")

print("SearchOps hero typography and AI scanning console updated.")
