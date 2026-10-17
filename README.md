
# 🏨 HotelPulse 

HotelPulse is an AI-powered web application that analyzes hotel guest feedback, classifies complaints, and assigns severity and priority scores to help hotel support teams identify issues that may require attention.

## Features

- **Complaint classification:** Categorizes guest feedback into Positive, Cleanliness, Staff/Service, Room/Facilities, Food/Dining, Location, Noise, or Value/Billing.
- **Severity assessment:** Classifies complaints by severity: minor, moderate, serious, or severe.
- **Priority scoring:** Assigns a priority score from 0 to 100 and a corresponding priority level.
- **Safety awareness:** Identifies potential safety concerns and considers them when prioritizing complaints.
- **Interactive dashboard:** Provides a simple Streamlit interface for analyzing guest feedback.
- **Model evaluation:** Evaluates predictions against a set of manually labelled examples and saves detailed results to a CSV file.

## Tech Stack

- Python
- Streamlit
- Groq API
- Large language model: `openai/gpt-oss-120b`
- JSON-based evaluation examples
- pandas (for evaluation result analysis, if used by the evaluation script)

## Project Structure

```text
SWYNEX-HotelPulse/
├── analyzer.py
├── dashboard.py
├── evaluate.py
├── evaluation_examples.json
├── prepare_dataset.py
├── evaluation_results.csv
├── README.md
└── .gitignore
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/lohit555/SWYNEX-HotelPulse.git
cd SWYNEX-HotelPulse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the packages required by the application:

```bash
pip install streamlit groq python-dotenv
```

If the repository contains a `requirements.txt` file, you can install the project's listed dependencies instead:

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key.

**Security:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run dashboard.py
```

Streamlit will provide a local URL where you can interact with the HotelPulse dashboard.

## Model Evaluation

HotelPulse includes a labelled evaluation set and an evaluation script.

Run the evaluation with:

```bash
python evaluate.py
```

The script evaluates model predictions against the expected labels and reports:

- Category classification accuracy
- Complaint detection accuracy
- Severity classification accuracy
- Incorrect predictions, where applicable
- Detailed results saved to `evaluation_results.csv`

### Latest Evaluation Results

The latest completed evaluation used 24 labelled examples. All 24 predictions completed successfully without API errors.

| Metric | Result |
|---|---:|
| Category accuracy | 100.00% (24/24) |
| Complaint detection accuracy | 100.00% (24/24) |
| Severity accuracy | 100.00% (24/24) |
| Failed predictions | 0 |

No incorrect category, complaint-detection, or severity predictions were reported in this evaluation run.

### Failure Cases and Limitations

The evaluation process is designed to identify mismatches between expected and predicted labels. An earlier run exposed a category-classification failure involving a room-service phone that went unanswered and a delayed order. The model classified the complaint as `Food/Dining` instead of `Staff/Service`.

The prompt and evaluation examples were subsequently refined. In the latest 24-example run, this mismatch and the other evaluated mismatches were no longer present.

However, a perfect score on a small evaluation set does not guarantee perfect performance on unseen hotel reviews. Real-world feedback may contain ambiguous wording, multiple complaints, sarcasm, or safety issues that require human review. The evaluation set should be expanded to test performance across more varied examples.

## Intended Users

Hotel customer-support staff and hotel operations teams who need help organizing guest feedback, identifying complaint categories, and prioritizing issues for follow-up.

## Project Goal

HotelPulse aims to reduce the effort required to manually review hotel feedback by providing structured complaint classifications, severity assessments, and priority recommendations.

The system is a prototype intended to support human decision-making, not replace professional judgment or operational safety procedures.

## Repository

GitHub: https://github.com/lohit555/SWYNEX-HotelPulse
