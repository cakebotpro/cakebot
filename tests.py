import unittest
try:
    import slots
except ImportError:
    raise OSError("Failed to load dependencies")


class Tests(unittest.TestCase):
    def test_slots(self):
        self.assertIsNotNone(slots.emojis)
        self.assertIsNotNone(slots.result())
        self.assertIsNotNone(slots.row())
        self.assertEqual(slots.emojis, "🍎🍊🍐🍋🍉🍇🍒")


if __name__ == "__main__":
    unittest.main()
