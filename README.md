# SaveText Node for ComfyUI

This custom node for ComfyUI allows you to save and process text, typically used for managing prompts in image generation workflows. It is specifically designed for saving text files from the Florence2 node. This node creates bulk prompts to generate bulk images for AI digital models and characters.

Made by Aiconomist from [https://www.youtube.com/@aiconomist](https://www.youtube.com/@aiconomist)

## Features

- Save text to a file in the ComfyUI output directory
- Optional text processing:
  - Replace image style descriptions
  - Replace gender and age descriptions
  - Add LoRA trigger words
- Handle both positive and negative prompts

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```
   cd ComfyUI/custom_nodes/
   ```
2. Clone this repository:
   ```
   git clone https://github.com/Pixelailabs/Save_Florence2_Bulk_Text.git
   ```
3. Restart ComfyUI

## Usage

1. In the ComfyUI interface, find the "Save Text From Florence2 (AICONOMIST)" node in the "utils" category.
2. Connect the text output you want to save to the "text" input of the SaveText node.
3. Configure the node settings:
   - `file`: Name of the output file (default: "output.txt")
   - `enable_replacement`: Enable or disable text processing
   - `image_style`: Style to replace "The image is" or "The image shows"
   - `gender_age_replacement`: Text to replace gender and age descriptions
   - `lora_trigger`: LoRA trigger word to add at the beginning
   - `negative_prompt_text`: Negative prompt to save

## Example

[Add a simple example of how to use the node in a ComfyUI workflow]

## License

MIT License

Copyright (c) 2024 PixelAI LTD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
