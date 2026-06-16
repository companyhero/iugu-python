import unittest

from iugu.errors import format_api_error_message


class FormatApiErrorMessageTest(unittest.TestCase):
    def test_returns_none_for_success_payload(self) -> None:
        self.assertIsNone(
            format_api_error_message(
                {"id": "abc", "status": "pending", "fine_cents": 408}
            )
        )

    def test_formats_errors_dict(self) -> None:
        message = format_api_error_message({"errors": {"base": "Invalid request"}})
        self.assertEqual(message, "base: Invalid request")

    def test_formats_errors_string(self) -> None:
        message = format_api_error_message({"errors": "Invoice Not Found"})
        self.assertEqual(message, "Invoice Not Found")

    def test_formats_rate_limit_response(self) -> None:
        message = format_api_error_message(
            {
                "error": "Too many requests",
                "code": "2000",
                "msg": (
                    "Bloqueado por muitas chamadas não autorizada "
                    "(invoices com status 401)."
                ),
            }
        )
        self.assertEqual(
            message,
            "Too many requests | code=2000 | Bloqueado por muitas chamadas não "
            "autorizada (invoices com status 401).",
        )

    def test_formats_error_without_code_or_msg(self) -> None:
        message = format_api_error_message({"error": "Unauthorized"})
        self.assertEqual(message, "Unauthorized")


if __name__ == "__main__":
    unittest.main()
