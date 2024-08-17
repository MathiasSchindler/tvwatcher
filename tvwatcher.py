import time
import requests
import json
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File and API configurations
INPUT_FILE = ""
TRANS_FILE = ""
SUMMARY_FILE = ""
TRANSLATION_API_URL = ""
LLAMA_API_URL = ""
HEADERS = {"Content-Type": "application/json"}
SUMMARY_INTERVAL = 30  # Summarize every 30 seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

class NewsHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_position = 0
        self.last_summary_time = 0
        self.new_content = ""

    def on_modified(self, event):
        if event.src_path.endswith(INPUT_FILE):
            self.process_new_content()
            current_time = time.time()
            if current_time - self.last_summary_time >= SUMMARY_INTERVAL:
                self.summarize_content()
                self.last_summary_time = current_time

    def process_new_content(self):
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            file.seek(self.last_position)
            new_content = file.read()
            self.last_position = file.tell()

        cleaned_content = self.clean_text(new_content)
        lines = cleaned_content.split('\n')

        for line in lines:
            if line.strip():
                translated_text = self.translate_text(line.strip())
                self.write_to_output(TRANS_FILE, translated_text)
                self.new_content += translated_text + "\n"

    def clean_text(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        text = ansi_escape.sub('', text)
        text = ''.join(char for char in text if char == '\n' or ord(char) >= 32)
        return text

    def translate_text(self, text):
        payload = {
            "text": text,
            "source_lang": "auto",
            "target_lang": "en"
        }
        try:
            response = requests.post(TRANSLATION_API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            result = json.loads(response.text)
            return result['translations'][0]['text']
        except requests.exceptions.RequestException as e:
            print(f"Error during translation: {str(e)}")
            return f"TRANSLATION ERROR: {text}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"Error processing translation response: {str(e)}")
            return f"PROCESSING ERROR: {text}"

    def summarize_content(self):
        if not self.new_content.strip():
            return

        prompt = f"""Fasse den folgenden englischen Text sehr knapp auf Deutsch zusammen. 
        Konzentriere dich nur auf die wichtigsten Informationen. 
        Verwende maximal 1-2 Sätze pro Thema und insgesamt nicht mehr als 4 Sätze.
        Sei präzise und direkt. Beginne direkt mit der Zusammenfassung, ohne einleitende Sätze.

        Text:
        {self.new_content}

        Zusammenfassung:"""

        payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(LLAMA_API_URL, json=payload)
                response.raise_for_status()
                result = json.loads(response.text)
                summary = result.get('response', 'Keine Zusammenfassung generiert.')
                self.write_to_output(SUMMARY_FILE, summary.strip())
                print(f"\nNeue Zusammenfassung:\n{summary.strip()}\n")
                break
            except requests.exceptions.RequestException as e:
                print(f"Fehler bei der Zusammenfassung (Versuch {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Wiederhole in {RETRY_DELAY} Sekunden...")
                    time.sleep(RETRY_DELAY)
                else:
                    print("Maximale Anzahl von Versuchen erreicht. Überspringe diese Zusammenfassung.")
                    self.write_to_output(SUMMARY_FILE, "FEHLER: Zusammenfassung konnte nicht generiert werden.")
                    print("\nFEHLER: Zusammenfassung konnte nicht generiert werden.\n")
            except json.JSONDecodeError:
                print(f"Fehler beim Dekodieren der Antwort (Versuch {attempt + 1}/{MAX_RETRIES})")
                if attempt < MAX_RETRIES - 1:
                    print(f"Wiederhole in {RETRY_DELAY} Sekunden...")
                    time.sleep(RETRY_DELAY)
                else:
                    print("Maximale Anzahl von Versuchen erreicht. Überspringe diese Zusammenfassung.")
                    self.write_to_output(SUMMARY_FILE, "FEHLER: Antwort konnte nicht dekodiert werden.")
                    print("\nFEHLER: Antwort konnte nicht dekodiert werden.\n")

        self.new_content = ""  # Reset new content after summarization

    def write_to_output(self, filename, text):
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(text + '\n')

def main():
    event_handler = NewsHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    print(f"Combined News Translator and Summarizer started. Watching for changes in {INPUT_FILE}...")
    print("Summaries will be displayed here and written to a file every 30 seconds.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
