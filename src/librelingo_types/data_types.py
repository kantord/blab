from collections import namedtuple


class TextToSpeechSettings(
    namedtuple(
        "TextToSpeechSettings",
        [
            "provider",
            "voice",
            "engine",
        ],
        defaults=["Polly", "Lupe", "standard"],
    )
):
    """
    Settings about how to use TTS to generate audios

    ### Usage example:

    >>> TextToSpeechSettings(
    ...     provider="Polly",
    ...     voice="Aditi",
    ...     engine="standard"
    ... )
    TextToSpeechSettings(provider='Polly', voice='Aditi', engine='standard')
    """

    pass


# pylint: disable=line-too-long
class AudioSettings(
    namedtuple(
        "AudioSettings",
        [
            "enabled",
            "text_to_speech_settings_list",
        ],
        defaults=[False, []],
    )
):
    """
    Settings for audio in a course

    ### Usage example:

    >>> AudioSettings(
    ...     enabled=True,
    ...     text_to_speech_settings_list=[TextToSpeechSettings()]
    ... )
    AudioSettings(enabled=True, text_to_speech_settings_list=[TextToSpeechSettings(provider='Polly', voice='Lupe', engine='standard')])
    """

    pass


class HunspellSettings(
    namedtuple(
        "HunspellSettings",
        [
            "source_language",
            "target_language",
        ],
        defaults=[None, None],
    )
):
    """
    Settings for hunspell spell checking

    ### Usage example:

    >>> HunspellSettings(
    ...     source_language="en-US",
    ...     target_language="es-ES",
    ... )
    HunspellSettings(source_language='en-US', target_language='es-ES')
    """

    pass


# pylint: disable=line-too-long
class Settings(
    namedtuple(
        "Settings",
        ["audio_settings", "hunspell"],
        defaults=[AudioSettings(), HunspellSettings()],
    )
):
    """
    Settings for a course

    ### Usage example:

    >>> Settings()
    Settings(audio_settings=AudioSettings(enabled=False, text_to_speech_settings_list=[]), hunspell=HunspellSettings(source_language=None, target_language=None))
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
            "course_dir",
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
        course_dir="some_language/course",
        settings=Settings()
    )
    ```
    """

    pass


class Language(namedtuple("Language", ["name", "code"])):
    """
    Metadata about a language

    ### Usage example:

    >>> Language("English", "en")
    Language(name='English', code='en')
    """

    pass


# pylint: disable=line-too-long
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

    >>> License(
    ...     full_name="Attribution 4.0 International (CC BY 4.0)",
    ...     name="CC BY 4.0",
    ...     link="https://creativecommons.org/licenses/by/4.0/"
    ... )
    License(name='CC BY 4.0', full_name='Attribution 4.0 International (CC BY 4.0)', link='https://creativecommons.org/licenses/by/4.0/')
    """

    pass


class Module(
    namedtuple(
        "Module",
        [
            "title",
            "filename",
            "skills",
        ],
    )
):
    """
    A module of a LibreLingo course.

    ### Usage examples:

    ```python
    my_module = Module(title="Basics", filename="basic/module.yaml", skills=[skill1, skill2])
    ```
    """

    pass


class Skill(
    namedtuple(
        "Skill",
        [
            "name",
            "filename",
            "id",
            "words",
            "phrases",
            "characters",
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
        filename="basic/skills/hello.yaml",
        id="3adc78da-ea42-4ecd-9e3d-2e0986a3b914",
        words=[word1, word2, word3],
        phrases=[phrases1, phrases2, phrases3],
        characters=[character1, character2, character3]
        image_set=["cat1", "dog2", "horse1"],
        dictionary=[dict_item_1, dict_item_2, dict_item_3, dict_item_4],
        introduction="My *markdown* text",
    )
    ```
    """

    pass


# pylint: disable=line-too-long
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

    >>> Word(
    ...     in_target_language=["perro"],
    ...     in_source_language=["dog"],
    ...     pictures=["dog1", "dog2", "dog3"]
    ... )
    Word(in_target_language=['perro'], in_source_language=['dog'], pictures=['dog1', 'dog2', 'dog3'])
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

    >>> Phrase(
    ...     in_target_language=["perro", "can"],
    ...     in_source_language=["dog"],
    ... )
    Phrase(in_target_language=['perro', 'can'], in_source_language=['dog'])
    """

    pass

class Character(
    namedtuple("Character", ["character", "transliteration", "ipa_pronounciation"])
):
    """
    A new character taught in a LibreLingo skill. These are used for teaching 
    languages which use a different script or characters than what the learner's
    source language uses. These are taught in lessons using the transliteration(s)
    and pronounciation of the character and it's sounds.

    A character in LibreLingo could either be a single character, or a combination
    of characters, depending on what makes sense for that specific language. There
    should be two Character entries if a letter has both lowercase and uppercase.

    ipa_pronounciation is how the character is written in the Internation Phonetic
    Alphabet (IPA). It is a list as in many languages a character can represent 
    several sounds. Knowing this can help with pronounciation or differentiating 
    similar characters and sound blends. Read the Wikipedia article on 
    https://en.wikipedia.org/wiki/International_Phonetic_Alphabet. 

    A long sound macron on an 'a' in Te Reo Māori
    >>> Character("ā", ["aa"], ["/aː/"])
    Character(character='ā', transliteration=['aa'], ipa_pronounciation=['/aː/'])

    The Г character in Ukranian (which uses the Cyrillic script).
    >>> Character("Г", ["H"], ["/ɦ/"])
    Character(character='Г', transliteration=['H'], ipa_pronounciation=['/ɦ/'])
    """
    
    pass

class DictionaryItem(
    namedtuple("DictionaryItem", ["word", "definition", "is_in_target_language"])
):
    """
    A dictionary item for a LibreLingo course. It contains the definition of
    a word. The word can be either in the source language or the target
    language.

    Definition in the source language (Spanish in this case)
    >>> DictionaryItem("hablo", "I speak", False)
    DictionaryItem(word='hablo', definition='I speak', is_in_target_language=False)

    Definition in the target language (English in this case)
    >>> DictionaryItem("speak", "hablo", True)
    DictionaryItem(word='speak', definition='hablo', is_in_target_language=True)
    """

    pass


class PhraseIdentity(namedtuple("PhraseIdentity", ["text", "source"])):
    """
    This is the set of information that identifies a phrase as 'the same'. If any
    of these things change, the phrase will be seen as 'new' and re-generated.
    """

    pass
