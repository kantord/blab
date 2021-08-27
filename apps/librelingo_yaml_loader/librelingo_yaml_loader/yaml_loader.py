import collections
from pathlib import Path

import bleach
from librelingo_types import (
    Course,
    DictionaryItem,
    Language,
    License,
    Module,
    Phrase,
    Skill,
    Word,
    Settings,
    AudioSettings,
    TextToSpeechSettings,
)
import markdown
from yaml import safe_load
from yaml.constructor import SafeConstructor

import html2markdown  # type: ignore


def add_bool(self, node):
    return self.construct_scalar(node)


SafeConstructor.add_constructor(u"tag:yaml.org,2002:bool", add_bool)


def _load_yaml(path):
    """Helper function for reading a YAML file"""
    with open(path) as f:
        return safe_load(f)


def _convert_language(raw_language):
    """
    Convert a YAML langauge description to a Language() object
    """
    return Language(
        name=raw_language["Name"],
        code=raw_language["IETF BCP 47"],
    )


def _get_dictionary_items_from_new_words(skill):
    """
    Extract new words in a skill as dictionary items
    """
    for word in skill.words:
        yield word.in_source_language[0], word.in_target_language[0], False
        yield word.in_target_language[0], word.in_source_language[0], True


def _get_dictionary_items_from_skill_mini_dictionary(skill):
    """
    Iterate over all dictionary items from the mini-dictionary of a skill
    """
    for dictionary_item in skill.dictionary:
        word, definitions, is_in_target_language = dictionary_item
        for definition in definitions:
            yield word, definition, is_in_target_language


def _get_all_skills(modules):
    """
    Iterate over all skills in the supplied list of modules
    """
    for module in modules:
        for skill in module.skills:
            yield skill


def _get_dictionary_items(modules):
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


def _get_merged_dictionary_items(modules):
    """
    Generates merged dictionary items using every skill in every module that is
    passed in the argument.

    Merging dictionary items means that multiple definitions of the same word
    are compressed into one definition that has a multiple meanings listed.
    """
    return _merge_dictionary_definitions(_get_dictionary_items(modules))


def _load_dictionary(modules):
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


def _alternatives_from_yaml(raw_object, key):
    """
    Returns alternative solutions based on the key, or an empty list if
    there are no alternative solutions specified
    """
    return raw_object[key] if key in raw_object else []


def _solution_from_yaml(raw_object, solution_key, alternatives_key):
    """
    Converts a solution and it's alternatives into a single list, where
    the alternatives are optional
    """
    solution = raw_object[solution_key]
    return [solution, *_alternatives_from_yaml(raw_object, alternatives_key)]


def _convert_word(raw_word):
    """
    Converts a YAML word definition into a Word() object
    """
    return Word(
        in_target_language=_solution_from_yaml(raw_word, "Word", "Synonyms"),
        in_source_language=_solution_from_yaml(
            raw_word, "Translation", "Also accepted"
        ),
        pictures=raw_word["Images"] if "Images" in raw_word else None,
    )


def _convert_words(raw_words):
    """
    Converts each YAML word definition into Word() objects
    """
    return list(map(_convert_word, raw_words))


def _convert_phrase(raw_phrase):
    """
    Converts a YAML phrase definition into a Phrase() object
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
    except KeyError:
        raise RuntimeError(
            'Phrase "{}" needs to have a "Translation".'.format(raw_phrase["Phrase"])
        )


def _convert_phrases(raw_phrases):
    """
    Converts each YAML phrase definition into Phrase() objects
    """
    return list(map(_convert_phrase, raw_phrases))


def _convert_mini_dictionary(raw_mini_dictionary, course):
    """
    Handles loading the mini-dictionary form the YAML format
    """
    configurations = (
        (course.target_language.name, True),
        (course.source_language.name, False),
    )
    for language_name, is_in_target_language in configurations:
        for item in raw_mini_dictionary[language_name]:
            word = list(item.keys())[0]
            raw_definition = list(item.values())[0]
            definition = (
                raw_definition if type(raw_definition) == list else [raw_definition]
            )
            yield (word, tuple(definition), is_in_target_language)


def _sanitize_markdown(mdtext):
    "Removes unsafe text content from Markdown"
    dirty_html = markdown.markdown(mdtext)
    clean_html = bleach.clean(
        dirty_html,
        strip=True,
        tags=[*bleach.sanitizer.ALLOWED_TAGS, "h1", "h2", "h3", "h4", "h5", "h6"],
    )

    return html2markdown.convert(clean_html)


def _load_introduction(path):
    "Loads the introduction text from a Markdown file"
    try:
        with open(path) as f:
            return _sanitize_markdown(f.read())
    except:
        return None


def _load_skill(path, course):
    try:
        data = _load_yaml(path)
        introduction = _load_introduction(str(path).replace(".yaml", ".md"))
        skill = data["Skill"]
        words = data["New words"]
        phrases = data["Phrases"]
    except TypeError:
        raise RuntimeError('Skill file "{}" is empty or does not exist'.format(path))
    except KeyError as error:
        raise RuntimeError(
            'Skill file "{}" needs to have a "{}" key'.format(path, error.args[0])
        )

    try:
        name = skill["Name"]
    except Exception:
        raise RuntimeError('Skill file "{}" needs to have skill name'.format(path))

    try:
        skill_id = skill["Id"]
    except Exception:
        raise RuntimeError('Skill file "{}" needs to have skill id'.format(path))

    try:
        phrases = _convert_phrases(phrases)
    except TypeError:
        raise RuntimeError('Skill file "{}" has an invalid phrase'.format(path))

    try:
        words = _convert_words(words)
    except TypeError:
        raise RuntimeError('Skill file "{}" has an invalid word'.format(path))

    return Skill(
        name=name,
        id=skill_id,
        words=words,
        phrases=phrases,
        image_set=skill["Thumbnails"] if "Thumbnails" in skill else [],
        dictionary=list(_convert_mini_dictionary(data["Mini-dictionary"], course))
        if "Mini-dictionary" in data
        else [],
        introduction=introduction,
    )


def _load_skills(path, skills, course):
    """
    Load each YAML skill specified in the list
    """
    try:
        return [_load_skill(Path(path) / "skills" / skill, course) for skill in skills]
    except TypeError:
        raise RuntimeError(
            'Module file "{}/module.yaml" needs to have a list of skills'.format(path)
        )


def _load_module(path, course):
    """
    Load a YAML module
    """
    filepath = Path(path) / "module.yaml"
    data = _load_yaml(filepath)
    try:
        module = data["Module"]
        skills = data["Skills"]
    except TypeError:
        raise RuntimeError(
            'Module file "{}" is empty or does not exist'.format(filepath)
        )
    except KeyError as error:
        raise RuntimeError(
            'Module file "{}" needs to have a "{}" key'.format(filepath, error.args[0])
        )

    try:
        title = module["Name"]
    except Exception:
        raise RuntimeError(
            'Module file "{}" needs to have module name'.format(filepath)
        )

    return Module(title=title, skills=_load_skills(path, skills, course))


def _load_modules(path, modules, course):
    """
    Load each YAML module specifed in the list
    """
    return [_load_module(Path(path) / module, course) for module in modules]


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
        text_to_speech_settings_list = _convert_text_to_speech_settings_list(raw_audio_settings)
    else:
        text_to_speech_settings_list = []

    return AudioSettings(
        enabled=raw_audio_settings["Enabled"] == "True",
        text_to_speech_settings_list=text_to_speech_settings_list
    )


def _convert_settings(data):
    if "Settings" not in data:
        return Settings()

    raw_settings = data["Settings"]

    return Settings(
        audio_settings=_convert_audio_settings(raw_settings),
    )


def load_course(path):
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
        settings=_convert_settings(data),
        repository_url=course["Repository"],
    )
    modules = _load_modules(path, raw_modules, dumb_course)

    return Course(
        **{
            **dumb_course._asdict(),
            "dictionary": _load_dictionary(modules),
            "modules": modules,
        }
    )
