import solution_day_15

def test_merge_ranges():
    range, other_range = (0, 1), (1, 2)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == (0, 2)

    range, other_range = (0, 1), (0, 1)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == (0, 1)

    range, other_range = (0, 3), (0, 1)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == (0, 3)

    range, other_range = (0, 1), (0, 3)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == (0, 3)

    range, other_range = (0, 1), (2, 3)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == (0, 3)

    range, other_range = (0, 1), (3, 4)
    merged = solution_day_15.merge_ranges(range, other_range)
    assert merged == None


def test_merge_coverage():
    row_coverage = [(0, 1), (1, 2), (3, 4)]
    sensor_coverage = (5, 6)
    merged = solution_day_15.merge_coverage(row_coverage, sensor_coverage)
    assert merged == [(0, 6)]

    row_coverage = [(0, 1), (1, 2), (3, 4), (6, 10)]
    sensor_coverage = (14, 16)
    merged = solution_day_15.merge_coverage(row_coverage, sensor_coverage)
    assert merged == [(0, 4), (6, 10), (14, 16)]

    row_coverage = [(0, 1), (1, 2), (3, 4), (14, 16)]
    sensor_coverage = (5, 6)
    merged = solution_day_15.merge_coverage(row_coverage, sensor_coverage)
    assert merged == [(0, 6), (14, 16)]