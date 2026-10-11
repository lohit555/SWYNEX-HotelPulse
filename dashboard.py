
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

    .result-card {
        background: white;
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

    .result-panel {
        background: white;
        border: 1px solid #e3e9f2;
        border-radius: 16px;
        padding: 22px;
        margin-top: 16px;
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

            if not analysis["is_complaint"]:
                st.info(
                    "This text was not identified as a hotel complaint "
                    "or review. Please check the input."
                )
                st.write(analysis["explanation"])

            else:
                priority = calculate_priority(analysis)

                category_col, score_col, level_col = st.columns(3)

                with category_col:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="card-label">Complaint Category</div>
                            <div class="card-value">{analysis['category']}</div>
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
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="card-label">Priority Level</div>
                            <span class="priority-pill"
                                style="
                                    background:{priority['background']};
                                    color:{priority['color']};">
                                {priority['level']}
                            </span>
                            <p style="color:#53627c;margin-top:12px;">
                                {priority['description']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    '<div class="result-panel">',
                    unsafe_allow_html=True,
                )
                st.markdown("### 📝 Complaint Summary")
                st.write(analysis["summary"])

                st.markdown("### 💡 Analysis Explanation")
                st.write(analysis["explanation"])
                st.markdown("</div>", unsafe_allow_html=True)

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
                    st.write(f"Severity: {analysis['severity'].title()}")

                    st.write(
                        "Safety concern: "
                        + ("Yes" if analysis["safety_concern"] else "No")
                    )
                    st.write(
                        "Urgent language: "
                        + ("Yes" if analysis["urgent_language"] else "No")
                    )
                    st.write(
                        "Financial impact: "
                        + ("Yes" if analysis["financial_impact"] else "No")
                    )
                    st.write(
                        "Multiple issues: "
                        + ("Yes" if analysis["multiple_issues"] else "No")
                    )

        except Exception:
            st.error(
                "Could not analyze the complaint. Check your Groq API key, "
                "internet connection, model availability, and usage limits."
            )
            st.caption(
                "If the issue continues, check the terminal for the "
                "technical error details."
            )

st.divider()
st.caption(
    "HotelPulse is an AI internship prototype. Classifications and "
    "priority scores may be incorrect and require human review."
)
