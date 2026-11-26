
import pytest
from load_scores import load_scores


# 1. 정상 입력 테스트
def test_normal_scores(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,85\n지훈,70\n서연,100\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 85), ("지훈", 70), ("서연", 100)]
    assert skipped == []


# 2. 파일이 없을 때 예외 테스트
def test_file_not_found(tmp_path):
    file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


# 3. 헤더만 있는 경우
def test_header_only(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


# 4. 열 개수가 2개가 아닌 경우
def test_wrong_column_count(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,80,추가\n지훈\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 2
    assert skipped[0][2] == "열 개수가 2가 아님"


# 5. 점수가 비어 있는 경우
def test_empty_score(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n민수,\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"


# 6. 점수가 정수가 아닌 경우
def test_non_integer_score(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,abc\n지훈,85.5\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 2
    assert all(item[2] == "점수가 정수가 아님" for item in skipped)


# 7. 점수 범위 경계값 테스트
@pytest.mark.parametrize("score, expected", [
    (0, True),
    (100, True),
    (-1, False),
    (101, False),
])
def test_score_boundary(tmp_path, score, expected):
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    if expected:
        assert kept == [("민수", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped[0][2] == "점수가 0~100 밖"


# 8. 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n,80\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"


# 9. 같은 이름이 중복되는 경우
def test_duplicate_names(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,80\n민수,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 80), ("민수", 90)]
    assert skipped == []


# 10. 빈 줄은 기록하지 않는 경우
def test_blank_line(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n\n민수,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 80)]
    assert skipped == []
