class Sample:
    """Represents a lab sample."""

    def __init__(self, sample_id, sample_type, collected_by, status="Collected", notes=""):
        self.sample_id = sample_id.strip()
        self.sample_type = sample_type.strip()
        self.collected_by = collected_by.strip()
        self.status = status
        self.notes = notes.strip()


if __name__ == "__main__":
    s = Sample("SMP-001", "blood", "Khayo")
    print(s.sample_id)
    print(s.sample_type)
    print(s.collected_by)
    print(s.status)
