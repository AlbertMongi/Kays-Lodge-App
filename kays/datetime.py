# Importing timezone from django.utils
from django.utils import timezone

# Example usage of timezone.now()
now = timezone.now()

# Print the current datetime in UTC timezone
print(f"Current datetime in UTC: {now}")

# You can also convert the datetime to a specific timezone if needed
local_time = now.astimezone(timezone.get_current_timezone())
print(f"Current datetime in local timezone: {local_time}")
