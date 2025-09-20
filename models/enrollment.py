class Enrollment:
    pass

class CapacityPolicy:
    @staticmethod
    def can_register_with_cap(current_enrolled: int, max_capacity: int) -> bool:
        return current_enrolled < max_capacity  # มีเพดาน

    @staticmethod
    def can_register_unlimited() -> bool:
        return True  # ไม่มีเพดาน (-1)
