from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Callable, Optional, Union

import polars

from quipus.utils.types import EncodingType, OutputType, BINARY_FILE_TYPES


@dataclass
class CraftConfig:
    output_type: OutputType
    encoding_type: Optional[EncodingType]
    template_path: Union[str, Path]
    output_path: Optional[Union[str, Path]]
    output_dir: Optional[Union[str, Path]]
    decide_filename_with: Callable[[dict[str, Any]], str]


def craft_file(craft_config: CraftConfig, data: polars.DataFrame):
    if craft_config.output_type in BINARY_FILE_TYPES:
        _manage_binary_output(craft_config, data)
        return

    for item in data.iter_rows(named=True):
        with open(craft_config.template_path, "r") as file:
            template = file.read()
            rendered = template.format(**item)

        if craft_config.output_path:
            with open(craft_config.output_path, "w", encoding="utf-8") as file:
                file.write(rendered)

        if craft_config.output_dir:
            if not os.path.exists(craft_config.output_dir):
                os.makedirs(craft_config.output_dir)

            filename = craft_config.decide_filename_with(item)
            output_path = os.path.join(craft_config.output_dir, filename)
            with open(
                f"{output_path}.{craft_config.output_type.value}", "w", encoding="utf-8"
            ) as file:
                file.write(rendered)


def _manage_binary_output(craft_config: CraftConfig, data: polars.DataFrame):
    invoke = {OutputType.PDF: craft_pdf}
    invoke[craft_config.output_type](craft_config, data)


def craft_pdf(craft_config: CraftConfig, data: polars.DataFrame):
    raise NotImplementedError()
