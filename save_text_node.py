import os
import re
import folder_paths
from server import PromptServer

class SaveText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
                "file": ("STRING", {"default": "output.txt"}),
                "enable_replacement": ("BOOLEAN", {
                    "default": True, "label_on": "Yes", "label_off": "No"
                }),
                "image_style": ("STRING", {"default": ""}),
                "gender_age_replacement": ("STRING", {"default": ""}),
                "lora_trigger": ("STRING", {"default": ""}),
                "negative_prompt_text": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "write_text"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def write_text(self, text, file, enable_replacement, image_style, gender_age_replacement, lora_trigger, negative_prompt_text):
        full_path = folder_paths.get_output_directory()
        file = os.path.join(full_path, file)

        # Process the text only if enable_replacement is True
        if enable_replacement:
            processed_text = self.process_text(text, image_style, gender_age_replacement, lora_trigger)
        else:
            processed_text = text

        try:
            with open(file, "a") as f:
                f.write(f"positive: {processed_text}\n")
                f.write(f"negative: {negative_prompt_text}\n")
                f.write("---------\n")
            
            return (processed_text,)
        except Exception as e:
            print(f"Error writing to file: {e}")
            return (text,)

    def process_text(self, text, image_style, gender_age_replacement, lora_trigger):
        # Replace "The image is" or "The image shows"
        if image_style:
            text = re.sub(r"^(The image is|The image shows)\s+", f"{image_style} ", text)

        # Replace gender and age
        if gender_age_replacement:
            gender_age_patterns = [
                r"\ba (young |middle-aged |blonde )?(woman|man)\b",
                r"\ban (young |middle-aged |blonde )?(woman|man)\b"
            ]
            for pattern in gender_age_patterns:
                text = re.sub(pattern, gender_age_replacement, text)

        # Add LoRA trigger word at the beginning
        if lora_trigger:
            text = f"{lora_trigger.strip()} {text}"

        return text

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "SaveText": SaveText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveText": "Save Text From Florence2 (AICONOMIST)"
}