"""
Biblical Calendar Generator - Grok Optimized Version

A comprehensive, extensible system for generating Biblical calendar mappings.
Combines the best practices from previous refactorings with additional improvements.

Features:
- Type-safe configuration with validation
- Modular architecture for easy extension
- Comprehensive event system
- Configurable output formats
- Built-in validation and error handling
- Test-friendly design
"""

import json
import logging
from datetime import date, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Protocol, TypedDict
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

class CalendarEntry(TypedDict):
    """A single calendar entry mapping Gregorian to Biblical dates."""
    bore: str
    yehudim: str
    note: str
    moon: str
    aviv: str
    event: str


class MonthConfig(TypedDict):
    """Configuration for a Biblical month."""
    name: str
    gregorian_month: int
    gregorian_day: int
    duration_days: int
    bore_month_num: int
    yehudim_month_name: str


class EventType(Enum):
    """Types of calendar events."""
    FESTIVAL = "festival"
    NEW_MOON = "new_moon"
    OMER = "omer"
    SEASONAL = "seasonal"


@dataclass
class CalendarEvent:
    """Represents a calendar event with metadata."""
    name: str
    note: str
    event_type: EventType
    priority: int = 1  # Higher priority events override lower ones


@dataclass
class GlobalConfig:
    """Global calendar configuration."""
    gregorian_year: int
    bore_year: int
    yehudim_year: int

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not (1 <= self.gregorian_year <= 9999):
            raise ValueError(f"Invalid gregorian_year: {self.gregorian_year}")
        if not (1 <= self.bore_year <= 99999):
            raise ValueError(f"Invalid bore_year: {self.bore_year}")
        if not (1 <= self.yehudim_year <= 99999):
            raise ValueError(f"Invalid yehudim_year: {self.yehudim_year}")


# ============================================================================
# EVENT SYSTEM
# ============================================================================

class EventProvider(Protocol):
    """Protocol for event providers."""
    def get_events_for_date(self, month_name: str, bore_day: int, iso_date: str) -> List[CalendarEvent]:
        """Return events for a specific date."""
        ...


class FixedEventProvider:
    """Provides fixed calendar events."""

    def __init__(self):
        self._events: Dict[str, Dict[int, CalendarEvent]] = {
            "Aviv": {
                1: CalendarEvent("Rosh Hashanah", "Beginning of the Biblical year", EventType.SEASONAL, 10),
                14: CalendarEvent("Pesach", "Pesach begins at sunset", EventType.FESTIVAL, 10),
                15: CalendarEvent("Hag Ha'Matzot", "Start of Hag Ha'Matzot", EventType.FESTIVAL, 10),
                21: CalendarEvent("Bikurim and Omer", "Bikurim (Firstfruits) and first day of the Omer", EventType.SEASONAL, 10),
            },
            "Etanim": {
                1: CalendarEvent("Yom Teruah", "Yom Teruah (Rosh Hashana)", EventType.FESTIVAL, 10),
                10: CalendarEvent("Yom Ha'Kipurim", "Yom Ha'Kipurim (Day of Atonement)", EventType.FESTIVAL, 10),
                15: CalendarEvent("Sucot", "Sucot begins", EventType.FESTIVAL, 10),
            }
        }

    def get_events_for_date(self, month_name: str, bore_day: int, iso_date: str) -> List[CalendarEvent]:
        """Get fixed events for a date."""
        if month_name in self._events and bore_day in self._events[month_name]:
            return [self._events[month_name][bore_day]]
        return []


class OmerEventProvider:
    """Provides Omer-related events."""

    def __init__(self, omer_start_date: Optional[date] = None):
        self.omer_schedule: Dict[str, int] = {}
        if omer_start_date:
            self._generate_omer_schedule(omer_start_date)

    def set_omer_start(self, start_date: date):
        """Set the Omer start date and regenerate schedule."""
        self._generate_omer_schedule(start_date)

    def _generate_omer_schedule(self, start_date: date):
        """Generate the 50-day Omer schedule."""
        self.omer_schedule = {}
        for i in range(50):
            current_day = start_date + timedelta(days=i)
            self.omer_schedule[current_day.isoformat()] = i + 1

    def get_events_for_date(self, month_name: str, bore_day: int, iso_date: str) -> List[CalendarEvent]:
        """Get Omer events for a date."""
        events = []
        if iso_date in self.omer_schedule:
            omer_day = self.omer_schedule[iso_date]
            events.append(CalendarEvent("Omer", f"Omer day {omer_day}", EventType.OMER, 5))

            if omer_day == 50:
                events.append(CalendarEvent("Shavuot", "Shavuot", EventType.FESTIVAL, 10))

        return events


class NewMoonEventProvider:
    """Provides new moon markers."""

    def get_events_for_date(self, month_name: str, bore_day: int, iso_date: str) -> List[CalendarEvent]:
        """Get new moon events."""
        if bore_day == 1 and month_name != "Aviv":
            return [CalendarEvent("New month", f"Beginning of month {month_name}", EventType.NEW_MOON, 3)]
        return []


# ============================================================================
# CALENDAR GENERATOR
# ============================================================================

class CalendarGenerator:
    """
    Main calendar generator with extensible event system.

    This class orchestrates the generation of Biblical calendar entries
    by coordinating multiple event providers and applying business rules.
    """

    def __init__(self, config: GlobalConfig):
        self.config = config
        self.event_providers: List[EventProvider] = [
            FixedEventProvider(),
            OmerEventProvider(),
            NewMoonEventProvider()
        ]

    def add_event_provider(self, provider: EventProvider):
        """Add a custom event provider."""
        self.event_providers.append(provider)

    def calculate_month_start(self, month_cfg: MonthConfig) -> date:
        """
        Calculate the Gregorian start date for a Biblical month.

        The Biblical day begins at sunset, so if the sighting/conjunction
        is on day X, the Biblical month starts on day X+1.
        """
        base_date = date(self.config.gregorian_year, month_cfg["gregorian_month"], month_cfg["gregorian_day"])
        return base_date + timedelta(days=1)

    def find_omer_start(self, months_config: List[MonthConfig]) -> Optional[date]:
        """Find the Omer start date (Aviv 21)."""
        for month_cfg in months_config:
            if month_cfg["name"] == "Aviv":
                aviv_start = self.calculate_month_start(month_cfg)
                # Aviv 21 is 20 days after Aviv 1 (0-indexed)
                return aviv_start + timedelta(days=20)
        return None

    def generate_calendar(self, months_config: List[MonthConfig]) -> Dict[str, CalendarEntry]:
        """
        Generate the complete calendar.

        Args:
            months_config: List of month configurations

        Returns:
            Dictionary mapping ISO dates to calendar entries
        """
        calendar: Dict[str, CalendarEntry] = {}

        # Set up Omer provider with correct start date
        omer_start = self.find_omer_start(months_config)
        if omer_start:
            for provider in self.event_providers:
                if isinstance(provider, OmerEventProvider):
                    provider.set_omer_start(omer_start)

        # Generate entries for each month
        for month_cfg in months_config:
            month_start = self.calculate_month_start(month_cfg)

            for day_offset in range(month_cfg["duration_days"]):
                current_date = month_start + timedelta(days=day_offset)
                bore_day = day_offset + 1
                iso_date = current_date.isoformat()

                entry = self._build_calendar_entry(current_date, month_cfg, bore_day)
                calendar[iso_date] = entry

        logger.info(f"Generated calendar with {len(calendar)} entries")
        return calendar

    def _build_calendar_entry(self, gregorian_date: date, month_cfg: MonthConfig, bore_day: int) -> CalendarEntry:
        """Build a single calendar entry following original logic."""
        iso_date = gregorian_date.isoformat()

        # Format date strings
        bore = f"{bore_day} {month_cfg['name']} {self.config.bore_year}"
        yehudim = f"{bore_day} {month_cfg['yehudim_month_name']} {self.config.yehudim_year}"

        # Initialize
        note = ""
        event = ""

        # Collect all events for this date
        all_events = []
        for provider in self.event_providers:
            events = provider.get_events_for_date(month_cfg["name"], bore_day, iso_date)
            all_events.extend(events)

        # Process events in specific order to match original logic
        # 1. Regular high priority events (Festivals/Seasonal except Shavuot) - set note and event
        for evt in all_events:
            if evt.event_type in [EventType.FESTIVAL, EventType.SEASONAL] and evt.name != "Shavuot":
                if note:
                    note += f" | {evt.note}"
                else:
                    note = evt.note
                event = evt.name

        # 2. Omer events (except Shavuot) - add to note and override event
        for evt in all_events:
            if evt.event_type == EventType.OMER:
                if note:
                    note += f" | {evt.note}"
                else:
                    note = evt.note
                event = evt.name

        # 3. Shavuot - special handling like in original
        for evt in all_events:
            if evt.name == "Shavuot":
                if note:
                    note += f" | {evt.note}"
                else:
                    note = evt.note
                event = evt.name

        # 4. New moon events - only if no other event
        for evt in all_events:
            if evt.event_type == EventType.NEW_MOON and not event:
                if note:
                    note += f" | {evt.note}"
                else:
                    note = evt.note
                event = evt.name

        return CalendarEntry(
            bore=bore,
            yehudim=yehudim,
            note=note,
            moon="visible" if bore_day == 1 else "",
            aviv="confirmed" if month_cfg["name"] == "Aviv" and bore_day == 1 else "",
            event=event
        )


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

class ConfigManager:
    """Manages calendar configuration loading and validation."""

    @staticmethod
    def create_default_config() -> GlobalConfig:
        """Create default configuration for current year."""
        return GlobalConfig(
            gregorian_year=2025,
            bore_year=6025,
            yehudim_year=5785
        )

    @staticmethod
    def get_default_months() -> List[MonthConfig]:
        """Get default month configurations."""
        return [
            {"name": "Aviv", "gregorian_month": 3, "gregorian_day": 31, "duration_days": 29, "bore_month_num": 1, "yehudim_month_name": "Nisán"},
            {"name": "Ziv", "gregorian_month": 4, "gregorian_day": 28, "duration_days": 30, "bore_month_num": 2, "yehudim_month_name": "Iyyar"},
            {"name": "3rd month", "gregorian_month": 5, "gregorian_day": 27, "duration_days": 29, "bore_month_num": 3, "yehudim_month_name": "Sivan"},
            {"name": "4th month", "gregorian_month": 6, "gregorian_day": 27, "duration_days": 30, "bore_month_num": 4, "yehudim_month_name": "Tamuz"},
            {"name": "5th month", "gregorian_month": 7, "gregorian_day": 27, "duration_days": 29, "bore_month_num": 5, "yehudim_month_name": "Av"},
            {"name": "6th month", "gregorian_month": 8, "gregorian_day": 24, "duration_days": 30, "bore_month_num": 6, "yehudim_month_name": "Elul"},
            {"name": "Etanim", "gregorian_month": 9, "gregorian_day": 24, "duration_days": 29, "bore_month_num": 7, "yehudim_month_name": "Tishrei"},
            {"name": "Bul", "gregorian_month": 10, "gregorian_day": 24, "duration_days": 29, "bore_month_num": 8, "yehudim_month_name": "Cheshvan"},
            {"name": "9th month", "gregorian_month": 11, "gregorian_day": 21, "duration_days": 29, "bore_month_num": 9, "yehudim_month_name": "Kislev"},
        ]


# ============================================================================
# OUTPUT HANDLERS
# ============================================================================

class OutputHandler(ABC):
    """Abstract base class for output handlers."""

    @abstractmethod
    def save(self, calendar: Dict[str, CalendarEntry], filename: str) -> None:
        """Save the calendar to a file."""
        pass


class JSONOutputHandler(OutputHandler):
    """Handles JSON output."""

    def save(self, calendar: Dict[str, CalendarEntry], filename: str) -> None:
        """Save calendar as JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(calendar, f, ensure_ascii=False, indent=2)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class BiblicalCalendarApp:
    """Main application class."""

    def __init__(self, config: Optional[GlobalConfig] = None):
        self.config = config or ConfigManager.create_default_config()
        self.generator = CalendarGenerator(self.config)
        self.output_handler = JSONOutputHandler()

    def generate_and_save(self, months_config: Optional[List[MonthConfig]] = None,
                         filename: Optional[str] = None) -> str:
        """
        Generate calendar and save to file.

        Args:
            months_config: Optional custom month configuration
            filename: Optional custom filename

        Returns:
            The filename where the calendar was saved
        """
        logger.info("Starting calendar generation...")

        months = months_config or ConfigManager.get_default_months()
        calendar = self.generator.generate_calendar(months)

        # Keep backward compatibility with the original filename format
        filename = filename or f"{self.config.bore_year}.json"
        self.output_handler.save(calendar, filename)

        logger.info(f"✅ Calendar successfully generated: {filename}")
        return filename

    def add_custom_event_provider(self, provider: EventProvider):
        """Add a custom event provider to the generator."""
        self.generator.add_event_provider(provider)


def main():
    """Main entry point."""
    app = BiblicalCalendarApp()
    app.generate_and_save()


if __name__ == "__main__":
    main()
