from typing import Tuple
from datetime import datetime, timedelta
import os 


class Activity:
    """
    Represents an individual activity within a daily report.
    
    Attributes:
        title (str): Activity name or title
        description (str): Detailed description of the activity
        start_time (str): Start time in 24h format (HH:MM)
        end_time (str): End time in 24h format (HH:MM)
        duration (str): Automatically calculated duration (HH:MM)
        images (list[str]): List of image file paths
    """

    # Configuration constants
    MAX_IMAGES = 5
    MAX_SIZE_IMAGE_MB = 10
    FORMATS_ALLOW_IMAGE = ['.jpg', '.jpeg', '.png']

    def __init__(self,
                 title: str,
                 description: str,
                 start_time: str = "00:00",
                 end_time: str = "00:00",
                 images: list[str] | None = None):  # ✅ Fixed: Removed None[str]

        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.images = images if images is not None else []
        self._duration = ""

        if self.start_time and self.end_time:
            self.calculate_duration()

    # ============================================================================
    # CALCULATION METHODS
    # ============================================================================

    def calculate_duration(self) -> str:
        """
        Calculates activity duration based on start_time and end_time.
        
        Returns:
            str: Duration in format "HH:MM" or error message
        """
        try:
            # ✅ Fixed: Changed method name
            if not self._validate_format_hour(self.start_time):
                self._duration = "Invalid start time"
                return self._duration

            if not self._validate_format_hour(self.end_time):
                self._duration = "Invalid end time"
                return self._duration

            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")

            # If end is before start, assume next day
            if end <= start:
                end += timedelta(days=1)

            difference = end - start

            hours = int(difference.total_seconds() // 3600)
            minutes = int((difference.total_seconds() % 3600) // 60)

            self._duration = f"{hours:02d}:{minutes:02d}"
            return self._duration

        except Exception as e:  # ✅ Fixed: Better exception handling
            self._duration = "Calculate Error"
            return self._duration

    def get_duration_in_minutes(self) -> int:  # ✅ Fixed: Better name
        """
        Gets the total duration in minutes.
        
        Returns:
            int: Total duration in minutes, 0 if error
        """
        try:
            if not self._duration or ":" not in self._duration:
                self.calculate_duration()

            if ":" not in self._duration:
                return 0

            hours, minutes = self._duration.split(":")
            return int(hours) * 60 + int(minutes)

        except (ValueError, AttributeError):
            return 0

    @property
    def duration(self) -> str:
        """
        Read-only property to get the duration.
        Automatically calculated when hours change.
        
        Returns:
            str: Duration in HH:MM format
        """
        if not self._duration:
            self.calculate_duration()
        return self._duration

    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================

    def validate_hours(self) -> Tuple[bool, str]:
        """
        Validates that start and end times are correct.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # ✅ Fixed: Using correct attribute names
        if not self._validate_format_hour(self.start_time):
            return False, f"Invalid start time: '{self.start_time}'. Use HH:MM format (00:00 - 23:59)"

        if not self._validate_format_hour(self.end_time):
            return False, f"Invalid end time: '{self.end_time}'. Use HH:MM format (00:00 - 23:59)"

        try:
            # ✅ Fixed: Using correct attribute names
            h_start, m_start = map(int, self.start_time.split(":"))
            h_end, m_end = map(int, self.end_time.split(":"))

            if not (0 <= h_start <= 23 and 0 <= m_start <= 59):
                return False, "Start time out of range (00:00 - 23:59)"

            if not (0 <= h_end <= 23 and 0 <= m_end <= 59):
                return False, "End time out of range (00:00 - 23:59)"

        except ValueError:
            return False, "Error processing times"

        return True, "Valid hours"

    def _validate_format_hour(self, hour: str) -> bool:
        """
        Validates that an hour has the correct HH:MM format.
        
        Args:
            hour: String with the hour to validate
            
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

    def validate_required_fields(self) -> Tuple[bool, str]:
        """
        Validates that required fields are complete.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # ✅ Fixed: Using correct attribute names
        if not self.title or self.title.strip() == "":
            return False, "Title is required"

        if not self.description or self.description.strip() == "":
            return False, "Description is required"

        if not self.start_time:
            return False, "Start time is required"

        if not self.end_time:
            return False, "End time is required"

        return True, "All fields complete"

    def complete_validate(self) -> Tuple[bool, str]:
        """
        Performs all activity validations.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Validate required fields
        valid, message = self.validate_required_fields()
        if not valid:
            return False, message

        # Validate hours
        valid, message = self.validate_hours()
        if not valid:
            return False, message

        # Validate images
        valid, message = self.validate_images()
        if not valid:
            return False, message

        return True, "Valid activity"

    # ============================================================================
    # IMAGE MANAGEMENT METHODS
    # ============================================================================

    def add_image(self, path_image: str) -> Tuple[bool, str]:
        """
        Adds an image to the activity with validations.
        
        Args:
            path_image: Image file path
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # ✅ Fixed: Removed 'self' from comparison
        if len(self.images) >= self.MAX_IMAGES:
            return False, f"Limit of {self.MAX_IMAGES} images reached"

        # Validate file exists
        if not os.path.exists(path_image):
            return False, "File does not exist"

        # Validate extension
        extension = os.path.splitext(path_image)[1].lower()
        if extension not in self.FORMATS_ALLOW_IMAGE:
            return False, f"Invalid format. Use: {', '.join(self.FORMATS_ALLOW_IMAGE)}"

        # Validate size
        size_mb = os.path.getsize(path_image) / (1024 * 1024)
        if size_mb > self.MAX_SIZE_IMAGE_MB:
            return False, f"Image too large ({size_mb:.1f}MB). Maximum {self.MAX_SIZE_IMAGE_MB}MB"

        # Add image
        self.images.append(path_image)
        return True, f"Image added ({len(self.images)}/{self.MAX_IMAGES})"

    def delete_image(self, index: int) -> Tuple[bool, str]:
        """
        Deletes an image by its index.
        
        Args:
            index: Image index to delete (0-based)
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if 0 <= index < len(self.images):
            self.images.pop(index)
            return True, "Image deleted"
        return False, "Invalid index"

    def delete_image_by_path(self, path: str) -> Tuple[bool, str]:
        """
        Deletes an image by its path.
        
        Args:
            path: Full image path
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if path in self.images:
            self.images.remove(path)
            return True, "Image deleted"
        return False, "Image not found"

    def reorganize_images(self, new_order: list[int]) -> Tuple[bool, str]:
        """
        Reorders images according to an index list.
        
        Args:
            new_order: List of indices in the new order
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if len(new_order) != len(self.images):
                return False, "Number of indices doesn't match"

            # Validate all indices are valid
            if set(new_order) != set(range(len(self.images))):
                return False, "Invalid indices"

            # Reorder
            new_images = [self.images[i] for i in new_order]
            self.images = new_images
            return True, "Images reordered"

        except (IndexError, TypeError):
            return False, "Error reordering images"

    def validate_images(self) -> Tuple[bool, str]:
        """
        Validates that all images exist and are valid.
        
        Returns:
            Tuple[bool, str]: (are_valid, message)
        """
        if len(self.images) > self.MAX_IMAGES:
            return False, f"Too many images (max: {self.MAX_IMAGES})"

        for i, path in enumerate(self.images):
            if not os.path.exists(path):
                return False, f"Image {i+1} not found: {path}"

            extension = os.path.splitext(path)[1].lower()
            if extension not in self.FORMATS_ALLOW_IMAGE:
                return False, f"Image {i+1} with invalid format"

        return True, "Valid images"  # ✅ Fixed: Added return statement

    def clean_images(self):
        """Removes all images from the activity."""
        self.images.clear()

    def get_number_of_images(self) -> int:  # ✅ Fixed: Better name
        """Returns the number of images in the activity."""
        return len(self.images)

    # ============================================================================
    # CONVERSION AND SERIALIZATION METHODS
    # ============================================================================

    def to_dict(self) -> dict:
        """
        Converts the activity to a dictionary.
        
        Returns:
            dict: Dictionary with all activity data
        """
        return {
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'images': self.images.copy(),
            'number_images': len(self.images)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        """
        Creates an activity from a dictionary.
        
        Args:
            data: Dictionary with activity data
            
        Returns:
            Activity: New Activity instance
        """
        return cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            start_time=data.get('start_time', '00:00'),
            end_time=data.get('end_time', '00:00'),
            images=data.get('images', []).copy() if data.get('images') else []  # ✅ Fixed: typo
        )

    def copy(self) -> 'Activity':  # ✅ Fixed: English name
        """
        Creates a deep copy of the activity.
        
        Returns:
            Activity: New instance with same data
        """
        return Activity.from_dict(self.to_dict())

    # ============================================================================
    # SPECIAL METHODS AND UTILITIES
    # ============================================================================

    def __str__(self) -> str:
        """String representation of the activity."""
        return (
            f"Activity: {self.title}\n"
            f"  Schedule: {self.start_time} - {self.end_time}\n"
            f"  Duration: {self.duration}\n"
            f"  Images: {len(self.images)}"
        )

    def __repr__(self) -> str:
        """Technical representation of the activity."""
        return (
            f"Activity(title='{self.title}', "
            f"start_time='{self.start_time}', "
            f"end_time='{self.end_time}', "
            f"images={len(self.images)})"
        )

    def __eq__(self, other) -> bool:
        """Compares two activities for equality."""
        if not isinstance(other, Activity):
            return False

        return (
            self.title == other.title and
            self.description == other.description and
            self.start_time == other.start_time and
            self.end_time == other.end_time and
            self.images == other.images
        )

    def short_summary(self) -> str:
        """
        Generates a short summary of the activity.
        
        Returns:
            str: Summary in format "Title (HH:MM - HH:MM) - Duration"
        """
        return f"{self.title} ({self.start_time} - {self.end_time}) - {self.duration}"

    def is_valid(self) -> bool:
        """
        Quickly checks if the activity is valid.
        
        Returns:
            bool: True if the activity is valid
        """
        valid, _ = self.complete_validate()
        return valid


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ACTIVITY MODEL USAGE EXAMPLE")
    print("=" * 60)

    # 1. Create basic activity
    activity = Activity(
        title="Documentation Reading",
        description="Review of PySide6 technical documentation",
        start_time="09:00",
        end_time="11:30"
    )

    print("\n1. Activity created:")
    print(activity)

    # 2. Validate
    print("\n2. Validation:")
    valid, message = activity.complete_validate()
    print(f"   Is valid? {valid} - {message}")

    # 3. Duration
    print("\n3. Duration:")
    print(f"   Duration: {activity.duration}")
    print(f"   In minutes: {activity.get_duration_in_minutes()}")

    # 4. Convert to dictionary
    print("\n4. Serialization:")
    data = activity.to_dict()
    print(f"   Dictionary: {data}")

    print("\n" + "=" * 60)