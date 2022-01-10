import collections
import pytest

from librelingo_json_export.challenge_types import get_short_input_challenge
from librelingo_fakes import fakes

TCData = collections.namedtuple("TCData", ["word", "course", "expected_result", "name"])


@pytest.mark.parametrize(
    "test_case_data",
    [
        TCData(
            fakes.word1,
            fakes.course1,
            {
                "id": "749e7c734898",
                "type": "shortInput",
                "pictures": ["foo.jpg", "bar.jpg", "baz.jpg"],
                "formInTargetLanguage": ["foous"],
                "phrase": [{"word": "foo", "definition": "barrus"}],
                "priority": 1,
                "group": "aab69500f014",
            },
            "data_set_a",
        ),
        TCData(
            fakes.word2,
            fakes.course1,
            {
                "id": "5f1b4778039c",
                "type": "shortInput",
                "pictures": ["1.jpg", "2.jpg", "3.jpg"],
                "formInTargetLanguage": ["apfel"],
                "phrase": [{"word": "apple", "definition": "red fruit"}],
                "priority": 1,
                "group": "9dbe235cb2d6",
            },
            "data_set_b",
        ),
        TCData(
            fakes.word_with_spaces,
            fakes.course1,
            {
                "id": "3b0f6c9df85b",
                "type": "shortInput",
                "pictures": ["1.jpg", "2.jpg", "3.jpg"],
                "formInTargetLanguage": ["three word term"],
                "phrase": [{"word": "foo bar baz", "definition": "three word term"}],
                "priority": 1,
                "group": "e707f76a703d",
            },
            "word_with_spaces",
        ),
    ],
    ids=lambda cur_test_case_data: cur_test_case_data.name,
)
def test_get_short_input_challenge(test_case_data):
    cur_res = get_short_input_challenge(test_case_data.word, test_case_data.course)[0]
    assert cur_res == test_case_data.expected_result
