import enum


class SizeUnit(str, enum.Enum):
    G = "g"
    KG = "kg"
    ML = "mL"
    L = "L"
    PCS = "pcs"
    ROLLS = "rolls"
    PACKS = "packs"
    SACHETS = "sachets"
    CANS = "cans"
    BOTTLES = "bottles"


class PriceSource(str, enum.Enum):
    MANUAL = "manual"
    SCRAPED = "scraped"
    CROWDSOURCED = "crowdsourced"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
