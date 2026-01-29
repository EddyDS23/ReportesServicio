from typing import List, Tuple, Dict, Optional
from datetime import datetime, date, timedelta
import json

from models.activity_model import Activity


class Report:
    """
    Represents a daily activity report.
    
    Attributes:
        responsible (str): Name of the person responsible for the activity
        student (str): Name of the student
        date (date): Report date
        entry_time (str): Entry time in 24h format (HH:MM)
        exit_time (str): Exit time in 24h format (HH:MM)
        instance_hours (str): Total instance hours (automatically calculated)
        activities (List[Activity]): List of activities performed
    """
    
    def __init__(
        self,
        responsible: str = "",
        student: str = "",
        report_date: Optional[date] = None,
        entry_time: str = "00:00",
        exit_time: str = "00:00",
        activities: Optional[List[Activity]] = None
    ):
        """
        Initializes a new report.
        
        Args:
            responsible: Name of responsible person
            student: Student name
            report_date: Report date (defaults to today)
            entry_time: Entry time in HH:MM format
            exit_time: Exit time in HH:MM format
            activities: Optional list of activities
        """
        self.responsible = responsible
        self.student = student
        self.date = report_date if report_date is not None else date.today()
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.activities = activities if activities is not None else []
        self._instance_hours = ""
        
        # Calculate instance hours if times are provided
        if self.entry_time and self.exit_time:
            self.calculate_instance_hours()
    
    # ============================================================================
    # CALCULATION METHODS
    # ============================================================================
    
    def calculate_instance_hours(self) -> str:
        """
        Calculates total instance hours based on entry and exit times.
        
        Returns:
            str: Instance hours in format "HH:MM" or error message
        """
        try:
            if not self._validate_format_hour(self.entry_time):
                self._instance_hours = "Invalid entry time"
                return self._instance_hours
            
            if not self._validate_format_hour(self.exit_time):
                self._instance_hours = "Invalid exit time"
                return self._instance_hours
            
            entry = datetime.strptime(self.entry_time, "%H:%M")
            exit_dt = datetime.strptime(self.exit_time, "%H:%M")
            
            # If exit is before entry, assume next day
            if exit_dt <= entry:
                exit_dt += timedelta(days=1)
            
            difference = exit_dt - entry
            
            hours = int(difference.total_seconds() // 3600)
            minutes = int((difference.total_seconds() % 3600) // 60)
            
            self._instance_hours = f"{hours:02d}:{minutes:02d}"
            return self._instance_hours
            
        except Exception as e:
            self._instance_hours = "Calculate Error"
            return self._instance_hours
    
    @property
    def instance_hours(self) -> str:
        """
        Read-only property to get instance hours.
        
        Returns:
            str: Instance hours in HH:MM format
        """
        if not self._instance_hours:
            self.calculate_instance_hours()
        return self._instance_hours
    
    def calculate_total_activity_hours(self) -> str:
        """
        Calculates total hours from all activities.
        
        Returns:
            str: Total hours in HH:MM format
        """
        total_minutes = sum(
            activity.get_duration_in_minutes() 
            for activity in self.activities
        )
        
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return f"{hours:02d}:{minutes:02d}"
    
    def get_instance_hours_in_minutes(self) -> int:
        """
        Gets instance hours in minutes.
        
        Returns:
            int: Total minutes
        """
        try:
            if not self._instance_hours or ":" not in self._instance_hours:
                self.calculate_instance_hours()
            
            if ":" not in self._instance_hours:
                return 0
            
            hours, minutes = self._instance_hours.split(":")
            return int(hours) * 60 + int(minutes)
            
        except (ValueError, AttributeError):
            return 0
    
    def _validate_format_hour(self, hour: str) -> bool:
        """
        Validates hour format HH:MM.
        
        Args:
            hour: Hour string to validate
            
        Returns:
            bool: True if format is correct
        """
        if not hour or not isinstance(hour, str):
            return False
        
        try:
            datetime.strptime(hour, "%H:%M")
            return True
        except ValueError:
            return False
    
    # ============================================================================
    # ACTIVITY MANAGEMENT METHODS
    # ============================================================================
    
    def add_activity(self, activity: Activity) -> Tuple[bool, str]:
        """
        Adds an activity to the report.
        
        Args:
            activity: Activity to add
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not isinstance(activity, Activity):
            return False, "Invalid activity object"
        
        # Validate activity before adding
        valid, message = activity.complete_validate()
        if not valid:
            return False, f"Invalid activity: {message}"
        
        self.activities.append(activity)
        return True, f"Activity added (Total: {len(self.activities)})"
    
    def remove_activity(self, index: int) -> Tuple[bool, str]:
        """
        Removes an activity by index.
        
        Args:
            index: Activity index to remove (0-based)
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if 0 <= index < len(self.activities):
            removed = self.activities.pop(index)
            return True, f"Activity '{removed.title}' removed"
        return False, "Invalid index"
    
    def edit_activity(self, index: int, updated_activity: Activity) -> Tuple[bool, str]:
        """
        Edits an activity at a specific index.
        
        Args:
            index: Activity index to edit (0-based)
            updated_activity: New activity data
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not (0 <= index < len(self.activities)):
            return False, "Invalid index"
        
        if not isinstance(updated_activity, Activity):
            return False, "Invalid activity object"
        
        # Validate new activity
        valid, message = updated_activity.complete_validate()
        if not valid:
            return False, f"Invalid activity: {message}"
        
        old_title = self.activities[index].title
        self.activities[index] = updated_activity
        return True, f"Activity '{old_title}' updated"
    
    def get_activity(self, index: int) -> Optional[Activity]:
        """
        Gets an activity by index.
        
        Args:
            index: Activity index (0-based)
            
        Returns:
            Activity or None if invalid index
        """
        if 0 <= index < len(self.activities):
            return self.activities[index]
        return None
    
    def get_activity_count(self) -> int:
        """
        Returns the number of activities.
        
        Returns:
            int: Number of activities
        """
        return len(self.activities)
    
    def clear_activities(self):
        """Removes all activities from the report."""
        self.activities.clear()
    
    def move_activity(self, from_index: int, to_index: int) -> Tuple[bool, str]:
        """
        Moves an activity from one position to another.
        
        Args:
            from_index: Source index
            to_index: Destination index
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not (0 <= from_index < len(self.activities)):
            return False, "Invalid source index"
        
        if not (0 <= to_index < len(self.activities)):
            return False, "Invalid destination index"
        
        activity = self.activities.pop(from_index)
        self.activities.insert(to_index, activity)
        return True, f"Activity '{activity.title}' moved"
    
    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================
    
    def validate_times(self) -> Tuple[bool, str]:
        """
        Validates entry and exit times.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not self._validate_format_hour(self.entry_time):
            return False, f"Invalid entry time: '{self.entry_time}'. Use HH:MM format (00:00 - 23:59)"
        
        if not self._validate_format_hour(self.exit_time):
            return False, f"Invalid exit time: '{self.exit_time}'. Use HH:MM format (00:00 - 23:59)"
        
        try:
            h_entry, m_entry = map(int, self.entry_time.split(":"))
            h_exit, m_exit = map(int, self.exit_time.split(":"))
            
            if not (0 <= h_entry <= 23 and 0 <= m_entry <= 59):
                return False, "Entry time out of range (00:00 - 23:59)"
            
            if not (0 <= h_exit <= 23 and 0 <= m_exit <= 59):
                return False, "Exit time out of range (00:00 - 23:59)"
            
        except ValueError:
            return False, "Error processing times"
        
        return True, "Valid times"
    
    def validate_required_fields(self) -> Tuple[bool, str]:
        """
        Validates required fields.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not self.responsible or self.responsible.strip() == "":
            return False, "Responsible name is required"
        
        if not self.student or self.student.strip() == "":
            return False, "Student name is required"
        
        if not self.date:
            return False, "Date is required"
        
        if not self.entry_time:
            return False, "Entry time is required"
        
        if not self.exit_time:
            return False, "Exit time is required"
        
        return True, "All required fields complete"
    
    def validate_activities(self) -> Tuple[bool, str]:
        """
        Validates all activities in the report.
        
        Returns:
            Tuple[bool, str]: (are_valid, error_message)
        """
        if len(self.activities) == 0:
            return False, "Report must contain at least one activity"
        
        for i, activity in enumerate(self.activities):
            valid, message = activity.complete_validate()
            if not valid:
                return False, f"Activity {i+1} invalid: {message}"
        
        return True, "All activities valid"
    
    def complete_validate(self) -> Tuple[bool, str]:
        """
        Performs complete report validation.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Validate required fields
        valid, message = self.validate_required_fields()
        if not valid:
            return False, message
        
        # Validate times
        valid, message = self.validate_times()
        if not valid:
            return False, message
        
        # Validate activities
        valid, message = self.validate_activities()
        if not valid:
            return False, message
        
        return True, "Valid report"
    
    def is_valid(self) -> bool:
        """
        Quick validation check.
        
        Returns:
            bool: True if report is valid
        """
        valid, _ = self.complete_validate()
        return valid
    
    # ============================================================================
    # SEARCH AND FILTER METHODS
    # ============================================================================
    
    def find_activities_by_title(self, title: str) -> List[Activity]:
        """
        Finds activities by title (case-insensitive partial match).
        
        Args:
            title: Title to search for
            
        Returns:
            List[Activity]: List of matching activities
        """
        title_lower = title.lower()
        return [
            activity for activity in self.activities
            if title_lower in activity.title.lower()
        ]
    
    def find_activities_by_time_range(
        self, 
        start_time: str, 
        end_time: str
    ) -> List[Activity]:
        """
        Finds activities within a time range.
        
        Args:
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            
        Returns:
            List[Activity]: List of activities in range
        """
        result = []
        for activity in self.activities:
            if start_time <= activity.start_time <= end_time:
                result.append(activity)
        return result
    
    def get_activities_with_images(self) -> List[Activity]:
        """
        Gets all activities that have images.
        
        Returns:
            List[Activity]: List of activities with images
        """
        return [
            activity for activity in self.activities
            if len(activity.images) > 0
        ]
    
    def get_total_images_count(self) -> int:
        """
        Gets total number of images across all activities.
        
        Returns:
            int: Total image count
        """
        return sum(len(activity.images) for activity in self.activities)
    
    # ============================================================================
    # STATISTICS METHODS
    # ============================================================================
    
    def get_statistics(self) -> Dict:
        """
        Generates report statistics.
        
        Returns:
            Dict: Dictionary with statistics
        """
        return {
            'total_activities': len(self.activities),
            'total_activity_hours': self.calculate_total_activity_hours(),
            'instance_hours': self.instance_hours,
            'total_images': self.get_total_images_count(),
            'activities_with_images': len(self.get_activities_with_images()),
            'average_activity_duration': self._calculate_average_duration(),
            'longest_activity': self._get_longest_activity(),
            'shortest_activity': self._get_shortest_activity()
        }
    
    def _calculate_average_duration(self) -> str:
        """Calculates average activity duration."""
        if not self.activities:
            return "00:00"
        
        total_minutes = sum(
            activity.get_duration_in_minutes() 
            for activity in self.activities
        )
        avg_minutes = total_minutes // len(self.activities)
        
        hours = avg_minutes // 60
        minutes = avg_minutes % 60
        
        return f"{hours:02d}:{minutes:02d}"
    
    def _get_longest_activity(self) -> Optional[str]:
        """Gets the title of the longest activity."""
        if not self.activities:
            return None
        
        longest = max(
            self.activities, 
            key=lambda a: a.get_duration_in_minutes()
        )
        return longest.title
    
    def _get_shortest_activity(self) -> Optional[str]:
        """Gets the title of the shortest activity."""
        if not self.activities:
            return None
        
        shortest = min(
            self.activities, 
            key=lambda a: a.get_duration_in_minutes()
        )
        return shortest.title
    
    # ============================================================================
    # SERIALIZATION METHODS
    # ============================================================================
    
    def to_dict(self) -> Dict:
        """
        Converts report to dictionary.
        
        Returns:
            Dict: Dictionary with all report data
        """
        return {
            'responsible': self.responsible,
            'student': self.student,
            'date': self.date.isoformat(),
            'entry_time': self.entry_time,
            'exit_time': self.exit_time,
            'instance_hours': self.instance_hours,
            'activities': [activity.to_dict() for activity in self.activities],
            'statistics': self.get_statistics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Report':
        """
        Creates report from dictionary.
        
        Args:
            data: Dictionary with report data
            
        Returns:
            Report: New Report instance
        """
        # Parse date
        report_date = None
        if data.get('date'):
            try:
                report_date = date.fromisoformat(data['date'])
            except ValueError:
                report_date = date.today()
        
        # Parse activities
        activities = []
        if data.get('activities'):
            activities = [
                Activity.from_dict(act_data) 
                for act_data in data['activities']
            ]
        
        return cls(
            responsible=data.get('responsible', ''),
            student=data.get('student', ''),
            report_date=report_date,
            entry_time=data.get('entry_time', '00:00'),
            exit_time=data.get('exit_time', '00:00'),
            activities=activities
        )
    
    def to_json(self, filepath: str) -> Tuple[bool, str]:
        """
        Saves report to JSON file.
        
        Args:
            filepath: Path to save JSON file
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
            return True, f"Report saved to {filepath}"
        except Exception as e:
            return False, f"Error saving report: {str(e)}"
    
    @classmethod
    def from_json(cls, filepath: str) -> Tuple[Optional['Report'], str]:
        """
        Loads report from JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Tuple[Optional[Report], str]: (report or None, message)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            report = cls.from_dict(data)
            return report, f"Report loaded from {filepath}"
        except FileNotFoundError:
            return None, "File not found"
        except json.JSONDecodeError:
            return None, "Invalid JSON format"
        except Exception as e:
            return None, f"Error loading report: {str(e)}"
    
    def copy(self) -> 'Report':
        """
        Creates a deep copy of the report.
        
        Returns:
            Report: New instance with same data
        """
        return Report.from_dict(self.to_dict())
    
    # ============================================================================
    # SPECIAL METHODS
    # ============================================================================
    
    def __str__(self) -> str:
        """String representation of report."""
        return (
            f"Report: {self.date.strftime('%Y-%m-%d')}\n"
            f"  Responsible: {self.responsible}\n"
            f"  Student: {self.student}\n"
            f"  Time: {self.entry_time} - {self.exit_time}\n"
            f"  Instance Hours: {self.instance_hours}\n"
            f"  Activities: {len(self.activities)}\n"
            f"  Total Activity Hours: {self.calculate_total_activity_hours()}"
        )
    
    def __repr__(self) -> str:
        """Technical representation of report."""
        return (
            f"Report(responsible='{self.responsible}', "
            f"student='{self.student}', "
            f"date={self.date}, "
            f"activities={len(self.activities)})"
        )
    
    def __eq__(self, other) -> bool:
        """Compares two reports for equality."""
        if not isinstance(other, Report):
            return False
        
        return (
            self.responsible == other.responsible and
            self.student == other.student and
            self.date == other.date and
            self.entry_time == other.entry_time and
            self.exit_time == other.exit_time and
            len(self.activities) == len(other.activities)
        )
    
    def summary(self) -> str:
        """
        Generates a summary of the report.
        
        Returns:
            str: Summary text
        """
        stats = self.get_statistics()
        return (
            f"Report Summary - {self.date.strftime('%Y-%m-%d')}\n"
            f"Student: {self.student}\n"
            f"Responsible: {self.responsible}\n"
            f"Instance: {self.entry_time} to {self.exit_time} ({self.instance_hours})\n"
            f"Activities: {stats['total_activities']}\n"
            f"Total Activity Time: {stats['total_activity_hours']}\n"
            f"Images: {stats['total_images']}"
        )


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("REPORT MODEL USAGE EXAMPLE")
    print("=" * 60)
    
    # Create report
    report = Report(
        responsible="Dr. Smith",
        student="John Doe",
        entry_time="08:00",
        exit_time="17:00"
    )
    
    print("\n1. Report created:")
    print(report)
    
    # Add activities
    activity1 = Activity(
        title="Python Programming",
        description="Developed reporting system with PySide6",
        start_time="09:00",
        end_time="12:00"
    )
    
    activity2 = Activity(
        title="Documentation",
        description="Wrote technical documentation",
        start_time="13:00",
        end_time="15:30"
    )
    
    report.add_activity(activity1)
    report.add_activity(activity2)
    
    print("\n2. Activities added:")
    print(f"   Total activities: {report.get_activity_count()}")
    
    # Statistics
    print("\n3. Statistics:")
    stats = report.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Validate
    print("\n4. Validation:")
    valid, message = report.complete_validate()
    print(f"   Is valid? {valid} - {message}")
    
    # Summary
    print("\n5. Summary:")
    print(report.summary())
    
    print("\n" + "=" * 60)