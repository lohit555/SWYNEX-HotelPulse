
# HotelPulse Model Evaluation

## 1. Objective

The purpose of this evaluation is to assess HotelPulse's ability to classify hotel guest feedback, distinguish complaints from positive feedback, and assign complaint severity.

The evaluation uses 24 manually labelled examples covering positive feedback, all eight complaint categories, multiple severity levels, mixed sentiment, and unrelated input.

## 2. Evaluation Method

Each example contains an expected category, complaint flag, and severity label. HotelPulse processes the feedback using the configured Groq model, `openai/gpt-oss-120b`.

The predicted outputs are compared against the manually assigned expected labels.

The evaluation measures:

- **Category accuracy:** Percentage of predictions whose category matches the expected category.
- **Complaint-detection accuracy:** Percentage of predictions whose complaint flag matches the expected flag.
- **Severity accuracy:** Percentage of predictions whose severity exactly matches the expected severity.

These results measure agreement with this initial test set and should not be interpreted as proof of production readiness.

## 3. Results

| Metric | Previous Baseline | Latest Result |
|---|---:|---:|
| Category classification | 23/24 (95.83%) | 24/24 (100.00%) |
| Complaint detection | 24/24 (100.00%) | 24/24 (100.00%) |
| Severity classification | 14/24 (58.33%) | 22/24 (91.67%) |

All 24 model calls completed successfully, with no API failures.

### Results Summary

The updated model instructions improved severity accuracy from 58.33% to 91.67%, an increase of 33.34 percentage points. Category accuracy also improved from 95.83% to 100.00%, while complaint-detection accuracy remained at 100.00%.

These improvements were observed on the same 24-example evaluation set. Further testing is required to determine whether the improvements generalize to new reviews.

## 4. Remaining Failure Cases

Two examples were incorrectly classified by severity in the latest evaluation.

### Case 1: Severity Underestimation or Overestimation — ID 10

- **Expected severity:** Minor
- **Predicted severity:** Moderate

**Observation:** The model assigned a higher severity than the expected label.

**Next step:** Review the original feedback and the model's explanation to determine whether the severity definitions or the expected label need further examination.

### Case 2: Severity Overestimation — ID 11

- **Expected severity:** Moderate
- **Predicted severity:** Serious

**Observation:** The model assigned a higher severity than the expected label.

**Next step:** Inspect the review text and model explanation, then determine whether the model is overestimating the impact of the complaint or whether the expected severity requires reconsideration.

The exact review text and explanations for these two cases should be examined before making further prompt changes.

## 5. Limitations

- The evaluation contains only 24 manually labelled examples.
- The expected labels are initial human judgements and may be subjective.
- Accuracy on this small, purpose-built test set may not generalize to real-world hotel reviews.
- The test does not establish that the model's priority scores reliably predict actual operational urgency.
- Additional examples are needed to assess performance across different wording, languages, complaint combinations, and severity levels.
- The evaluation does not independently verify whether the model's classifications are appropriate for actual hotel operations.

## 6. Next Steps

1. Review the two remaining severity mismatches using their original feedback and model explanations.
2. Expand the evaluation dataset with additional manually labelled examples.
3. Retest the model using the existing baseline examples after any changes.
4. Compare results across categories and severity levels to identify recurring errors.
5. Assess performance on new examples that were not used to refine the model instructions.
6. Have hotel staff review high-priority or safety-related cases before taking action.

## 7. Conclusion

In the latest evaluation, HotelPulse achieved 100.00% category accuracy, 100.00% complaint-detection accuracy, and 91.67% severity accuracy across 24 manually labelled examples.

Compared with the previous baseline, severity accuracy improved by 33.34 percentage points, while category accuracy increased by 4.17 percentage points.

The results are encouraging for an initial prototype, but the small test set and subjective labels limit the conclusions that can be drawn. A larger evaluation set, further testing on unseen reviews, and human review of high-priority cases are necessary before using the system for operational decisions.
