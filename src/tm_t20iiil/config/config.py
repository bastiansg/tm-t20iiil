from pydantic import NonNegativeInt, StrictBytes
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    print_completion_command: StrictBytes = b"\x1d\x72\x01"
    status_format_mask: NonNegativeInt = 0b11110000
    status_format_value: NonNegativeInt = 0
    paper_near_end_mask: NonNegativeInt = 0b00000011
    paper_out_mask: NonNegativeInt = 0b00001100


config = Config()
