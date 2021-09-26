from librelingo_types.data_types import HunspellSettings

hunspell = None


def _run_skill_spellcheck(phrases, words, course):
    if not course.settings:
        return

    if not course.settings.hunspell:
        return

    for phrase in phrases:
        if course.settings.hunspell.target_language is not None:
            for variant in phrase.in_target_language:
                for variant_subword in variant.split():
                    if not course.settings.hunspell.target_language.spell(
                        variant_subword
                    ):
                        raise RuntimeError(
                            f'The {course.target_language.name} phrase "{variant}" is misspelled. The word "{variant_subword}" is unknown.'
                        )

        if course.settings.hunspell.source_language is not None:
            for variant in phrase.in_source_language:
                for variant_subword in variant.split():
                    if not course.settings.hunspell.source_language.spell(
                        variant_subword
                    ):
                        raise RuntimeError(
                            f'The {course.source_language.name} phrase "{variant}" is misspelled. The word "{variant_subword}" is unknown.'
                        )

    for word in words:
        if course.settings.hunspell.source_language is not None:
            for variant in word.in_source_language:
                for variant_subword in variant.split():
                    if not course.settings.hunspell.source_language.spell(
                        variant_subword
                    ):
                        raise RuntimeError(
                            f'The {course.source_language.name} word "{variant}" is misspelled.'
                        )

        if course.settings.hunspell.target_language is not None:
            for variant in word.in_target_language:
                for variant_subword in variant.split():
                    if not course.settings.hunspell.target_language.spell(
                        variant_subword
                    ):
                        raise RuntimeError(
                            f'The {course.target_language.name} word "{variant}" is misspelled.'
                        )


def _convert_hunspell_settings_for_language(raw_language_name):
    language_code = raw_language_name.replace("-", "_")

    # Only import hunspell if actually needed. Still allow mocking it.
    global hunspell
    if not hunspell:
        import hunspell  # type: ignore

    return hunspell.HunSpell(
        f"/usr/share/hunspell/{language_code}.dic",
        f"/usr/share/hunspell/{language_code}.aff",
    )


def _convert_hunspell_settings(raw_settings, course):
    if "Hunspell" not in raw_settings:
        return None

    return HunspellSettings(
        source_language=_convert_hunspell_settings_for_language(
            raw_settings["Hunspell"][course.source_language.name]
        ),
        target_language=_convert_hunspell_settings_for_language(
            raw_settings["Hunspell"][course.target_language.name]
        ),
    )
