from rest_framework.test import APITestCase


class NewOrderTestCase(APITestCase):
    def test_simple_order(self):
        """Endpoint przyjmuje id nowej subskrypcji, tworzy nowy order"""
        # sprawdź czy subskrypcaj i order mają tego samego clienta
        pass

    def test_calculate_orde_expnesive(self):
        """Sprawdź czy jak kupisz drogą subskrycpjcę to czy jest droga"""
        pass

    def test_calculate_order_cheap(self):
        """Sprawdź czy jak kupisz tanią subskrycpjcę to czy jest tania"""
        pass

    def test_payment_successful(self):
        """Udana płatność. Przyjmuje id orderu i zmienia jego status,
        oraz status pokrewenj subskrypcji"""
        pass

    def test_payment_failed(self):
        """coś wymyślcie"""
        pass

    def test_email_client_after_successful_payment(self):
        """skorzystaj z mocka"""
        pass
