<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaveText Node for ComfyUI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #2c3e50;
        }
        code {
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 2px 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        pre {
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>SaveText Node for ComfyUI</h1>
    
    <p>This custom node for ComfyUI allows you to save and process text, typically used for managing prompts in image generation workflows. It is specifically designed for saving text files from the Florence2 node. This node creates bulk prompts to generate bulk images for AI digital models and characters.</p>
    
    <p>Made by Aiconomist from <a href="https://www.youtube.com/@aiconomist">https://www.youtube.com/@aiconomist</a></p>

    <h2>Features</h2>
    <ul>
        <li>Save text to a file in the ComfyUI output directory</li>
        <li>Optional text processing:
            <ul>
                <li>Replace image style descriptions</li>
                <li>Replace gender and age descriptions</li>
                <li>Add LoRA trigger words</li>
            </ul>
        </li>
        <li>Handle both positive and negative prompts</li>
    </ul>

    <h2>Installation</h2>
    <ol>
        <li>Navigate to your ComfyUI custom nodes directory:
            <pre><code>cd ComfyUI/custom_nodes/</code></pre>
        </li>
        <li>Clone this repository:
            <pre><code>git clone https://github.com/yourusername/save-text-node.git</code></pre>
        </li>
        <li>Restart ComfyUI</li>
    </ol>

    <h2>Usage</h2>
    <ol>
        <li>In the ComfyUI interface, find the "Save Text From Florence2 (AICONOMIST)" node in the "utils" category.</li>
        <li>Connect the text output you want to save to the "text" input of the SaveText node.</li>
        <li>Configure the node settings:
            <ul>
                <li><code>file</code>: Name of the output file (default: "output.txt")</li>
                <li><code>enable_replacement</code>: Enable or disable text processing</li>
                <li><code>image_style</code>: Style to replace "The image is" or "The image shows"</li>
                <li><code>gender_age_replacement</code>: Text to replace gender and age descriptions</li>
                <li><code>lora_trigger</code>: LoRA trigger word to add at the beginning</li>
                <li><code>negative_prompt_text</code>: Negative prompt to save</li>
            </ul>
        </li>
    </ol>

    <h2>Example</h2>
    <p>[Add a simple example of how to use the node in a ComfyUI workflow]</p>

    <h2>License</h2>
    <pre>
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
    </pre>

    <h2>Contributing</h2>
    <p>Contributions are welcome! Please feel free to submit a Pull Request.</p>
</body>
</html>