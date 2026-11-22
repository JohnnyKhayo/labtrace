class Sample:
    """Represents a lab sample."""

    STATUSES = ["Collected", "Processing", "Completed", "Archived"]

    def __init__(self, sample_id, sample_type, collected_by, status="Collected", notes=""):
        self.sample_id = sample_id.strip()
        self.sample_type = sample_type.strip()
        self.collected_by = collected_by.strip()
        self.status = status
        self.notes = notes.strip()


