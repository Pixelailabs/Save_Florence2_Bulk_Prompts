import re
import json
import hashlib

class SaveTextFlorence:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
                "positive_prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "gender_age_replacement": ("STRING", {"default": ""}),
                "hair_replacement": ("STRING", {"default": ""}),
                "body_size_replacement": ("STRING", {"default": ""}),
                "lora_trigger": ("STRING", {"default": ""}),
                "remove_tattoos": ("BOOLEAN", {"default": True, "label_on": "Remove Tattoos", "label_off": "Keep Tattoos"})
            }
        }

    # Enable list input/output
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, True)
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("processed_positive_text", "processed_negative_text")
    FUNCTION = "process_text"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    # Class variable to store the last inputs and outputs
    _cache = {}
    
    def process_text(self, text, positive_prompt_text, negative_prompt_text, 
                    gender_age_replacement, hair_replacement, body_size_replacement, lora_trigger, remove_tattoos):
        # Handle case where inputs are not lists
        if not isinstance(text, list):
            text = [text]
        if not isinstance(positive_prompt_text, list):
            positive_prompt_text = [positive_prompt_text] * len(text)
        if not isinstance(negative_prompt_text, list):
            negative_prompt_text = [negative_prompt_text] * len(text)
        if not isinstance(gender_age_replacement, list):
            gender_age_replacement = [gender_age_replacement] * len(text)
        if not isinstance(hair_replacement, list):
            hair_replacement = [hair_replacement] * len(text)
        if not isinstance(body_size_replacement, list):
            body_size_replacement = [body_size_replacement] * len(text)
        if not isinstance(lora_trigger, list):
            lora_trigger = [lora_trigger] * len(text)
        if not isinstance(remove_tattoos, list):
            remove_tattoos = [remove_tattoos] * len(text)
            
        # Make sure all lists have the same length
        max_length = max(len(text), len(positive_prompt_text), len(negative_prompt_text),
                         len(gender_age_replacement), len(hair_replacement),
                         len(body_size_replacement), len(lora_trigger), len(remove_tattoos))
        
        text = self._extend_list(text, max_length)
        positive_prompt_text = self._extend_list(positive_prompt_text, max_length)
        negative_prompt_text = self._extend_list(negative_prompt_text, max_length)
        gender_age_replacement = self._extend_list(gender_age_replacement, max_length)
        hair_replacement = self._extend_list(hair_replacement, max_length)
        body_size_replacement = self._extend_list(body_size_replacement, max_length)
        lora_trigger = self._extend_list(lora_trigger, max_length)
        remove_tattoos = self._extend_list(remove_tattoos, max_length)
        
        # Generate a cache key for this specific run
        input_data = {
            "text": text,
            "positive_prompt_text": positive_prompt_text,
            "negative_prompt_text": negative_prompt_text,
            "gender_age_replacement": gender_age_replacement,
            "hair_replacement": hair_replacement,
            "body_size_replacement": body_size_replacement,
            "lora_trigger": lora_trigger,
            "remove_tattoos": remove_tattoos
        }
        
        # Create a hash of the inputs to use as cache key
        cache_key = self._get_cache_key(input_data)
        
        # Check if we've already processed these exact inputs
        if cache_key in SaveTextFlorence._cache:
            print("Using cached result for SaveTextFlorence node")
            return SaveTextFlorence._cache[cache_key]
        
        processed_positive_texts = []
        processed_negative_texts = []
        
        for i in range(max_length):
            current_text = text[i]
            
            # Process the text with all replacements
            processed_text = self._apply_text_replacements(
                current_text, 
                gender_age_replacement[i], 
                hair_replacement[i],
                body_size_replacement[i],
                lora_trigger[i],
                remove_tattoos[i]
            )
            
            # Concatenate with positive prompt text at the end
            if positive_prompt_text[i].strip():
                processed_text = f"{processed_text}, {positive_prompt_text[i].strip()}"
            
            processed_positive_texts.append(processed_text)
            processed_negative_texts.append(negative_prompt_text[i])
            
            print(f"Processed text #{i+1}: {processed_text[:100]}...")
        
        # Store the result in cache
        result = (processed_positive_texts, processed_negative_texts)
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
    
    def _apply_text_replacements(self, text, gender_age_replacement, 
                                hair_replacement, body_size_replacement, lora_trigger, remove_tattoos):
        """Apply all text replacements to the input text"""
        
        # First, remove any text between double quotes
        text = re.sub(r'"[^"]*"', '', text)
        
        # Remove unwanted tags (replace with empty string)
        unwanted_tags = [
            r"\bjewelry\b", r"\brings\b", r"\bpiercing\b", r"\bring\b",
            r"\bmedium skin tone\b", r"\bIndian\b", r"\bsaree\b",
            r"\bearrings\b", r"\bnecklace\b", r"\bbracelet\b",
            r"\bwatch\b", r"\bangklet\b", r"\bbody jewelry\b", r"\bnose ring\b",
            r"\bear piercing\b", r"\blip piercing\b", r"\btongue piercing\b"
        ]
        
        # Add tattoo-related patterns to unwanted tags if remove_tattoos is True
        if remove_tattoos:
            tattoo_patterns = [
                r"\btattoo\b", r"\btattoos\b", r"\btattooed\b", r"\btattooing\b",
                r"\bink\b", r"\binked\b", r"\bbody art\b", r"\btribal tattoo\b",
                r"\bsleeve tattoo\b", r"\bface tattoo\b", r"\bneck tattoo\b",
                r"\bback tattoo\b", r"\bchest tattoo\b", r"\barm tattoo\b",
                r"\bleg tattoo\b", r"\bshoulder tattoo\b", r"\bwrist tattoo\b",
                r"\bankle tattoo\b", r"\bfinger tattoo\b", r"\btattoo sleeve\b",
                r"\bfull sleeve\b", r"\bhalf sleeve\b", r"\btattoo design\b",
                r"\btattoo artist\b", r"\btattoo parlor\b", r"\btattoo shop\b"
            ]
            unwanted_tags.extend(tattoo_patterns)
        
        for pattern in unwanted_tags:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        
        # Replace hair color and style keywords
        if hair_replacement:
            hair_patterns = [
                # Compound hair colors (must come before simple colors)
                r"\bdark\s+brown\s+hair\b", r"\blight\s+brown\s+hair\b", r"\bmedium\s+brown\s+hair\b",
                r"\bdark\s+blonde\s+hair\b", r"\blight\s+blonde\s+hair\b", r"\bgolden\s+blonde\s+hair\b",
                r"\bdark\s+red\s+hair\b", r"\bbright\s+red\s+hair\b", r"\bauburn\s+hair\b",
                r"\bjet\s+black\s+hair\b", r"\braven\s+black\s+hair\b", r"\bpitch\s+black\s+hair\b",
                r"\bsalt\s+and\s+pepper\s+hair\b", r"\bsilver\s+grey\s+hair\b", r"\bplatinum\s+silver\s+hair\b",
                r"\bpastel\s+pink\s+hair\b", r"\bhot\s+pink\s+hair\b", r"\brose\s+gold\s+hair\b",
                r"\bdeep\s+purple\s+hair\b", r"\blavender\s+hair\b", r"\bviolet\s+hair\b",
                r"\bmint\s+green\s+hair\b", r"\bemerald\s+green\s+hair\b", r"\bteal\s+hair\b",
                r"\bnavy\s+blue\s+hair\b", r"\bsky\s+blue\s+hair\b", r"\bcobalt\s+blue\s+hair\b",
                r"\bcopper\s+hair\b", r"\bhoney\s+blonde\s+hair\b", r"\bcaramel\s+hair\b",
                r"\bchestnut\s+hair\b", r"\bmahogany\s+hair\b", r"\bburgundy\s+hair\b",
                
                # Simple hair colors (using \s* to match zero or more spaces, then \s+ for one or more)
                r"\bdark\s+hair\b", r"\bbrown\s+hair\b", r"\bblonde\s+hair\b", r"\bred\s+hair\b",
                r"\bblack\s+hair\b", r"\bwhite\s+hair\b", r"\bgray\s+hair\b", r"\bgrey\s+hair\b",
                r"\bsilver\s+hair\b", r"\bpink\s+hair\b", r"\bblue\s+hair\b", r"\bgreen\s+hair\b",
                r"\bpurple\s+hair\b", r"\borange\s+hair\b", r"\byellow\s+hair\b", r"\bmulticolored\s+hair\b",
                # Also match with exactly one space for common cases
                r"\bdark hair\b", r"\bbrown hair\b", r"\bblonde hair\b", r"\bred hair\b",
                r"\bblack hair\b", r"\bwhite hair\b", r"\bgray hair\b", r"\bgrey hair\b",
                r"\bsilver hair\b", r"\bpink hair\b", r"\bblue hair\b", r"\bgreen hair\b",
                r"\bpurple hair\b", r"\borange hair\b", r"\byellow hair\b", r"\bmulticolored hair\b",
                r"\brainbow\s+hair\b", r"\btwo-tone\s+hair\b", r"\bombre\s+hair\b", r"\bbalayage\s+hair\b",
                r"\bhighlighted\s+hair\b", r"\bstreaked\s+hair\b", r"\bfrosted\s+hair\b",
                
                # Hair with highlights/lowlights
                r"\bhair\s+with\s+highlights\b", r"\bhair\s+with\s+lowlights\b", r"\bhair\s+with\s+streaks\b",
                r"\bhighlights\b", r"\blowlights\b", r"\bstreaks\b", r"\bfoils\b",
                
                # Hair descriptors (standalone)
                r"\bblonde\b", r"\brunette\b", r"\bredhead\b", r"\bplatinum\s+blonde\b",
                r"\bdirty\s+blonde\b", r"\bstrawberry\s+blonde\b", r"\bash\s+blonde\b",
                r"\bginger\b", r"\bauburn\b", r"\braven-haired\b", r"\bfair-haired\b",
                
                # Hair texture and styles
                r"\bcurly\s+hair\b", r"\bstraight\s+hair\b", r"\bwavy\s+hair\b", r"\bkinky\s+hair\b",
                r"\bcoily\s+hair\b", r"\bfrizzy\s+hair\b", r"\bsmooth\s+hair\b", r"\bsilky\s+hair\b",
                r"\bthick\s+hair\b", r"\bthin\s+hair\b", r"\bfine\s+hair\b", r"\bcoarse\s+hair\b",
                
                # Hair lengths
                r"\blong\s+hair\b", r"\bshort\s+hair\b", r"\bmedium\s+hair\b", r"\bmedium-length\s+hair\b",
                r"\bshoulder-length\s+hair\b", r"\bwaist-length\s+hair\b", r"\bchin-length\s+hair\b",
                r"\bbuzz\s+cut\b", r"\bcrew\s+cut\b", r"\bvery\s+short\s+hair\b", r"\bvery\s+long\s+hair\b",
                
                # Specific hairstyles
                r"\bbob\s+cut\b", r"\bbob\b", r"\blob\b", r"\bpixie\s+cut\b", r"\bpixie\b",
                r"\bponytail\b", r"\bhigh\s+ponytail\b", r"\blow\s+ponytail\b", r"\bside\s+ponytail\b",
                r"\bpigtails\b", r"\btwin\s+tails\b", r"\bdouble\s+buns\b", r"\bspace\s+buns\b",
                r"\bbun\b", r"\bmessy\s+bun\b", r"\btop\s+knot\b", r"\bchignon\b", r"\bupdo\b",
                r"\bbraids\b", r"\bbraided\s+hair\b", r"\bfrench\s+braid\b", r"\bdutch\s+braid\b",
                r"\bfishtail\s+braid\b", r"\bside\s+braid\b", r"\bbox\s+braids\b", r"\bcornrows\b",
                r"\bbangs\b", r"\bfringe\b", r"\bside-swept\s+bangs\b", r"\bblunt\s+bangs\b",
                r"\bcurtain\s+bangs\b", r"\bwispy\s+bangs\b", r"\bchoppy\s+bangs\b", r"\bmicro\s+bangs\b",
                r"\blayers\b", r"\blayered\s+hair\b", r"\bfeathered\s+hair\b", r"\bshag\b",
                r"\bbeach\s+waves\b", r"\bcrimped\s+hair\b", r"\bpermed\s+hair\b", r"\bnatural\s+hair\b",
                r"\bafro\b", r"\bdreadlocks\b", r"\blocs\b", r"\btwists\b", r"\bprotective\s+style\b",
                r"\bfade\s+cut\b", r"\bfade\b", r"\bundercut\b", r"\bmohawk\b", r"\bfauxhawk\b",
                r"\bshaved\s+sides\b", r"\bside\s+part\b", r"\bmiddle\s+part\b", r"\bno\s+part\b",
                r"\bslicked\s+back\b", r"\bpompadour\b", r"\bquiff\b", r"\bmullet\b",
                r"\bextensions\b", r"\bweave\b", r"\bwig\b", r"\btoupee\b",
                
                # Hair conditions
                r"\bshiny\s+hair\b", r"\bglossy\s+hair\b", r"\bmatte\s+hair\b", r"\bgreasy\s+hair\b",
                r"\bdry\s+hair\b", r"\bdamaged\s+hair\b", r"\bhealthy\s+hair\b", r"\bvoluminous\s+hair\b",
                r"\bflat\s+hair\b", r"\btangled\s+hair\b", r"\btousled\s+hair\b", r"\bmessy\s+hair\b",
                r"\bneat\s+hair\b", r"\bstyled\s+hair\b", r"\bunstyled\s+hair\b", r"\bnatural-looking\s+hair\b"
            ]
            
            # Sort patterns by length (longest first) to ensure more specific patterns match first
            hair_patterns.sort(key=len, reverse=True)
            
            for pattern in hair_patterns:
                text = re.sub(pattern, hair_replacement, text, flags=re.IGNORECASE)
        
        # Replace body size keywords
        if body_size_replacement:
            body_size_patterns = [
                r"\bthin\b", r"\bslim\b", r"\bskinny\b", r"\bpetite\b", r"\bsmall\b",
                r"\bcurvy\b", r"\bvoluptuous\b", r"\bplus size\b", r"\bchubby\b",
                r"\boverweight\b", r"\bbig\b", r"\blarge\b", r"\bheavy\b",
                r"\bmuscular\b", r"\btoned\b", r"\bfit\b", r"\bathletic\b",
                r"\bbuff\b", r"\bripped\b", r"\blean\b", r"\baverage build\b",
                r"\bmedium build\b", r"\bstocky\b", r"\bbroad\b", r"\bwide\b"
            ]
            
            for pattern in body_size_patterns:
                text = re.sub(pattern, body_size_replacement, text, flags=re.IGNORECASE)
        
        # Replace gender patterns
        if gender_age_replacement:
            gender_patterns = [
                r"\bblonde woman\b", r"\bredhead woman\b", r"\bbrunette woman\b",
                r"\b1girl\b", r"\bwoman\b", r"\bman\b", r"\bgirl\b", r"\bboy\b",
                r"\blady\b", r"\bgentleman\b", r"\bmale\b", r"\bfemale\b",
                r"\byoung woman\b", r"\byoung man\b", r"\bmiddle-aged woman\b",
                r"\bmiddle-aged man\b", r"\bolderly woman\b", r"\bolderly man\b",
                r"\bteen girl\b", r"\bteen boy\b", r"\bteenager\b"
            ]
            
            for pattern in gender_patterns:
                text = re.sub(pattern, gender_age_replacement, text, flags=re.IGNORECASE)
        
        # Add LoRA trigger word at the beginning
        if lora_trigger:
            text = f"{lora_trigger.strip()}, {text}"
        
        # Clean up extra spaces and commas
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r',\s*,', ',', text)  # Multiple commas
        text = re.sub(r'^\s*,\s*', '', text)  # Leading comma
        text = re.sub(r'\s*,\s*$', '', text)  # Trailing comma
        text = text.strip()
        
        return text

    @classmethod
    def IS_CHANGED(cls, text, positive_prompt_text, negative_prompt_text, 
                   gender_age_replacement, hair_replacement, body_size_replacement, lora_trigger, remove_tattoos):
        """
        Tells ComfyUI whether this node should be re-executed.
        Returns None to indicate the node should be considered cached.
        """
        return None

NODE_CLASS_MAPPINGS = {
    "SaveTextFlorence": SaveTextFlorence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveTextFlorence": "Text Processor by Aiconomist"
}
