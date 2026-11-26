
import pytest
import csv
from load_scores import load_scores


# 1. 정상 테스트: 유효한 데이터 읽기
def test_normal(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,85\n지훈,70\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 85), ("지훈", 70)]
    assert skipped == []


# 2. 예외 테스트: 파일이 존재하지 않는 경우
def test_file_not_found(tmp_path):
    file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


# 3. 경계값 테스트: 헤더만 있는 경우
def test_header_only(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


# 4. 경계값 테스트: 점수의 최솟값과 최댓값
def test_score_boundary(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,0\n지훈,100\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 0), ("지훈", 100)]
    assert skipped == []


# 5. 예외 데이터 테스트: 잘못된 점수
def test_invalid_score(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,abc\n지훈,150\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 2


# 6. 예외 데이터 테스트: 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


# 7. 예외 데이터 테스트: 열 개수가 맞지 않는 경우
def test_wrong_column_count(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,80,추가\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


# 8. 중복 이름 유지 테스트
def test_duplicate_names(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,80\n민수,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 80), ("민수", 90)]
    assert skipped == []


# 9. 빈 줄 무시 테스트
def test_blank_line(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,80\n\n지훈,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 80), ("지훈", 90)]
    assert skipped == []
