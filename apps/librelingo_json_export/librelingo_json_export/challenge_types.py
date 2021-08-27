import editdistance  # type: ignore

from librelingo_utils import (
    get_dumb_opaque_id,
    audio_id,
    remove_control_characters_for_display,
    clean_word,
    iterate_phrases,
)
from .dictionary import _define_words_in_sentence


def get_listening_challenge(source, course):
    if not course.settings.audio_settings.enabled:
        return []

    return [
        {
            "type": "listeningExercise",
            "answer": remove_control_characters_for_display(
                source.in_target_language[0]
            ),
            "meaning": remove_control_characters_for_display(
                source.in_source_language[0]
            ),
            "audio": audio_id(
                course.target_language,
                remove_control_characters_for_display(source.in_target_language[0]),
            ),
            "id": get_dumb_opaque_id("Word", source, "listeningExercise"),
            "priority": 1,
            "group": get_dumb_opaque_id("Group", source),
        }
    ]


def get_short_input_challenge(source, course):
    return [
        {
            "type": "shortInput",
            "pictures": [pic + ".jpg" for pic in source.pictures]
            if source.pictures
            else None,
            "formInTargetLanguage": [
                remove_control_characters_for_display(t)
                for t in source.in_target_language
            ],
            "phrase": _define_words_in_sentence(
                course, source.in_source_language[0], reverse=False
            ),
            "id": get_dumb_opaque_id("Word", source, "shortInput"),
            "priority": 1,
            "group": get_dumb_opaque_id("Group", source),
        }
    ]


def get_cards_challenge(word, _):
    return [
        {
            "type": "cards",
            "pictures": [pic + ".jpg" for pic in word.pictures]
            if word.pictures
            else None,
            "formInTargetLanguage": remove_control_characters_for_display(
                word.in_target_language[0]
            ),
            "meaningInSourceLanguage": remove_control_characters_for_display(
                word.in_source_language[0]
            ),
            "id": get_dumb_opaque_id("Word", word, "cards"),
            "priority": 0,
            "group": get_dumb_opaque_id("Group", word),
        }
    ]


def get_options_challenge(phrase, _):
    return [
        {
            "type": "options",
            "formInTargetLanguage": remove_control_characters_for_display(
                phrase.in_target_language[0]
            ),
            "meaningInSourceLanguage": remove_control_characters_for_display(
                phrase.in_source_language[0]
            ),
            "id": get_dumb_opaque_id("Options", phrase, "options"),
            "priority": 0,
            "group": get_dumb_opaque_id("Group", phrase),
        }
    ]


def get_chips_from_string(phrase):
    return list(map(clean_word, phrase.split()))


def get_chips_from_phrase(get_input_texts, phrase, course):
    extra_chips = []
    solution_chips = get_chips_from_string(get_input_texts(phrase)[0])

    for phrase in iterate_phrases(course):
        for variant in get_input_texts(phrase):
            for chip in get_chips_from_string(variant):
                if chip not in solution_chips:
                    extra_chips.append(chip)

    chips_already_added = set()
    deduplicated_chips = []

    for chip in extra_chips:
        if chip.lower() not in chips_already_added:
            deduplicated_chips.append(chip)
            chips_already_added.add(chip.lower())

    extra_chips = sorted(
        deduplicated_chips,
        key=lambda chip: sum(
            editdistance.eval(other_chip, chip) for other_chip in solution_chips
        ),
    )

    return solution_chips + extra_chips[0 : max(len(solution_chips) - 1, 2)]


def get_solutions_from_phrase(get_input_texts, phrase):
    return [get_chips_from_string(x) for x in get_input_texts(phrase)]


def create_chips_challenge_generator(reverse):
    def get_input_texts(phrase):
        return phrase.in_source_language if reverse else phrase.in_target_language

    def get_phrase_texts(phrase):
        return phrase.in_target_language if reverse else phrase.in_source_language

    def get_input_text(phrase):
        return get_input_texts(phrase)[0]

    def get_phrase_text(phrase):
        return get_phrase_texts(phrase)[0]

    def is_long_enough_to_have_chips(phrase):
        if len(phrase.in_source_language[0].split()) < 2:
            return False
        if len(phrase.in_target_language[0].split()) < 2:
            return False
        return True

    def get_chips_challenge(phrase, course):
        if not is_long_enough_to_have_chips(phrase):
            return []

        return [
            {
                "type": "chips",
                "translatesToSourceLanguage": reverse,
                "phrase": _define_words_in_sentence(
                    course, get_phrase_text(phrase), reverse
                ),
                "chips": get_chips_from_phrase(get_input_texts, phrase, course),
                "solutions": get_solutions_from_phrase(get_input_texts, phrase),
                "formattedSolution": remove_control_characters_for_display(
                    get_input_text(phrase)
                ),
                "id": get_dumb_opaque_id(
                    "Chips", phrase, "reverse chips" if reverse else "chips"
                ),
                "priority": 2,
                "group": get_dumb_opaque_id("Group", phrase),
            }
        ]

    return get_chips_challenge


get_chips_challenge = create_chips_challenge_generator(False)
get_reverse_chips_challenge = create_chips_challenge_generator(True)
