"""The nine menu choices and quota handover, using fake CLI replies only."""
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import channel_profiles, cli, llm, session, writing


@contextmanager
def saved_session():
    names = ('BRAIN', 'SOLO', 'PARTNER', 'NO_QUOTA', 'LAST_AI')
    old = {name: getattr(session, name) for name in names}
    try:
        session.NO_QUOTA = set()
        yield
    finally:
        for name, value in old.items():
            setattr(session, name, value)


@contextmanager
def fake_providers(calls, replies):
    def reply(ai):
        calls.append(ai)
        return replies[ai]

    def claude(*args, **kwargs):
        return type('Reply', (), {'stdout': reply('claude'), 'stderr': ''})()

    with patch.object(llm.shutil, 'which', side_effect=lambda name: name), \
         patch.object(llm, 'run_codex', side_effect=lambda *a, **kw: reply('codex')), \
         patch.object(llm, 'run_agy', side_effect=lambda *a, **kw: reply('gemini')), \
         patch.object(llm.subprocess, 'run', side_effect=claude):
        yield


def test_all_modes_route_writer_editor_and_reader():
    for mode in channel_profiles.BRAINS:
        with saved_session():
            channel_profiles.configure_brain(mode)
            writer, editor = mode.split('-')
            editor = writer if editor == 'only' else editor
            assert session.BRAIN == writer and session.SOLO == mode.endswith('-only')
            calls = []
            def ask(prompt, **kw):
                ai = kw.get('brain') or session.BRAIN
                calls.append(ai)
                session.LAST_AI = ai
                return {}
            with patch.object(llm, 'ask_ai', side_effect=ask), patch.dict(session.RULES, {'Story rules': 'One story.'}):
                writing.edit_scripts([{'topic': 'Topic', 'title': 'Title', 'lines': ['He stopped.', 'She won.']}], {'niche': 'history'})
            assert calls == [editor, editor], (mode, calls)


def test_every_mode_can_continue_through_two_exhausted_ais():
    for mode in channel_profiles.BRAINS:
        with saved_session():
            channel_profiles.configure_brain(mode)
            first = session.BRAIN
            second = llm.other_ai(first)
            third = next(ai for ai in channel_profiles.AI_NAMES if ai not in (first, second))
            calls = []
            replies = {first: "You've hit your limit", second: 'usage limit reached', third: '{"ok":true}'}
            with fake_providers(calls, replies):
                assert llm.ask_ai('task') == {'ok': True}
                assert calls == [first, second, third], (mode, calls)
                assert session.BRAIN == third
                assert session.NO_QUOTA == {first, second}
                assert llm.ask_ai('next task') == {'ok': True}
                assert calls == [first, second, third, third]


def test_exhausted_accounts_are_not_retried_when_all_three_are_empty():
    with saved_session():
        session.NO_QUOTA = set(channel_profiles.AI_NAMES)
        calls = []
        with fake_providers(calls, {}):
            assert llm.ask_ai('task', fatal=False) is None
        assert calls == []


def test_batch_uses_selected_codex_writer_and_migrates_saved_aliases():
    for mode in channel_profiles.BRAINS + ['claude', 'gemini']:
        with saved_session(), patch.object(sys, 'argv', ['make_shorts.py', '1', 'test', mode]), \
             patch.object(cli.rules, 'require_rules'), patch.object(channel_profiles, 'use_channel'), \
             patch.object(channel_profiles, 'load_channel', return_value={'brain': mode}), \
             patch.object(cli.picture_pool, 'prune_cache'), patch.object(cli.short_render, 'prune_work'), \
             patch.object(cli.writing, 'write_scripts', return_value=[]) as write, \
             patch.object(cli.seo, 'seo_pass'):
            cli.main()
            assert write.call_count == 1
            assert session.BRAIN == channel_profiles.normalize_brain(mode).split('-')[0]


if __name__ == '__main__':
    names = [name for name in sorted(globals()) if name.startswith('test_')]
    failed = 0
    for name in names:
        try:
            globals()[name]()
            print(f'PASS {name}')
        except Exception:
            failed += 1
            traceback.print_exc()
    print(f'{len(names) - failed}/{len(names)} passed')
    sys.exit(bool(failed))
