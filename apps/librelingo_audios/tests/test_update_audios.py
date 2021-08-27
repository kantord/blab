import re
import subprocess
import inspect
import json

from unittest.mock import patch

from librelingo_fakes import fakes
from librelingo_types import Settings, AudioSettings, TextToSpeechSettings

from librelingo_audios.update_audios import update_audios_for_course
import librelingo_audios.cli as cli

course = fakes.customize(
    fakes.course1,
    settings=Settings(
        audio_settings=AudioSettings(
            enabled=True,
            text_to_speech_settings_list=[TextToSpeechSettings()]
        )
    )
)

empty_course = fakes.customize(
    fakes.courseEmpty,
    settings=Settings(
        audio_settings=AudioSettings(
            enabled=True,
            text_to_speech_settings_list=[TextToSpeechSettings()]
        )
    )
)

def test_dry_run_does_nothing(tmp_path, capsys):
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=True, destructive=False))
    assert len(list(tmp_path.iterdir())) == 0
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Would generate ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
            'Would generate ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )

def test_dry_run_does_nothing_with_destructive(tmp_path, capsys):
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=True, destructive=True))
    assert len(list(tmp_path.iterdir())) == 0
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Would generate ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
            'Would generate ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )

@patch('subprocess.run')
def test_generate_from_scratch(subprocess_run, tmp_path, capsys):
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=False))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
            'Generating ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "foous barus",
        tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3',
    ], stdout = subprocess.DEVNULL)
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_generate_from_scratch_with_destructive(subprocess_run, tmp_path, capsys):
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=True))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
            'Generating ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "foous barus",
        tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3',
    ], stdout = subprocess.DEVNULL)
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_noop_update(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=False))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    assert captured.out == ''
    assert subprocess_run.call_count == 0
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_overwrite_with_destructive(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=True))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
            'Generating ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "foous barus",
        tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3',
    ], stdout = subprocess.DEVNULL)
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_partial_update(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=False))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 1
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_partial_update_with_deletion(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "oldid",
            "text": "an unnecessary phrase",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    _write_dummy_audio_file(tmp_path / 'oldid.mp3')
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=False))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Deleting ' + str(tmp_path / 'oldid.mp3'),
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 1
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_overwrite_with_deletion(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "oldid",
            "text": "an unnecessary phrase",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    _write_dummy_audio_file(tmp_path / 'oldid.mp3')
    update_audios_for_course(tmp_path, 'test', course, cli.Settings(dry_run=False, destructive=True))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Deleting ' + str(tmp_path / 'oldid.mp3'),
            'Generating ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3') + ' using Lupe standard',
            'Generating ' + str(tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3') + ' using Lupe standard',
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 2
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "foous barus",
        tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3',
    ], stdout = subprocess.DEVNULL)
    subprocess_run.assert_any_call([
        "aws", "polly", "synthesize-speech",
        "--output-format", "mp3",
        "--voice-id", "Lupe",
        "--engine", "standard",
        "--text", "lorem ipsum",
        tmp_path / '7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2.mp3',
    ], stdout = subprocess.DEVNULL)
    assert _load_json_file(tmp_path / 'test.json') == [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "7dc37637ce2395ed74d4f6ae0f63e0885536356c8910914d3af8afe05694cab2",
            "text": "lorem ipsum",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ]

@patch('subprocess.run')
def test_delete_all(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "oldid",
            "text": "an unnecessary phrase",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    _write_dummy_audio_file(tmp_path / 'oldid.mp3')
    _write_dummy_audio_file(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3')
    update_audios_for_course(tmp_path, 'test', empty_course, cli.Settings(dry_run=False, destructive=False))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Deleting ' + str(tmp_path / 'oldid.mp3'),
            'Deleting ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3'),
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 0
    assert _load_json_file(tmp_path / 'test.json') == []

@patch('subprocess.run')
def test_delete_all_with_destructive(subprocess_run, tmp_path, capsys):
    _write_json_file(tmp_path / 'test.json', [
        {
            "id": "0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6",
            "text": "foous barus",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
        {
            "id": "oldid",
            "text": "an unnecessary phrase",
            "source": "TTS",
            "license": "foo bar license",
            "ttsProvider": "Polly",
            "ttsVoice": "Lupe",
            "ttsEngine": "standard",
        },
    ])
    _write_dummy_audio_file(tmp_path / 'oldid.mp3')
    _write_dummy_audio_file(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3')
    update_audios_for_course(tmp_path, 'test', empty_course, cli.Settings(dry_run=False, destructive=True))
    assert list(tmp_path.iterdir()) == [tmp_path / 'test.json']
    captured = capsys.readouterr()
    _assert_output_lines(
        [
            'Deleting ' + str(tmp_path / 'oldid.mp3'),
            'Deleting ' + str(tmp_path / '0804b0ba52a7fa507998b7f18d6514876195f12dab6cbe7876b924524a1583f6.mp3'),
        ],
        captured.out,
    )
    assert subprocess_run.call_count == 0
    assert _load_json_file(tmp_path / 'test.json') == []

def _write_dummy_audio_file(file_path):
    with open(file_path, "w") as f:
        f.write("this is a fake audio file")

def _write_json_file(file_path, value):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=4)

def _load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())

def _assert_output_lines(lines, text):
    assert set(lines) == set([l for l in text.split('\n') if l != ''])
