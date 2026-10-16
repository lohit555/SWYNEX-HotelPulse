# HotelPulse Model Evaluation

## 1. Objective

The purpose of this evaluation is to assess HotelPulse's ability to classify hotel guest feedback, distinguish complaints from positive feedback, and assign complaint severity.

The evaluation uses 24 manually labelled examples covering positive feedback, all eight complaint categories, multiple severity levels, mixed sentiment, and unrelated input.

## 2. Evaluation Method

Each example contains an expected category, complaint flag, and severity label. HotelPulse processes the feedback using the configured Groq model, `openai/gpt-oss-120b`.

The predicted outputs are compared against the manually assigned expected labels.

The evaluation measures:
- **Category accuracy:** Percentage of successful predictions whose category matches the expected category.
- **Complaint-detection accuracy:** Percentage whose complaint flag matches the expected flag.
- **Severity accuracy:** Percentage whose predicted severity exactly matches the expected severity.

These results measure agreement with this initial test set and should not be interpreted as proof of production readiness.

## 3. Results

| Metric | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Category classification | 23 | 24 | 95.83% |
| Complaint detection | 24 | 24 | 100.00% |
| Severity classification | 14 | 24 | 58.33% |

All 24 model calls completed successfully, with no API failures.

## 4. Observed Failure Cases

### Case 1: Overlapping categories

**Example:** The guest reported that the air conditioner was noisy and did not cool the room effectively.

- Expected category: Room/Facilities
- Predicted category: Noise

**Observation:** The feedback contains both an equipment defect and a noise-related symptom. The model selected Noise rather than Room/Facilities.

**Potential improvement:** Clarify how to choose the primary category when multiple aspects of a complaint overlap.

### Case 2: Severity overestimation

**Example:** A guest reported waiting two hours for a room-service order.

- Expected severity: Moderate
- Predicted severity: Serious

**Observation:** The model assigned a higher severity than the initial expected label.

**Potential improvement:** Provide clearer severity definitions and examples for service delays, considering duration, impact, and whether the guest's basic needs were affected.

### Case 3: Severity of physical hazards

**Example:** A ceiling panel fell beside the bed and exposed damaged electrical wiring.

- Expected severity: Severe
- Predicted severity: Serious

**Observation:** The model recognized a serious issue but assigned a lower severity than expected.

**Potential improvement:** Add explicit guidance for physical hazards and potential electrical safety risks. Safety-related complaints should receive prompt human review.

### Case 4: Financial complaint severity

**Example:** A guest reported being charged for a cancelled reservation and receiving no response to repeated refund requests.

- Expected severity: Serious
- Predicted severity: Moderate

**Observation:** The model may have underestimated the impact of an unresolved financial complaint.

**Potential improvement:** Define how duplicate charges, cancelled bookings, and repeated unsuccessful refund requests should influence severity.

## 5. Limitations

- The evaluation contains only 24 manually labelled examples.
- The expected labels are initial human judgements and may be subjective.
- Accuracy on this small, purpose-built test set may not generalize to real-world hotel reviews.
- The test does not establish that the model's priority scores reliably predict actual operational urgency.
- Additional examples are needed to assess performance across different wording, languages, complaint combinations, and severity levels.

## 6. Next Steps

1. Review the severity definitions and refine the model instructions.
2. Add more manually reviewed evaluation examples.
3. Retest the model after changes using the same baseline examples.
4. Compare results across categories and severity levels.
5. Have hotel staff review high-priority or safety-related cases before taking action.

## 7. Conclusion

In this initial evaluation, HotelPulse achieved 95.83% category accuracy and 100.00% complaint-detection accuracy. Severity accuracy was lower at 58.33%, identifying severity assignment as the main area for further investigation.

The results are encouraging for an initial prototype, but the small test set and subjective labels limit the conclusions that can be drawn. Further evaluation and human review are necessary before using the system for operational decisions.
