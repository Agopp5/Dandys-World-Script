"""Voice BRIEF.md with this series' voice and style (mtk voice would use its default brisk style).
Usage: OPENROUTER_API_KEY=... python3 voice_brief.py"""
import argparse
import mtk.core as core
import mtk_cli

core.VOICE = "Achird"
core.STYLE = ("patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; "
              "unhurried, moderate pace, with a short pause after each sentence")
mtk_cli.voice(argparse.Namespace(brief="BRIEF.md", voice="Achird"))
