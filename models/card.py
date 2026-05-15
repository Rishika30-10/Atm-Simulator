"""
models/card.py
--------------
Card class — represents a physical ATM card.
Handles PIN validation, card blocking after failed attempts.
"""


class Card:
    MAX_ATTEMPTS = 3

    def __init__(self, card_number: str, pin: str, account_id: str):
        self.__card_number  = card_number   # private
        self.__pin          = pin           # private (would be hashed in production)
        self.__account_id   = account_id
        self.__is_blocked   = False
        self.__failed_attempts = 0

    # ── Getters ────────────────────────────────────────────────────
    @property
    def card_number(self) -> str:
        # Only expose last 4 digits for display
        return "**** **** **** " + self.__card_number[-4:]

    @property
    def account_id(self) -> str:
        return self.__account_id

    @property
    def is_blocked(self) -> bool:
        return self.__is_blocked

    # ── PIN Validation ─────────────────────────────────────────────
    def validate_pin(self, entered_pin: str) -> bool:
        if self.__is_blocked:
            raise PermissionError("Card is blocked. Please contact your bank.")

        if entered_pin == self.__pin:
            self.__failed_attempts = 0   # reset on success
            return True
        else:
            self.__failed_attempts += 1
            remaining = self.MAX_ATTEMPTS - self.__failed_attempts
            if remaining <= 0:
                self.__is_blocked = True
                raise PermissionError(
                    "Card blocked after 3 wrong PIN attempts. Contact your bank."
                )
            raise ValueError(
                f"Wrong PIN. {remaining} attempt(s) remaining."
            )

    # ── PIN Change ─────────────────────────────────────────────────
    def change_pin(self, old_pin: str, new_pin: str) -> None:
        if old_pin != self.__pin:
            raise ValueError("Current PIN is incorrect.")
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise ValueError("New PIN must be exactly 4 digits.")
        self.__pin = new_pin

    def __repr__(self):
        return f"Card({self.card_number}, blocked={self.__is_blocked})"
