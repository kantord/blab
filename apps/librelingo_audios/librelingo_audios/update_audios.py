from librelingo_utils import audio_id, iterate_phrases
from pathlib import Path
import subprocess
import json
import random
from collections import namedtuple

def update_audios_for_course(output_path, course_name, course, settings):
    if not course.settings.audio_settings.enabled:
        return

    index_file_path = Path(Path(output_path) / "{}.json".format(course_name))

    phrases_in_course = list(iterate_phrases(course))
    phrases_with_existing_audios = _load_index_file(index_file_path)

    # We want to go from the old state (the existing audios) to the new state
    # (the phrases now in the course). So we determine which phrases are the
    # same in both, which are new, and which are no longer needed.
    new_phrase_set = set([_phrase_identity_info_from_phrase(p) for p in phrases_in_course])
    old_phrase_set = set([_phrase_identity_info_from_index(p) for p in phrases_with_existing_audios])

    if settings.destructive:
        phrases_to_keep = set()
    else:
        phrases_to_keep = new_phrase_set & old_phrase_set
    phrases_to_fetch = new_phrase_set - phrases_to_keep
    phrases_to_delete = old_phrase_set - phrases_to_keep

    _delete_phrases(phrases_to_delete, output_path, phrases_with_existing_audios, settings)

    kept_phrases_index_entries = _keep_phrases(phrases_to_keep, phrases_with_existing_audios)
    fetched_phrases_index_entries = _fetch_phrases(phrases_to_fetch, output_path, course, settings)
    result_index = kept_phrases_index_entries + fetched_phrases_index_entries

    if not settings.dry_run:
        _save_index(result_index, index_file_path)

def _load_index_file(file_path):
    if not file_path.is_file():
        return []

    with open(file_path, "r") as f:
        return json.loads(f.read())

def _keep_phrases(phrases_to_keep, existing_index):
    return [p for p in existing_index
            if _phrase_identity_info_from_index(p) in phrases_to_keep]

def _fetch_phrases(phrases, output_path, course, settings):
    return [_fetch_audio_for_phrase(p, output_path, course, settings) for p in phrases]

def _fetch_audio_for_phrase(phrase_identity, output_path, course, settings):
    file_name = audio_id(course.target_language, phrase_identity.text)
    destination_path = Path(Path(output_path) / "{}.mp3".format(file_name))

    # This is where more audio sources would be added with an if statement. For
    # now there is only TTS.
    return _generate_audio_with_tts(phrase_identity, file_name, destination_path, course, settings)

def _generate_audio_with_tts(phrase_identity, file_name, destination_path, course, settings):
    tts_settings_list = course.settings.audio_settings.text_to_speech_settings_list
    if tts_settings_list == []:
        raise RuntimeError("Cannot generate {} because there are no TTS settings configured".format(destination_path))

    chosen_tts_settings = random.choice(tts_settings_list)

    if settings.dry_run:
        print('Would generate {} using {} {}'.format(destination_path, chosen_tts_settings.voice, chosen_tts_settings.engine))
    else:
        print('Generating {} using {} {}'.format(destination_path, chosen_tts_settings.voice, chosen_tts_settings.engine))
        # This is where more more TTS providers would be added with an if statement.
        # For now there is only Polly.
        subprocess.run([
            "aws", "polly", "synthesize-speech",
            "--output-format", "mp3",
            "--voice-id", chosen_tts_settings.voice,
            "--engine", chosen_tts_settings.engine,
            "--text", phrase_identity.text,
            destination_path
        ], stdout = subprocess.DEVNULL)

    return {
        "id": file_name,
        "text": phrase_identity.text,
        "source": "TTS",
        "license": course.license.full_name,
        "ttsProvider": "Polly",
        "ttsVoice": chosen_tts_settings.voice,
        "ttsEngine": chosen_tts_settings.engine
    }

def _delete_phrases(phrases, output_path, existing_index, settings):
    for p in existing_index:
        if _phrase_identity_info_from_index(p) in phrases:
            _delete_audio_for_phrase(p, output_path, settings)

def _delete_audio_for_phrase(index_entry, output_path, settings):
    target_path = Path(Path(output_path) / "{}.mp3".format(index_entry["id"]))

    if not target_path.is_file():
        # It's already not there, for whatever reason
        return

    if settings.dry_run:
        print('Would delete {}'.format(target_path))
    else:
        print('Deleting {}'.format(target_path))
        target_path.unlink()

def _save_index(result_index, index_file_path):
    with open(index_file_path, "w", encoding="utf-8") as f:
        json.dump(sorted(result_index, key=lambda i: i["id"]), f, ensure_ascii=False, indent=4)

# This is the set of information that identifies a phrase as 'the same'. If any
# of these things change, the phrase will be seen as 'new' and re-generated.
PhraseIdentity = namedtuple('PhraseIdentity', 'text source')

def _phrase_identity_info_from_phrase(phrase_object):
    return PhraseIdentity(phrase_object.in_target_language[0], "TTS")

def _phrase_identity_info_from_index(phrase_index_entry):
    return PhraseIdentity(phrase_index_entry["text"], phrase_index_entry["source"])
