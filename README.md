# Prescription-understanding
基于正则表达式和AC自动机多模匹配进行不规则处方文本理解，识别药品名、给药总量、用法用量等目标内容。

For example:

Input: 多巴丝肼(合资) 0.25g40*40.000 Sig.0.125g bid po

Output: {"Type": "Medicine_Name", "Offset_Begin": 0, "Offset_End": 3, "Original_Text": "多巴丝肼", "Interpretation": null, "Attributes": [{"PrescriptionComponent": {"Type": "Brand_Type", "Offset_Begin": 0, "Offset_End": 3, "Original_Text": "(合资)", "Interpretation": null}}, {}, {}, {"PrescriptionNumericalComponent": {"Type": "Specification", "Offset_Begin": 9, "Offset_End": 14, "Original_Text": "0.25g", "Interpretation": "每片/粒/袋/支 0.25克", "Value_Unit": [{"value": 0.25, "unit": "克"}]}}, {"PrescriptionNumericalComponent": {"Type": "Total_Amount", "Offset_Begin": 9, "Offset_End": 24, "Original_Text": "0.25g*40×40.000", "Interpretation": "每片/粒/袋/支 0.25克，每盒40.0片/粒/袋/支，共40.0盒，共计400.0克", "Value_Unit": null}}, [{"PrescriptionComponent": {"Type": "Frequency", "Offset_Begin": 39, "Offset_End": 41, "Original_Text": "bid", "Interpretation": "每天两次"}}], {"PrescriptionComponent": {"Type": "Route", "Offset_Begin": 36, "Offset_End": 37, "Original_Text": "po", "Interpretation": "经口，口服"}}, [{"PrescriptionNumericalComponent": {"Type": "Dosage", "Offset_Begin": 29, "Offset_End": 35, "Original_Text": "0.125g", "Interpretation": "0.5片/粒/袋/支", "Value_Unit": {"value": 0.125, "unit": "克"}}}], []]}
