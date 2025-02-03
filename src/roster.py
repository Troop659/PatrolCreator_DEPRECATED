import re
from collections import defaultdict

from pypdf import PdfReader

from src.scout import Scout


class Roster:

    parser = re.compile(
        r"\b\d\d?\s(?P<first_n>[a-zA-Z]+)\s((?P<middle_i>[A-Z])\s)?" +
        r"(?P<last_n>[a-zA-Z]+)\s([a-zA-Z]+\s)?" +
        r"(?P<age>\d\d\b)"
    )

    def __init__(self, file_path: str):
        self.file_path = file_path

        try:
            self.reader = PdfReader(file_path)
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong creating the PDF Reader {e}"
            )

        self.pages = self.reader.pages
        self.n_pages = len(self.reader.pages)

        self._parse_scouts()

    def _parse_scouts(self):

        self.scouts: set[Scout] = set()

        self.all_text = ""
        relevant_text = ""
        rank_str = ""
        for page in self.pages:
            for line in page.extract_text().split("\n"):
                line = Roster._replace_ligatures(line)
                relevant_text += line + "\n"

                # Once we reach a new rank of scouts, add the prev ones to set
                if "YOUTH MEMBERS: " in line:
                    rank_str = self._parse_section(
                        line, relevant_text, rank_str
                    )
                    relevant_text = ""

                if "ADULT MEMBERS" in line and relevant_text:
                    rank_str = self._parse_section(
                        line, relevant_text, rank_str
                    )
                    relevant_text = ""

                if rank_str == "EAGLE":
                    break

    def _parse_section(
                self,
                line: str,
                relevant_text: str,
                rank_str: str
            ) -> str:
        """Parses a "Youth Members" section and returns the next rank"""

        if rank_str == "EAGLE":
            return rank_str

        matches = Roster.parser.finditer(relevant_text)
        for match in matches:
            scout = Scout._from_match(match, rank_str)
            if scout.is_active:
                self.scouts.add(scout)

        rank_str = line.replace("YOUTH MEMBERS:", "").split(" ")[1]
        self.all_text += relevant_text

        return rank_str

    def as_dict(self) -> dict[str, list[Scout]]:
        scout_dict = defaultdict(list)
        for scout in self.scouts:
            scout_dict[scout.rank.name].append(scout)

        return scout_dict

    def count_dict(self) -> dict[str, int]:
        return {k: len(v) for k, v in self.as_dict().items()}

    @staticmethod
    def _replace_ligatures(text: str) -> str:
        ligatures = {
            "\x00": "fi",
        }
        for search, replace in ligatures.items():
            text = text.replace(search, replace)
        return text

    def __str__(self):
        return f"Roster({self.file_path}) ({self.n_pages} pages)"
