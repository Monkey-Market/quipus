from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Callable, Optional, Union

import polars

from quipus.utils.types import EncodingType, OutputType


@dataclass
class CraftConfig:
    output_type: OutputType
    encoding_type: Optional[EncodingType]
    template_path: Union[str, Path]
    output_path: Optional[Union[str, Path]]
    output_dir: Optional[Union[str, Path]]
    decide_filename_with: Callable[[dict[str, Any]], str]


def craft(
    craft_config: CraftConfig,
    data: polars.DataFrame,
):

    if not craft_config.output_path and not craft_config.output_dir:
        raise Exception()

    invoke = {
        OutputType.HTML: craft_html,
    }

    invoke[craft_config.output_type](craft_config, data)


def craft_html(
    craft_config: CraftConfig,
    data: polars.DataFrame,
):
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
            with open(f"{output_path}.html", "w", encoding="utf-8") as file:
                file.write(rendered)
