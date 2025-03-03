import os
import re
import folder_paths
import json
import hashlib

class SaveTextFlorence:
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
                "negative_prompt_text": ("STRING", {"multiline": True, "default": ""})
            }
        }

    # Enable list input/output
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "write_text"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    # Class variable to store the last inputs and outputs
    _cache = {}
    
    def write_text(self, text, file, enable_replacement, image_style, gender_age_replacement, lora_trigger, negative_prompt_text):
        # Handle case where inputs are not lists
        if not isinstance(text, list):
            text = [text]
        if not isinstance(file, list):
            file = [file] * len(text)
        if not isinstance(enable_replacement, list):
            enable_replacement = [enable_replacement] * len(text)
        if not isinstance(image_style, list):
            image_style = [image_style] * len(text)
        if not isinstance(gender_age_replacement, list):
            gender_age_replacement = [gender_age_replacement] * len(text)
        if not isinstance(lora_trigger, list):
            lora_trigger = [lora_trigger] * len(text)
        if not isinstance(negative_prompt_text, list):
            negative_prompt_text = [negative_prompt_text] * len(text)
            
        # Make sure all lists have the same length
        max_length = max(len(text), len(file), len(enable_replacement), 
                         len(image_style), len(gender_age_replacement), 
                         len(lora_trigger), len(negative_prompt_text))
        
        text = self._extend_list(text, max_length)
        file = self._extend_list(file, max_length)
        enable_replacement = self._extend_list(enable_replacement, max_length)
        image_style = self._extend_list(image_style, max_length)
        gender_age_replacement = self._extend_list(gender_age_replacement, max_length)
        lora_trigger = self._extend_list(lora_trigger, max_length)
        negative_prompt_text = self._extend_list(negative_prompt_text, max_length)
        
        # Generate a cache key for this specific run
        input_data = {
            "text": text,
            "file": file,
            "enable_replacement": enable_replacement,
            "image_style": image_style,
            "gender_age_replacement": gender_age_replacement,
            "lora_trigger": lora_trigger,
            "negative_prompt_text": negative_prompt_text
        }
        
        # Create a hash of the inputs to use as cache key
        cache_key = self._get_cache_key(input_data)
        
        # Check if we've already processed these exact inputs
        if cache_key in SaveTextFlorence._cache:
            print("Using cached result for SaveTextFlorence node")
            return SaveTextFlorence._cache[cache_key]
        
        processed_texts = []
        full_path = folder_paths.get_output_directory()
        
        for i in range(max_length):
            current_text = text[i]
            
            # Process the text only if enable_replacement is True
            if enable_replacement[i]:
                processed_text = self.process_text(
                    current_text, 
                    image_style[i], 
                    gender_age_replacement[i], 
                    lora_trigger[i]
                )
            else:
                processed_text = current_text
                
            processed_texts.append(processed_text)
            
            # Write to file
            file_path = os.path.join(full_path, file[i])
            try:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(f"positive: {processed_text}\n")
                    f.write(f"negative: {negative_prompt_text[i]}\n")
                    f.write("---------\n")
                
                print(f"Successfully wrote text #{i+1} to {file_path}")
            except Exception as e:
                print(f"Error writing to file {file_path}: {e}")
        
        # Store the result in cache
        result = (processed_texts,)
        SaveTextFlorence._cache[cache_key] = result
        return result

    def _get_cache_key(self, input_data):
        """Generate a unique hash for the input data to use as a cache key"""
        # Convert input data to a JSON string and hash it
        input_json = json.dumps(input_data, sort_keys=True)
        return hashlib.md5(input_json.encode()).hexdigest()

    def _extend_list(self, lst, target_length):
        """Helper method to extend a list to the target length by repeating the last element"""
        if len(lst) < target_length:
            last_element = lst[-1] if lst else ""
            lst.extend([last_element] * (target_length - len(lst)))
        return lst
    
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
    def IS_CHANGED(cls, text, file, enable_replacement, image_style, gender_age_replacement, lora_trigger, negative_prompt_text):
        """
        Tells ComfyUI whether this node should be re-executed.
        Returns None to indicate the node should be considered cached.
        """
        return None

NODE_CLASS_MAPPINGS = {
    "SaveTextFlorence": SaveTextFlorence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveTextFlorence": "Save Florence Bulk Prompts by Aiconomist"
}
