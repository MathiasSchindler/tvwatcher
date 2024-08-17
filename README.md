# News Summarizer

## Übersicht

Dieses Projekt kombiniert Spracherkennung, maschinelle Übersetzung und Textzusammenfassung, um Nachrichtensendungen in Echtzeit zu transkribieren, zu übersetzen und zusammenzufassen. Es nutzt whisper.cpp für die Spracherkennung, madlad400 für die Übersetzung und Llama3.1 für die Zusammenfassung.

## Funktionen

- Echtzeit-Transkription von Sprache aus einem Videostream
- Übersetzung der transkribierten Texte ins Englische
- Generierung von Zusammenfassungen alle 30 Sekunden
- Ausgabe der Zusammenfassungen in eine Datei und auf den Bildschirm

## Voraussetzungen

- Python 3.8+
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [madlad400](https://github.com/google-research/google-research/tree/master/madlad_400) (via ts_server oder llama.cpp)
- [Llama3.1](https://llama.meta.com/) (via [Ollama](https://github.com/ollama/ollama))

## Installation


## Einschränkungen und bekannte Probleme

- Die Genauigkeit hängt stark von der Qualität der Spracherkennung ab.
- Übersetzungs- und Zusammenfassungsfehler können sich verstärken.
- Das System kann Schwierigkeiten haben, den Kontext in Interviewsituationen zu erfassen.
- Gelegentliche Fehlinterpretationen von Namen und Begriffen können auftreten.


## Lizenz

Dieses Projekt wird unter der CC0 1.0 Universell (CC0 1.0) Public Domain Dedication veröffentlicht. Das bedeutet, dass Sie das Werk kopieren, modifizieren, verbreiten und aufführen können, auch für kommerzielle Zwecke, ohne um Erlaubnis zu bitten.

Für mehr Informationen siehe: https://creativecommons.org/publicdomain/zero/1.0/

## Danksagungen

Dieses Projekt wäre nicht möglich ohne die folgenden Projekte und -Modelle:

- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) von Georgi Gerganov
- [Whisper](https://github.com/openai/whisper) von OpenAI
- [MADLAD-400](https://github.com/google-research/google-research/tree/master/madlad_400) von Google Research
- [TextSynth Server (ts_server)](https://bellard.org/ts_server/) von Fabrice Bellard
- [Llama](https://llama.meta.com/) von Meta
- [Ollama](https://github.com/ollama/ollama) für die Bereitstellung und Nutzung von Llama

Ich danke allen Entwicklern und Organisationen, die diese Tools und Modelle der Öffentlichkeit zur Verfügung stellen.
