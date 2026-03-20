import importlib.util
import unittest
from pathlib import Path

import numpy as np

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str, module_name: str):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImageUtilsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if cv2 is None:
            raise unittest.SkipTest("opencv-python is not installed")
        cls.body_normalize = load_module("src/7_auto_human_body/normalize.py", "body_normalize")
        cls.body_contours = load_module("src/7_auto_human_body/findcontours.py", "body_contours")
        cls.pose_normalize = load_module("src/7_auto_human_pose/normalize.py", "pose_normalize")
        cls.pose_contours = load_module("src/7_auto_human_pose/findcontours.py", "pose_contours")

    def make_person_like_image(self):
        image = np.zeros((240, 160, 3), dtype=np.uint8)
        cv2.circle(image, (80, 45), 20, (255, 255, 255), -1)
        cv2.rectangle(image, (60, 65), (100, 180), (255, 255, 255), -1)
        cv2.rectangle(image, (40, 75), (60, 150), (255, 255, 255), -1)
        cv2.rectangle(image, (100, 75), (120, 150), (255, 255, 255), -1)
        cv2.rectangle(image, (62, 180), (78, 235), (255, 255, 255), -1)
        cv2.rectangle(image, (82, 180), (98, 235), (255, 255, 255), -1)
        return image

    def test_normalize_produces_expected_size(self):
        image = self.make_person_like_image()
        self.assertEqual(self.body_normalize.Normalize(image).shape, (90, 60, 3))
        self.assertEqual(self.pose_normalize.Normalize(image).shape, (90, 60, 3))

    def test_contour_comparison_prefers_same_shape(self):
        image = self.make_person_like_image()
        shifted = np.roll(image, 5, axis=1)
        changed = image.copy()
        cv2.rectangle(changed, (0, 0), (25, 25), (255, 255, 255), -1)

        same_score = self.body_contours.CalDiff(image, shifted)
        changed_score = self.body_contours.CalDiff(image, changed)

        self.assertLess(same_score, changed_score)
        self.assertAlmostEqual(
            self.pose_contours.GetDeltValue(image, image),
            0.0,
            places=6,
        )


if __name__ == "__main__":
    unittest.main()
