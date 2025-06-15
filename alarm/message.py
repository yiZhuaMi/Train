from enum import Enum
from typing import Dict
from dataclasses import dataclass, field


# 报警信息
@dataclass
class AlarmMsg:
    train_number: str
    alarm_content: str