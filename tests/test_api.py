import secrets
import unittest

try:
    from fastapi.testclient import TestClient

    from aegis.config import Settings
    from apps.api_gateway.main import create_app
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False


@unittest.skipUnless(API_AVAILABLE, "FastAPI test dependencies not installed")
class APITests(unittest.TestCase):
    def setUp(self):
        self.token = secrets.token_urlsafe(32)
        settings = Settings(api_token=self.token, trusted_hosts=("testserver",))
        self.client = TestClient(create_app(settings))

    def test_health_is_public_and_has_security_headers(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")

    def test_dashboard_is_available_locally(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("AegisLLM", response.text)

    def test_dashboard_data_exposes_security_results(self):
        response = self.client.get("/dashboard-data")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["redteam"]["cases"], 8)
        self.assertGreaterEqual(len(payload["capabilities"]), 8)
        self.assertGreaterEqual(len(payload["pipeline"]), 8)
        self.assertGreaterEqual(len(payload["demo_scenarios"]), 6)
        self.assertEqual(payload["security_agents"]["readiness"]["level"], "portfolio_ready")
        self.assertGreaterEqual(len(payload["security_agents"]["coverage"]), 8)
        self.assertIn("owner", payload["security_agents"]["triage"][0])
        self.assertEqual(payload["final_open_step"]["name"], "Conectar n8n")
        self.assertTrue(payload["gates"]["passed"])

    def test_completion_requires_bearer_auth(self):
        self.assertEqual(self.client.post("/v1/secure-completions", json={"prompt": "olá"}).status_code, 401)

    def test_completion_rejects_mass_assignment_fields(self):
        response = self.client.post("/v1/secure-completions", headers={"Authorization": f"Bearer {self.token}"},
                                    json={"prompt": "olá", "tenant_id": "tenant-b"})
        self.assertEqual(response.status_code, 422)

    def test_authenticated_completion(self):
        response = self.client.post("/v1/secure-completions", headers={"Authorization": f"Bearer {self.token}"},
                                    json={"prompt": "consulte pedido", "requested_tool": "order_read"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "allowed")


if __name__ == "__main__":
    unittest.main()
