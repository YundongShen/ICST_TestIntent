"Onboarding document persistence."

import os
from datetime import datetime

class DocumentWriter:


    def __init__(self, output_dir="Result/onboarding_result"):
        print(f"[DOCUMENT WRITER] Initializing document writer, output directory: {output_dir}")
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):

        print(f"[DOCUMENT WRITER] Checking output directory: {self.output_dir}")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"[DOCUMENT WRITER] Created output directory: {self.output_dir}")
        else:
            print(f"[DOCUMENT WRITER] Output directory exists")

    def write_document(self, test_case_id, content, metadata=None):

        print(f"[DOCUMENT WRITER] Starting to write document: {test_case_id}")


        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_case_id}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)


        full_content = self._add_metadata(content, metadata or {})


        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"[DOCUMENT WRITER] Document successfully written: {filepath}")
        except IOError as e:
            print(f"[DOCUMENT WRITER] Error: Unable to write file {filepath}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

        return {
            "success": True,
            "filepath": filepath,
            "filename": filename,
            "size": len(full_content),
            "test_case_id": test_case_id
        }

    def save_document(self, content):

        print("[DOCUMENT WRITER] Saving document")

        try:

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"onboarding_{timestamp}.md"
            filepath = os.path.join(self.output_dir, filename)


            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[DOCUMENT WRITER] Document saved: {filepath}")

            return {
                "status": "success",
                "path": filepath,
                "error": None
            }
        except Exception as e:
            print(f"[DOCUMENT WRITER] Save failed: {e}")
            return {
                "status": "error",
                "path": "",
                "error": str(e)
            }

    @staticmethod
    def _add_metadata(content, metadata):

        print("[DOCUMENT WRITER] Adding metadata")

        metadata_str = "---\n"
        metadata_str += f"user_id: {metadata.get('user_id', 'unknown')}\n"
        metadata_str += f"priority: {metadata.get('priority', 'medium')}\n"
        metadata_str += f"confidence: {metadata.get('confidence', 0):.2f}\n"
        metadata_str += f"generated_at: {datetime.now().isoformat()}\n"
        metadata_str += "---\n\n"

        return metadata_str + content

    def list_documents(self):

        print("[DOCUMENT WRITER] Listing output documents")

        if not os.path.exists(self.output_dir):
            print(f"[DOCUMENT WRITER] Output directory does not exist: {self.output_dir}")
            return []

        files = os.listdir(self.output_dir)
        md_files = [f for f in files if f.endswith('.md')]
        print(f"[DOCUMENT WRITER] Found {len(md_files)} documents")
        return md_files

    @staticmethod
    def read_document(filepath):

        print(f"[DOCUMENT WRITER] Reading document: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"[DOCUMENT WRITER] Document read successfully")
            return content
        except IOError as e:
            print(f"[DOCUMENT WRITER] Error: Unable to read file {filepath}: {e}")
            return None
