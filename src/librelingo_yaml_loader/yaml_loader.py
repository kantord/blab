# pylint: disable=ungrouped-imports,use-yield-from,deprecated-method

import copy
import logging
import collections
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Union
import importlib.resources
import json
import bleach
from yaml.constructor import SafeConstructor
import jsonschema
import html2markdown  # type: ignore
import markdown
from yaml import load

from librelingo_types import (
    AudioSettings,
    Course,
    DictionaryItem,
    Language,
    License,
    Module,
    Phrase,
    Character,
    Settings,
    Skill,
    TextToSpeechSettings,
    Word,
)
from ._spelling import _convert_hunspell_settings, _run_skill_spellcheck


logger = logging.getLogger("librelingo_yaml_loader")
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    logger.warning(
        """
    Warning! PyYAML LibYAML C bindings are not installed.
    Course loading still works, but it will be slower.
    For more details, check https://github.com/yaml/pyyaml#Installation
    """
    )
    from yaml import SafeLoader  # type: ignore


class ValidationError(RuntimeError):
    pass


def add_bool(self, node):
    return self.construct_scalar(node)


SafeConstructor.add_constructor("tag:yaml.org,2002:bool", add_bool)

with importlib.resources.open_text(__package__, "module.json") as fp:
    module_schema = json.load(fp)

with importlib.resources.open_text(__package__, "skill.json") as fp:
    skill_schema = json.load(fp)


def _load_yaml(path: Path):
    """Helper function for reading a YAML file"""
    with open(path, encoding="utf-8") as yaml_file:
        return load(yaml_file, Loader=SafeLoader)


def _convert_language(raw_language) -> Language:
    """
    Convert a YAML langauge description to a Language() object
    """
    return Language(
        name=raw_language["Name"],
        code=raw_language["IETF BCP 47"],
    )


def _get_dictionary_items_from_new_words(skill: Skill):
    """
    Extract new words in a skill as dictionary items
    """
    for word in skill.words:
        yield word.in_source_language[0], word.in_target_language[0], False
        yield word.in_target_language[0], word.in_source_language[0], True


def _get_dictionary_items_from_skill_mini_dictionary(skill: Skill):
    """
    Iterate over all dictionary items from the mini-dictionary of a skill
    """
    for dictionary_item in skill.dictionary:
        word, definitions, is_in_target_language = dictionary_item
        for definition in definitions:
            yield word, definition, is_in_target_language


def _get_all_skills(modules: List[Module]):
    """
    Iterate over all skills in the supplied list of modules
    """
    for module in modules:
        for skill in module.skills:
            yield skill


def _get_dictionary_items(modules: List[Module]):
    """
    Extract all dictionary items from every module in the supplied list
    """
    for skill in _get_all_skills(modules):
        for item in _get_dictionary_items_from_new_words(skill):
            yield item

        if skill.dictionary is not None:
            for item in _get_dictionary_items_from_skill_mini_dictionary(skill):
                yield item


def _merge_dictionary_definitions(items_generator):
    """
    Merges dictionary items, meaning that multiple definitions of the same word
    are compressed into one definition that has a multiple meanings listed.
    """
    items = collections.defaultdict(set)
    for word, definition, is_in_target_language in items_generator:
        items[(word, is_in_target_language)].add(definition)
    return list(items.items())


def _get_merged_dictionary_items(modules: List[Module]):
    """
    Generates merged dictionary items using every skill in every module that is
    passed in the argument.

    Merging dictionary items means that multiple definitions of the same word
    are compressed into one definition that has a multiple meanings listed.
    """
    return _merge_dictionary_definitions(_get_dictionary_items(modules))


def _load_dictionary(modules: List[Module]) -> list:
    """
    Generates a dictionary using every skill in every module that is
    passed in the argument
    """
    items = []
    for key, definition in _get_merged_dictionary_items(modules):
        word, is_in_target_language = key
        items.append(
            DictionaryItem(
                word=word,
                definition="\n".join(sorted(definition)),
                is_in_target_language=is_in_target_language,
            )
        )
    return items


def _alternatives_from_yaml(raw_object, key: str):
    """
    Returns alternative solutions based on the key, or an empty list if
    there are no alternative solutions specified
    """
    return raw_object[key] if key in raw_object else []


def _solution_from_yaml(raw_object, solution_key: str, alternatives_key: str) -> list:
    """
    Converts a solution and it's alternatives into a single list, where
    the alternatives are optional
    """
    solution = raw_object[solution_key]
    return [solution, *_alternatives_from_yaml(raw_object, alternatives_key)]


def _convert_character(raw_character) -> Character:
    """
    Converts a YAML character into a Character() object

    >>> _convert_character(
    ...     {'Character': "Г", 'Tranliteration': ["H"], 'IPA': ["/ɦ/"]}
    ... )
    Character(character='Г', transliteration=['H'], ipa_pronounciation=['/ɦ/'])
    """
    return Character(
        character=raw_character["Character"],
        transliteration=raw_character["Transliteration"],
        ipa_pronounciation=raw_character["IPA"] if "IPA" in raw_character else None,
    )


def _convert_characters(raw_characters: List) -> List[Character]:
    """
    Convert each YAML character definition into Character() objects

    >>> _convert_characters(
    ...     {'Character': "Г", 'Tranliteration': ["H"], 'IPA': ["/ɦ/"]},
    ...     {'Character': "Д", 'Tranliteration': ["D"], 'IPA': ["/d/", "/dʲ/", "/ɟː/", "/d͡z/", "/d͡zʲ/", "/d͡ʒ/"]},
    ... )
    [Character(character='Г', 
            transliteration=['H'], 
            ipa_pronounciation=['/ɦ/']),
    Character(character='Д', 
            transliteration=['D'], 
            ipa_pronounciation=['/d/', '/dʲ/', '/ɟː/', '/d͡z/', '/d͡zʲ/', '/d͡ʒ/']),
    ]
    """
    return list(map(_convert_character, raw_characters))


def _convert_word(raw_word) -> Word:
    """
    Converts a YAML word definition into a Word() object

    >>> _convert_word(
    ...     {'Images': ["abc"], 'Word': "cat", 'Synonyms': ["kitten"], 'Translation': "gato"}
    ... )
    Word(in_target_language=['cat', 'kitten'], in_source_language=['gato'], pictures=['abc'])
    """
    return Word(
        in_target_language=_solution_from_yaml(raw_word, "Word", "Synonyms"),
        in_source_language=_solution_from_yaml(
            raw_word, "Translation", "Also accepted"
        ),
        pictures=raw_word["Images"] if "Images" in raw_word else None,
    )


def _convert_words(raw_words: List) -> List[Word]:
    """
    Converts each YAML word definition into Word() objects
    >>> _convert_words([
    ...     {
    ...         'Word': "l'homme",
    ...         'Translation': 'the man',
    ...         'Images': ['man1', 'man2', 'man3']
    ...     },
    ...     {
    ...         'Word': 'la femme',
    ...         'Synonyms': ['la dame'],
    ...         'Translation': 'the woman',
    ...         'Also accepted': ['the female']
    ...     }
    ... ])
    [Word(in_target_language=["l'homme"],
          in_source_language=['the man'],
          pictures=['man1', 'man2', 'man3']),
     Word(in_target_language=['la femme', 'la dame'],
          in_source_language=['the woman', 'the female'],
          pictures=None)]
    """
    return list(map(_convert_word, raw_words))


def _convert_phrase(raw_phrase) -> Phrase:
    """
    Converts a YAML phrase definition into a Phrase() object
    >>> _convert_phrase({
    ...     'Phrase': 'La femme dit bonjour',
    ...     'Alternative versions': ['la femme dit salut'],
    ...     'Translation': 'The woman says hello',
    ...     'Alternative translations': ['The woman says hi']
    ... })
    Phrase(in_target_language=['La femme dit bonjour', 'la femme dit salut'],
           in_source_language=['The woman says hello', 'The woman says hi'])
    """
    try:
        return Phrase(
            in_target_language=_solution_from_yaml(
                raw_phrase, "Phrase", "Alternative versions"
            ),
            in_source_language=_solution_from_yaml(
                raw_phrase, "Translation", "Alternative translations"
            ),
        )
    except KeyError as key_error:
        key_string = ", ".join('"' + key + '"' for key in raw_phrase.keys())
        if "Phrase" not in raw_phrase.keys():
            raise RuntimeError(
                f'Key "Phrase" not found. Keys found: {key_string}'
            ) from key_error
        raise RuntimeError(
            f'Phrase "{raw_phrase["Phrase"]}" needs to have a "Translation".'
        ) from key_error


def _convert_phrases(raw_phrases: List) -> List[Phrase]:
    """
    Converts each YAML phrase definition into Phrase() objects
    """
    return list(map(_convert_phrase, raw_phrases))


def _convert_two_way_dictionary(data) -> List[tuple]:
    """
    Handles loading the Two-way-dictionary form the YAML format
    """
    dictionary: List[tuple] = []
    # return dictionary
    if "Two-way-dictionary" not in data:
        return dictionary
    raw_two_way_dictionary = data["Two-way-dictionary"]
    for item in raw_two_way_dictionary:
        source_text = list(item.keys())[0]
        source_word = re.sub(r" *\([^)]*\) *", "", source_text)
        target_text = item[source_text]
        target_word = re.sub(r" *\([^)]*\) *", "", target_text)
        dictionary.append((source_word, ([target_text]), False))
        dictionary.append((target_word, ([source_text]), True))
    return dictionary


def _convert_mini_dictionary(data, course: Course) -> List[tuple]:
    """
    Handles loading the mini-dictionary form the YAML format
    """
    dictionary: List[tuple] = []
    if "Mini-dictionary" not in data:
        return dictionary

    raw_mini_dictionary = data["Mini-dictionary"]
    configurations = (
        (course.target_language.name, True),
        (course.source_language.name, False),
    )
    for language_name, is_in_target_language in configurations:
        for item in raw_mini_dictionary[language_name]:
            word = list(item.keys())[0]
            raw_definition = list(item.values())[0]
            definition = (
                raw_definition if isinstance(raw_definition, list) else [raw_definition]
            )
            dictionary.append((word, tuple(definition), is_in_target_language))
    return dictionary


def _sanitize_markdown(mdtext: str) -> str:
    "Removes unsafe text content from Markdown"
    dirty_html = markdown.markdown(mdtext)
    clean_html = bleach.clean(
        dirty_html,
        strip=True,
        tags=[*bleach.sanitizer.ALLOWED_TAGS, "h1", "h2", "h3", "h4", "h5", "h6"],
    )

    return html2markdown.convert(clean_html)


def _load_introduction(path: str) -> Union[str, None]:
    "Loads the introduction text from a Markdown file"
    if not os.path.exists(path):
        return None

    with open(path, encoding="utf-8") as f:
        return _sanitize_markdown(f.read())


def _get_skill_schema(course: Course):
    # Modifies the Skill schema to change the dynamic values
    # to match the langauges of the course
    new_schema = copy.deepcopy(skill_schema)
    new_schema["properties"]["Mini-dictionary"]["required"] = [
        course.source_language.name,
        course.target_language.name,
    ]
    new_schema["properties"]["Mini-dictionary"][course.source_language.name] = (
        new_schema["properties"]["Mini-dictionary"]["properties"][
            "ThisIsTheSourceLanguage"
        ]
    )
    del new_schema["properties"]["Mini-dictionary"]["properties"][
        "ThisIsTheSourceLanguage"
    ]
    new_schema["properties"]["Mini-dictionary"][course.target_language.name] = (
        new_schema["properties"]["Mini-dictionary"]["properties"][
            "ThisIsTheTargetLanguage"
        ]
    )
    del new_schema["properties"]["Mini-dictionary"]["properties"][
        "ThisIsTheTargetLanguage"
    ]

    return new_schema


def _load_skill(path: Path, course: Course) -> Skill:
    try:
        data = _load_yaml(path)
        jsonschema.validate(data, _get_skill_schema(course))
        introduction = _load_introduction(str(path).replace(".yaml", ".md"))
        skill = data["Skill"]
        characters = data["New Characters"]
        words = data["New words"]
        phrases = data["Phrases"]
    except TypeError as type_error:
        raise RuntimeError(
            f'Skill file "{path}" is empty or does not exist'
        ) from type_error
    except KeyError as error:
        raise RuntimeError(
            f'Skill file "{path}" needs to have a "{error.args[0]}" key'
        ) from error
    except jsonschema.ValidationError as validation_error:
        if str(validation_error).startswith("None is not of type 'object'"):
            raise ValidationError(
                f'Skill file "{path}" is empty or does not exist'
            ) from validation_error
        raise ValidationError(
            f"There is an error with the schema at the following file path: {path}\n"
            f"Original error message: {str(validation_error)}"
        ) from validation_error

    try:
        name = skill["Name"]
    except Exception as exception:
        raise RuntimeError(
            f'Skill file "{path}" needs to have skill name'
        ) from exception

    skill_id = skill["Id"]
    phrases = _convert_phrases(phrases)
    words = _convert_words(words)
    characters = _convert_characters(character)

    _run_skill_spellcheck(phrases, words, course)

    return Skill(
        name=name,
        filename=os.path.relpath(path, start=course.course_dir),
        id=skill_id,
        words=words,
        phrases=phrases,
        characters=characters,
        image_set=skill["Thumbnails"] if "Thumbnails" in skill else [],
        dictionary=_convert_mini_dictionary(data, course)
        + _convert_two_way_dictionary(data),
        introduction=introduction,
    )


def _load_skills(path: str, skills, course: Course) -> List[Skill]:
    """
    Load each YAML skill specified in the list
    """
    try:
        return [_load_skill(Path(path) / "skills" / skill, course) for skill in skills]
    except TypeError as type_error:
        raise RuntimeError(
            f'Module file "{path}/module.yaml" needs to have a list of skills'
        ) from type_error


def _load_module(path: str, course: Course):
    """
    Load a YAML module
    """
    filepath = Path(path) / "module.yaml"
    data = _load_yaml(filepath)

    try:
        jsonschema.validate(data, module_schema)
    except jsonschema.ValidationError as validation_error:
        if str(validation_error).startswith("None is not of type 'object'"):
            raise ValidationError(
                f'Module file "{filepath}" is empty or does not exist'
            ) from validation_error
        raise ValidationError(
            f"There is an error with the schema at the following file path: {filepath}\n"
            f"Original error message: {str(validation_error)}"
        ) from validation_error

    module = data["Module"]
    skills = data["Skills"]

    return Module(
        title=module["Name"],
        filename=os.path.relpath(path, start=course.course_dir),
        skills=_load_skills(path, skills, course),
    )


def _load_modules(path: str, modules, course: Course):
    """
    Load each YAML module specified in the list
    """
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        futures = [
            pool.submit(_load_module, Path(path) / module, course) for module in modules
        ]
        return [future.result() for future in futures]


def _convert_license(raw_license):
    """
    Creates a License() object based on the data structure
    in the YAML file
    """
    return License(
        name=raw_license["Short name"],
        full_name=raw_license["Name"],
        link=raw_license["Link"],
    )


def _convert_text_to_speech_settings_list(raw_audio_settings):
    """
    Creates an TextToSpeechSettings() object based on the data structure in the YAML
    file
    """
    if "TTS" not in raw_audio_settings:
        return AudioSettings().text_to_speech_settings_list

    return [
        TextToSpeechSettings(tts["Provider"], tts["Voice"], tts["Engine"])
        for tts in raw_audio_settings["TTS"]
    ]


def _convert_audio_settings(raw_settings):
    """
    Creates an AudioSettings() object based on the data structure in the YAML
    file
    """
    if "Audio" not in raw_settings:
        return AudioSettings()

    raw_audio_settings = raw_settings["Audio"]

    if raw_audio_settings["Enabled"]:
        text_to_speech_settings_list = _convert_text_to_speech_settings_list(
            raw_audio_settings
        )
    else:
        text_to_speech_settings_list = []

    return AudioSettings(
        enabled=raw_audio_settings["Enabled"] == "True",
        text_to_speech_settings_list=text_to_speech_settings_list,
    )


def _convert_settings(data, course: Course):
    if "Settings" not in data:
        return Settings()

    raw_settings = data["Settings"]

    return Settings(
        audio_settings=_convert_audio_settings(raw_settings),
        hunspell=_convert_hunspell_settings(raw_settings, course),
    )


def load_course(path: str):
    """
    Load a YAML-based course into a Course() object
    """
    data = _load_yaml(Path(path) / "course.yaml")
    course = data["Course"]
    raw_modules = data["Modules"]
    dumb_course = Course(
        target_language=_convert_language(course["Language"]),
        source_language=_convert_language(course["For speakers of"]),
        license=_convert_license(course["License"]),
        special_characters=course["Special characters"],
        dictionary=[],
        modules=[],
        settings=None,
        repository_url=course["Repository"],
        course_dir=path,
    )
    dumb_course = Course(
        **{
            **dumb_course._asdict(),
            "settings": _convert_settings(data, dumb_course),
        }
    )
    modules = _load_modules(path, raw_modules, dumb_course)

    return Course(
        **{
            **dumb_course._asdict(),
            "settings": _convert_settings(data, dumb_course),
            "dictionary": _load_dictionary(modules),
            "modules": modules,
        }
    )
