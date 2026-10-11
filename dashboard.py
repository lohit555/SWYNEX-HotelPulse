
import html

import streamlit as st

from analyzer import analyze_complaint, calculate_priority, PRIORITY_LEVELS

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

    /* Make form labels visible */
    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label {
        color: #14213d !important;
        font-weight: 600;
    }

    /* Fix complaint text visibility */
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
        min-height: 150px;
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

    .priority-pill {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: 800;
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
    }

    /* Keep analysis text readable */
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
    st.caption("Built with Python, Streamlit and Groq.")
    st.caption("AI-generated results require human review.")

# -------------------- Main dashboard --------------------

st.markdown(
    '<div class="main-title">Analyze a Guest Complaint</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Classify guest feedback and identify issues that may need attention."
    "</div>",
    unsafe_allow_html=True,
)

examples = {
    "Choose an example...": "",
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
    "Try a sample complaint",
    list(examples.keys()),
)

with st.form("complaint_form"):
    complaint = st.text_area(
        "Guest complaint",
        value=examples[selected_example],
        placeholder="Describe the guest's hotel experience...",
        height=140,
        max_chars=4000,
        help="Avoid entering names, booking numbers, or other personal information.",
    )

    submitted = st.form_submit_button(
        "🔎 Analyze Complaint",
        type="primary",
        use_container_width=True,
    )

# -------------------- Analysis results --------------------

if submitted:
    if not complaint.strip():
        st.warning("Please enter a complaint before analyzing it.")

    else:
        try:
            with st.spinner("Analyzing complaint with Groq..."):
                analysis = analyze_complaint(complaint.strip())

            st.divider()
            st.subheader("Analysis Results")

            if not analysis.get("is_complaint", False):
                st.info(
                    "This text was not identified as a hotel complaint "
                    "or review. Please check the input."
                )
                st.write(
                    analysis.get("explanation", "No explanation provided.")
                )

            else:
                priority = calculate_priority(analysis)

                category_col, score_col, level_col = st.columns(3)

                with category_col:
                    category = html.escape(str(analysis["category"]))

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="card-label">Complaint Category</div>
                            <div class="card-value">{category}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with score_col:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="card-label">Priority Score</div>
                            <div class="card-value">
                                {priority['score']}/100
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with level_col:
                    level = html.escape(str(priority["level"]))
                    color = html.escape(str(priority["color"]))
                    background = html.escape(str(priority["background"]))
                    description = html.escape(str(priority["description"]))

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="card-label">Priority Level</div>
                            <span class="priority-pill"
                                style="background:{background};color:{color};">
                                {level}
                            </span>
                            <p style="color:#53627c;margin-top:12px;">
                                {description}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Complaint summary and explanation
                with st.container(border=True):
                    st.markdown(
                        '<div class="section-heading">'
                        '📝 Complaint Summary</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="section-text">'
                        f'{html.escape(str(analysis.get("summary", "No summary provided.")))}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown("---")

                    st.markdown(
                        '<div class="section-heading">'
                        '💡 Analysis Explanation</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="section-text">'
                        f'{html.escape(str(analysis.get("explanation", "No explanation provided.")))}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                with st.expander("View priority score breakdown"):
                    st.write(
                        "The score uses a fixed rubric applied to the "
                        "indicators extracted by the AI."
                    )

                    for item in priority["breakdown"]:
                        st.write(f"- {item}")

                    st.progress(priority["score"] / 100)

                    st.caption(
                        "Prototype heuristic. Validate scores against "
                        "manually reviewed complaints before relying on them."
                    )

                with st.expander("View extracted indicators"):
                    st.write(f'Severity: {analysis["severity"].title()}')

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
            st.error("Could not analyze the complaint.")
            st.error(f"Error type: {type(e).__name__}")
            st.code(str(e))

            with st.expander("Technical details"):
                st.exception(e)

st.divider()

st.caption(
    "HotelPulse is an AI internship prototype. Classifications and "
    "priority scores may be incorrect and require human review."
)
