class Subject:
    @staticmethod
    def is_valid_subject_code(code: str) -> bool:
        # 8 digits; either starts with 0550* (first 5 digits '0550x') OR 9069**** (first 4 digits 9069)
        if len(code) != 8 or not code.isdigit():
            return False
        return code.startswith('0550') or code.startswith('9069')