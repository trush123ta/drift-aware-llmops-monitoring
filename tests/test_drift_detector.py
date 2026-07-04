from monitoring.retrieval_drift_detector import metric_drop


def test_metric_drop():
    baseline_value = 0.40
    current_value = 0.10

    drop = metric_drop(baseline_value, current_value)

    assert drop == 0.30