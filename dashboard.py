import html

import streamlit as st
import streamlit.components.v1 as components

from analyzer import (
    analyze_complaint,
    calculate_priority,
    PRIORITY_LEVELS,
)

st.set_page_config(
    page_title="HotelPulse | Complaint Analyzer",
    page_icon="🏨",
    layout="wide",
)

# -------------------- Styling --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #f7f9fc;
        color: #14213d;
    }

    .main-title {
        color: #14213d;
        font-size: 2.35rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #53627c;
        font-size: 1rem;
        margin: 4px 0 24px 0;
    }

    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label {
        color: #14213d !important;
        font-weight: 600;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #262730 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
        border: 1px solid #d0d7e2;
        border-radius: 10px;
        opacity: 1 !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder {
        color: #c3c8d4 !important;
        -webkit-text-fill-color: #c3c8d4 !important;
        opacity: 1 !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border: 1px solid #ff4b4b !important;
        box-shadow: 0 0 0 1px #ff4b4b !important;
        outline: none !important;
    }

    .result-card {
        background: #ffffff;
        color: #14213d;
        border: 1px solid #e3e9f2;
        border-radius: 16px;
        padding: 22px;
        min-height: 145px;
        box-shadow: 0 3px 12px rgba(20, 33, 61, 0.04);
    }

    .card-label {
        color: #53627c;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .card-value {
        color: #14213d;
        font-size: 1.5rem;
        font-weight: 750;
        overflow-wrap: anywhere;
    }

    div[data-testid="stExpander"] details {
        background: #ffffff !important;
        border: 1px solid #e3e9f2 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stExpander"] summary {
        background: #ffffff !important;
        border-radius: 12px;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span {
        color: #14213d !important;
        font-weight: 600;
    }

    div[data-testid="stExpander"] summary svg {
        color: #14213d !important;
        fill: #14213d !important;
    }

    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stExpander"] li {
        color: #36445d !important;
    }

    .category-card {
        min-height: 270px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .section-heading {
        color: #14213d !important;
        font-size: 1.25rem;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .section-text {
        color: #36445d !important;
        font-size: 1rem;
        line-height: 1.65;
        overflow-wrap: anywhere;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        color: #14213d !important;
    }

    div[data-testid="stMarkdownContainer"] p {
        color: #36445d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- Priority Gauge --------------------

def render_priority_gauge(score: int, level: str, color: str) -> None:
    """Render a semicircular priority gauge in an HTML component."""

    score = max(0, min(100, int(score)))
    safe_color = html.escape(color)
    safe_level = html.escape(level)

    # Legend uses the same colors as PRIORITY_LEVELS so everything matches.
    legend_items = "".join(
        '<span class="legend-item">'
        f'<i class="dot" style="background:{html.escape(item["color"])}"></i>'
        f'{html.escape(item["name"])}'
        "</span>"
        for item in PRIORITY_LEVELS
    )

    gauge_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: transparent;
            }}

            .gauge-card {{
                background: #ffffff;
                border: 1px solid #e3e9f2;
                border-radius: 16px;
                padding: 16px 12px;
                text-align: center;
                color: #14213d;
            }}

            .gauge-title {{
                font-size: 16px;
                font-weight: 700;
                color: #53627c;
                margin-bottom: 4px;
            }}

            .gauge-svg {{
                display: block;
                width: 100%;
                max-width: 320px;
                height: auto;
                margin: 0 auto;
            }}

            .score {{
                font-size: 36px;
                font-weight: 800;
                fill: #14213d;
            }}

            .out-of {{
                font-size: 16px;
                fill: #53627c;
            }}

            .level {{
                font-size: 17px;
                font-weight: 800;
            }}

            .minmax {{
                font-size: 12px;
                fill: #7a879b;
            }}

            .legend {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 8px 12px;
                font-size: 12px;
                color: #53627c;
                margin-top: 6px;
            }}

            .legend-item {{
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }}

            .dot {{
                width: 9px;
                height: 9px;
                border-radius: 50%;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="gauge-card">
            <div class="gauge-title">Priority Score</div>

            <svg class="gauge-svg" viewBox="0 0 300 175"
                 role="img"
                 aria-label="Priority score {score} out of 100, {safe_level}">

                <path d="M 35 125 A 115 115 0 0 1 265 125"
                      fill="none"
                      stroke="#e8edf4"
                      stroke-width="20"
                      stroke-linecap="butt"/>

                <path d="M 35 125 A 115 115 0 0 1 265 125"
                      fill="none"
                      stroke="{safe_color}"
                      stroke-width="20"
                      stroke-linecap="butt"
                      pathLength="100"
                      stroke-dasharray="{score} 100"/>

                <text x="35" y="149"
                      text-anchor="middle"
                      class="minmax">0</text>

                <text x="265" y="149"
                      text-anchor="middle"
                      class="minmax">100</text>

                <text x="150" y="102" text-anchor="middle">
                    <tspan class="score">{score}</tspan><tspan
                        class="out-of" dx="4">/100</tspan>
                </text>

                <text x="150" y="132"
                      text-anchor="middle"
                      class="level"
                      fill="{safe_color}">{safe_level}</text>
            </svg>

            <div class="legend">{legend_items}</div>
        </div>
    </body>
    </html>
    """

    components.html(
        gauge_html,
        height=300,
        scrolling=False,
    )


# -------------------- Sidebar --------------------

with st.sidebar:
    st.markdown("## 🏨 HotelPulse")
    st.caption("AI-Powered Complaint Classification & Prioritization")
    st.divider()

    st.markdown("### Priority guide")

    for item in PRIORITY_LEVELS:
        st.markdown(
            f"""
            <div style="
                background:{item['background']};
                color:{item['color']};
                padding:10px 12px;
                border-radius:9px;
                margin-bottom:8px;
                font-weight:700;">
                {item['name']} · {item['minimum']}-{item['maximum']}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------- Main Dashboard --------------------

st.markdown(
    '<div class="main-title">Analyze Guest Feedback</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Identify guest feedback categories and prioritize issues "
    "that may need hotel staff attention."
    "</div>",
    unsafe_allow_html=True,
)

examples = {
    "Choose an example...": "",
    "Positive feedback": "I love the place!",
    "Positive feedback with a minor issue": (
        "I love the place, but heard some noise."
    ),
    "Cleanliness complaint": (
        "The bathroom was dirty, there was hair in the shower, "
        "and the bedsheets looked used."
    ),
    "Billing complaint": (
        "I was charged twice for the same night and still have not "
        "received a refund after contacting reception."
    ),
    "Safety complaint": (
        "There is exposed electrical wiring near the bathroom sink. "
        "I reported it, but nobody has checked it."
    ),
    "Noise complaint": (
        "Loud construction noise outside my room kept me awake until 2 AM."
    ),
    "Food complaint": (
        "The breakfast was cold, and several advertised menu items "
        "were unavailable."
    ),
}

selected_example = st.selectbox(
    "Try a sample review",
    list(examples.keys()),
)

with st.form("complaint_form"):
    complaint = st.text_area(
        "Guest feedback",
        value=examples[selected_example],
        placeholder="Describe the guest's hotel experience...",
        height=140,
        max_chars=4000,
        help=(
            "Avoid entering names, booking numbers, or other "
            "personal information."
        ),
    )

    submitted = st.form_submit_button(
        "🔎 Analyze Feedback",
        type="primary",
        use_container_width=True,
    )


# -------------------- Analysis Results --------------------

if submitted:
    if not complaint.strip():
        st.warning("Please enter guest feedback before analyzing it.")

    else:
        try:
            with st.spinner("Analyzing guest feedback with Groq..."):
                analysis = analyze_complaint(complaint.strip())
                priority = calculate_priority(analysis)

            st.divider()
            st.subheader("Analysis Results")

            if analysis["category"] == "Positive":
                st.success(
                    "No actionable issue was detected. "
                    "This feedback is classified as Positive."
                )
            else:
                st.info(
                    "A potential issue was detected. Even minor issues "
                    "are categorized and assigned at least Low priority."
                )

            category_col, gauge_col = st.columns([1, 1.6])

            with category_col:
                category = html.escape(str(analysis["category"]))

                st.markdown(
                    f"""
                    <div class="result-card category-card">
                        <div class="card-label">Feedback Category</div>
                        <div class="card-value">{category}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with gauge_col:
                render_priority_gauge(
                    priority["score"],
                    priority["level"],
                    priority["color"],
                )

            with st.container(border=True):
                st.markdown(
                    '<div class="section-heading">'
                    '📝 Feedback Summary</div>',
                    unsafe_allow_html=True,
                )

                summary = html.escape(
                    str(analysis.get("summary", "No summary provided."))
                )
                st.markdown(
                    f'<div class="section-text">{summary}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown("---")

                st.markdown(
                    '<div class="section-heading">'
                    '💡 Analysis Explanation</div>',
                    unsafe_allow_html=True,
                )

                explanation = html.escape(
                    str(
                        analysis.get(
                            "explanation",
                            "No explanation provided.",
                        )
                    )
                )
                st.markdown(
                    f'<div class="section-text">{explanation}</div>',
                    unsafe_allow_html=True,
                )

            with st.expander("View priority score breakdown"):
                st.write(
                    "The score uses a fixed rubric applied to the "
                    "indicators extracted by the AI."
                )

                for item in priority["breakdown"]:
                    st.write(f"- {item}")

                bar_color = html.escape(str(priority["color"]))
                bar_width = max(0, min(100, int(priority["score"])))
                st.markdown(
                    f"""
                    <div style="background:#e8edf4;border-radius:999px;
                                height:10px;overflow:hidden;margin:10px 0;">
                        <div style="background:{bar_color};width:{bar_width}%;
                                    height:100%;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    "Prototype heuristic. Validate scores against "
                    "manually reviewed feedback before relying on them."
                )

            with st.expander("View extracted indicators"):
                st.write(f'Severity: {analysis["severity"].title()}')
                st.write(
                    "Identified issue: "
                    + ("Yes" if analysis["is_complaint"] else "No")
                )

                indicators = [
                    ("Safety concern", "safety_concern"),
                    ("Urgent language", "urgent_language"),
                    ("Financial impact", "financial_impact"),
                    ("Multiple issues", "multiple_issues"),
                ]

                for label, field in indicators:
                    value = "Yes" if analysis.get(field) else "No"
                    st.write(f"{label}: {value}")

        except Exception as e:
            st.error("Could not analyze the guest feedback.")
            st.code(f"{type(e).__name__}: {e}")