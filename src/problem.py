from typing import Optional


class Problem:
    id: str = ""
    source: str = ""
    multi_input: bool = False
    fileio: bool = False
    input_file_name: Optional[str] = None
    output_file_name: Optional[str] = None

    def file_name(self) -> str:
        return f"{self.source}_{self.id}.cpp"

    def __str__(self) -> str:
        return (
            f"Problem {{ "
            f"\n id: {self.id},"
            f"\n source: {self.source},"
            f"\n multi_input: {self.multi_input},"
            f"\n input_file_name: {self.input_file_name},"
            f"\n output_file_name: {self.output_file_name},"
            f"\n }}"
        )

    def __repr__(self) -> str:
        return (
            f"Problem {{ "
            f"\n id: {self.id},"
            f"\n source: {self.source},"
            f"\n multi_input: {self.multi_input},"
            f"\n input_file_name: {self.input_file_name},"
            f"\n output_file_name: {self.output_file_name},"
            f"\n }}"
        )
