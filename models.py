from dataclasses import dataclass, field

@dataclass
class IndependentSection:
    section_id: int
    section_type: str  # 更安全的属性命名

@dataclass
class Interval:
    sections: list[IndependentSection] = field(default_factory=list)
