from collections import namedtuple

class TextToSpeechSettings(
    namedtuple(
        "TextToSpeechSettings",
        [
            "provider",
            "voice",
            "engine",
        ],
        defaults=["Polly", "Lupe", "standard"]
    )
):
    """
    Settings about how to use TTS to generate audios

    ### Usage example:

    ```python
    TextToSpeechSettings(
        provider="Polly",
        voice="Aditi",
        engine="standard"
    )
    ```
    """

    pass

class AudioSettings(
    namedtuple(
        "AudioSettings",
        [
            "enabled",
            "text_to_speech_settings_list",
        ],
        defaults=[False, []]
    )
):
    """
    Settings for audio in a course

    ### Usage example:

    ```python
    AudioSettings(
        enabled=True,
        text_to_speech_settings_list=[TextToSpeechSettings()]
    )
    ```
    """

    pass


class Settings(namedtuple("Settings", ["audio_settings"], defaults=[AudioSettings()])):
    """
    Settings for a course

    ### Usage example:
    ```python
        my_settings = Settings()
    ```
    """

    pass


class Course(
    namedtuple(
        "Course",
        [
            "target_language",
            "source_language",
            "special_characters",
            "modules",
            "license",
            "dictionary",
            "repository_url",
            "settings",
        ],
        defaults=[Settings()],
    )
):
    """
    A LibreLingo course

    ### Usage example:

    ```python
    my_course = Course(
        target_language=Language("English", "en"),
        source_language=Language("Spanish", "es"),
        special_characters=[],
        modules=[module1, module2, module3, module4],
        license=License(
            full_name="Attribution 4.0 International (CC BY 4.0)",
            name="CC BY 4.0",
            link="https://creativecommons.org/licenses/by/4.0/"
        ),
        dictionary=[dict_item1, dict_item2, dict_item3, dict_item4],
        repository_url="https://example.com",
        setttings=Settings()
    )
    ```
    """

    pass


class Language(namedtuple("Language", ["name", "code"])):
    """
    Metadata about a language

    ### Usage example:
    ```python
        my_language = Language("English", "en")
    ```
    """

    pass


class License(
    namedtuple(
        "License",
        [
            "name",
            "full_name",
            "link",
        ],
    )
):
    """
    Metadata about the license of a LibreLingo course

    ### Usage example:

    ```python
    License(
        full_name="Attribution 4.0 International (CC BY 4.0)",
        name="CC BY 4.0",
        link="https://creativecommons.org/licenses/by/4.0/"
    )
    ```
    """

    pass


class Module(
    namedtuple(
        "Module",
        [
            "title",
            "skills",
        ],
    )
):
    """
    A module of a LibreLingo course.

    ### Usage examples:

    ```python
    my_module = Module(title="Basics", skills=[skill1, skill2])
    ```
    """

    pass


class Skill(
    namedtuple(
        "Skill",
        [
            "name",
            "id",
            "words",
            "phrases",
            "image_set",
            "dictionary",
            "introduction",
        ],
    )
):
    """
    A skill of a module of a LibreLingo course.

    ### Notes:

    *id*: Needs to be a unique ID. Use uuidv4.

    ### Usage examples:

    ```python
    my_skill = Skill(
        name="Animals",
        id="3adc78da-ea42-4ecd-9e3d-2e0986a3b914",
        words=[word1, word2, word3],
        phrases=[phrases1, phrases2, phrases3],
        image_set=["cat1", "dog2", "horse1"],
        dictionary=[dict_item_1, dict_item_2, dict_item_3, dict_item_4],
        introduction="My *markdown* text",
    )
    ```
    """

    pass


class Word(
    namedtuple(
        "Word",
        [
            "in_target_language",
            "in_source_language",
            "pictures",
        ],
    )
):
    """
    A new word taught in a LibreLingo skill.

    ### Notes:

    *in_source_language*: List of accepted forms in the target language of the
    course. The first item in the list is the main form. The main form is the
    only form that is shown in the course but all forms are accepted as
    answers.

    *in_target_language*: List of accepted forms in the target language of the
    course. The first item in the list is the main form. The main form is the
    only form that is shown in the course but all forms are accepted as
    answers.

    ### Usage example:

    ```python
    my_word = Word(
        in_target_language=["perro"],
        in_target_language=["dog"],
        pictures=["dog1", "dog2", "dog3"]
    )
    ```
    """

    pass


class Phrase(
    namedtuple(
        "Phrase",
        [
            "in_target_language",
            "in_source_language",
        ],
    )
):
    """
    A new phrase taught in a LibreLingo skill.

    ### Notes:

    *in_source_language*: List of accepted forms in the target language of the
    course. The first item in the list is the main form. The main form is the
    only form that is shown in the course but all forms are accepted as
    answers.

    *in_target_language*: List of accepted forms in the target language of the
    course. The first item in the list is the main form. The main form is the
    only form that is shown in the course but all forms are accepted as
    answers.

    ### Usage example:

    ```python
    my_phrase = Phrase(
        in_target_language=["perro"],
        in_target_language=["dog"],
    )
    ```
    """

    pass


class DictionaryItem(
    namedtuple("DictionaryItem", ["word", "definition", "is_in_target_language"])
):
    """
    A dictionary item for a LibreLingo course. It contains the definition of
    a word. The word can be either in the source language or the target
    language.

    ```python
    # Definition in the source language (Spanish in this case)
    my_dict_item_1 = DictionaryItem("hablo", "I speak", False)

    # Definition in the target language (English in this case)
    my_dict_item_2 = DictionaryItem("speak", "hablo", True)
    ```
    """

    pass
