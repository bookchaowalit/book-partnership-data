import json
import unittest
from importlib.resources import files

from book_partnership_data.capture import normalize
from book_partnership_data.cli import resource, validate


class SourceTests(unittest.TestCase):
    def test_stripe_source_fixture(self):
        raw = (
            "<h1>สมัครเป็นพาร์ทเนอร์ของ Stripe</h1>"
            "<p>Stripe Partner Ecosystem</p>"
            "<h2>SaaS Platforms track</h2>"
        ).encode()
        source = resource("source.json")
        data = normalize(raw, source, "2026-09-08T00:00:00Z")
        data["items"][0]["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
        self.assertEqual(data["items"][0]["category"], "integration-partner")
        self.assertEqual(validate(data)["schema_version"], "partnership.v1")

    def test_drift_markers_come_from_the_source_config(self):
        for entry in files("book_partnership_data").iterdir():
            if not (entry.name.startswith("source") and entry.name.endswith(".json")):
                continue
            source = json.loads(entry.read_text(encoding="utf-8"))
            with self.subTest(source=source["id"]):
                markers = source.get("required_markers")
                self.assertTrue(markers, "every source config ships its drift markers")
                page = ("<main><p>" + " ".join(markers) + "</p></main>").encode()
                normalize(page, source, "2026-09-08T00:00:00Z")
                stricter = dict(source, required_markers=[*markers, "zz-not-on-page"])
                with self.assertRaises(ValueError):
                    normalize(page, stricter, "2026-09-08T00:00:00Z")
                for broken in ([], None, [""], [42]):
                    with self.assertRaises(ValueError):
                        normalize(page, dict(source, required_markers=broken), "2026-09-08T00:00:00Z")
        stranger = dict(resource("source.json"), id="unreviewed-partner-program")
        with self.assertRaises(ValueError):
            normalize(b"<p>Stripe Partner Ecosystem SaaS</p>", stranger, "2026-09-08T00:00:00Z")

    def test_source_drift_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize(b"<h1>unrelated</h1>", resource("source.json"), "2026-09-08T00:00:00Z")

    def test_additional_partner_sources_normalize(self):
        fixtures = {
            "source-hubspot-affiliate-program.json": "Affiliate Program referrals earn commission.",
            "source-microsoft-csp-reseller.json": "Cloud Solution Provider partner program sign in.",
            "source-aws-marketplace-channel.json": "AWS Marketplace Channel helps Channel Partner resell software.",
            "source-shopify-partner-distribution.json": "Shopify Partner Program builds apps and referrals.",
            "source-apple-mfi-licensing.json": "MFi Program provides technical specifications for accessories.",
        }
        for filename, text in fixtures.items():
            with self.subTest(source=filename):
                source = resource(filename)
                data = normalize(f"<p>{text}</p>".encode(), source, "2026-09-08T00:00:00Z")
                data["items"][0]["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
                self.assertEqual(data["items"][0]["category"], source["category"])
                self.assertEqual(validate(data)["schema_version"], "partnership.v1")


if __name__ == "__main__":
    unittest.main()
