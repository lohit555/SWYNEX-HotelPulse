import html
import base64
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from analyzer import (
    analyze_complaint,
    calculate_priority,
    PRIORITY_LEVELS,
)

MAX_HISTORY_ITEMS = 5
BACKGROUND_IMAGE = Path(__file__).parent / "assets" / "hotel-lobby-background.png"


@st.cache_data
def hotel_background_data_uri() -> str:
    """Load the local visual asset once for use in the app stylesheet."""

    encoded = base64.b64encode(BACKGROUND_IMAGE.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

st.set_page_config(
    page_title="HotelPulse | Complaint Analyzer",
    page_icon="🏨",
    layout="wide",
)

background_image = hotel_background_data_uri()

# -------------------- Styling --------------------

st.markdown(
    """
    <style>
    .stApp {
        background:
            linear-gradient(rgba(247, 249, 252, 0.52), rgba(247, 249, 252, 0.62)),
            url("__BACKGROUND_IMAGE__") center / cover fixed;
        color: #14213d;
    }

    .main-title {
        color: #14213d;
        font-size: 2.35rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #111827;
        font-size: 1rem;
        font-weight: 750;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        margin: 4px 0 24px 0;
    }

    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label {
        color: #14213d !important;
        font-weight: 800;
        font-size: 0.95rem;
    }

    div[data-testid="stSelectbox"],
    div[data-testid="stTextArea"] {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
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

    div[data-testid="stFormSubmitButton"] button {
        font-weight: 800;
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
        color: #111827 !important;
        font-weight: 700;
    }

    .category-card {
        min-height: 270px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .section-heading {
        color: #0b0f19 !important;
        font-size: 1.25rem;
        font-weight: 800;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        margin-bottom: 10px;
    }

    .section-text {
        color: #111827 !important;
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.65;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        overflow-wrap: anywhere;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        color: #14213d !important;
    }

    div[data-testid="stMarkdownContainer"] p {
        color: #111827;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
    }

    .action-card {
        background: #fff8e7;
        border-left: 4px solid #e8590c;
        border-radius: 10px;
        padding: 14px 16px;
        color: #36445d;
        line-height: 1.55;
    }

    </style>
    """.replace("__BACKGROUND_IMAGE__", background_image),
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


def suggested_action(analysis: dict, priority: dict) -> str:
    """Return a human-review recommendation from transparent rules."""

    if analysis["category"] == "Positive":
        return "No follow-up is required. You may share the positive feedback with the team."
    if analysis.get("safety_concern"):
        return "Escalate to the duty manager now and arrange an immediate safety check."
    if analysis.get("financial_impact"):
        return "Ask the front-desk or billing team to review the charge and update the guest promptly."
    if priority["level"] in {"High", "Critical"}:
        return "Assign this to the duty manager for prompt review and guest follow-up."
    return "Add this to the operations queue and confirm the next available resolution step."


def render_results(feedback: str, analysis: dict, priority: dict) -> None:
    """Render a consistent, review-friendly analysis record."""

    st.divider()
    st.subheader("Analysis Results")

    if analysis["category"] == "Positive":
        st.success("No actionable issue was detected. This feedback is classified as Positive.")
    else:
        st.info("AI-assisted triage only: a staff member should review this result before acting.")

    category_col, gauge_col = st.columns([1, 1.6])
    with category_col:
        category = html.escape(str(analysis["category"]))
        st.markdown(
            f'<div class="result-card category-card"><div class="card-label">Feedback Category</div>'
            f'<div class="card-value">{category}</div></div>',
            unsafe_allow_html=True,
        )
    with gauge_col:
        render_priority_gauge(priority["score"], priority["level"], priority["color"])

    st.markdown('<div class="section-heading">Recommended next step</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="action-card">{html.escape(suggested_action(analysis, priority))}</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="section-heading">📝 Feedback Summary</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-text">{html.escape(str(analysis.get("summary", "No summary provided.")))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown('<div class="section-heading">💡 Analysis Explanation</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-text">{html.escape(str(analysis.get("explanation", "No explanation provided.")))}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("View priority score breakdown"):
        st.write("The score uses a fixed rubric applied to indicators extracted by the AI.")
        for item in priority["breakdown"]:
            st.write(f"- {item}")
        bar_color = html.escape(str(priority["color"]))
        bar_width = max(0, min(100, int(priority["score"])))
        st.markdown(
            f'<div style="background:#e8edf4;border-radius:999px;height:10px;overflow:hidden;margin:10px 0;">'
            f'<div style="background:{bar_color};width:{bar_width}%;height:100%;"></div></div>',
            unsafe_allow_html=True,
        )
        st.caption("Prototype heuristic. Validate scores against manually reviewed feedback before relying on them.")

    with st.expander("View extracted indicators"):
        st.write(f'Severity: {analysis["severity"].title()}')
        st.write("Identified issue: " + ("Yes" if analysis["is_complaint"] else "No"))
        for label, field in [
            ("Safety concern", "safety_concern"),
            ("Urgent language", "urgent_language"),
            ("Financial impact", "financial_impact"),
            ("Multiple issues", "multiple_issues"),
        ]:
            st.write(f"{label}: {'Yes' if analysis.get(field) else 'No'}")

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

    st.divider()
    st.caption("Privacy reminder: do not enter names, booking references, or payment details.")

    if st.session_state.get("recent_analyses"):
        st.markdown("### Recent analyses")
        for item in st.session_state.recent_analyses:
            if st.button(
                f"{item['priority']['score']} · {item['analysis']['category']}",
                key=f"history_{item['id']}",
                help=item["feedback"],
                use_container_width=True,
            ):
                st.session_state.current_result = item


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

    _, button_col, _ = st.columns([4, 2, 4])
    with button_col:
        submitted = st.form_submit_button(
            "Analyze",
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

            result = {
                "id": datetime.now().isoformat(),
                "feedback": complaint.strip(),
                "analysis": analysis,
                "priority": priority,
            }
            st.session_state.current_result = result
            history = st.session_state.get("recent_analyses", [])
            st.session_state.recent_analyses = [result, *history][:MAX_HISTORY_ITEMS]

        except Exception as e:
            st.error("Could not analyze the guest feedback.")
            st.caption("Check your local Groq configuration and connection, then try again.")


if st.session_state.get("current_result"):
    current = st.session_state.current_result
    render_results(current["feedback"], current["analysis"], current["priority"])
