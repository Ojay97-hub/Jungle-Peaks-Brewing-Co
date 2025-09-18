from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from unittest.mock import patch

from checkout.models import Order, OrderLineItem
from products.models import Category, Product
from profiles.models import UserProfile


@override_settings(DEFAULT_FROM_EMAIL="orders@example.com")
class CheckoutViewsTestCase(TestCase):
    """ Test cases for checkout views """

    def setUp(self):
        """ Set up test data including user, product, and client session. """
        self.client = Client()

        # ✅ Create a unique test user to avoid duplicate user_id errors
        self.user = User.objects.create_user(
            username=f'testuser_{self._testMethodName}',
            password='testpass'
        )

        # ✅ Ensure a unique UserProfile is created per test
        self.profile, created = UserProfile.objects.get_or_create(
            user=self.user)

        # ✅ Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A test category description"
        )

        # ✅ Create a test product
        self.product = Product.objects.create(
            name="Test Beer",
            sku="TEST123",
            type="Lager",
            abv=5.0,
            description="A refreshing beer",
            category=self.category,
            price=5.00
        )

        # ✅ Session data (shopping bag)
        session = self.client.session
        session["bag"] = {str(self.product.id): 2}  # 2 units of product
        session.save()

    @patch("stripe.PaymentIntent.modify")
    def test_cache_checkout_data(self, mock_stripe_modify):
        """ Test if checkout data is correctly cached
            in Stripe's PaymentIntent. """
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(
            reverse("cache_checkout_data"),
            {
                "client_secret": "test_pid_secret",
                "save_info": "true",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_stripe_modify.assert_called_once()

    @patch("stripe.PaymentIntent.create")
    def test_checkout_page_loads(self, mock_stripe_create):
        """ Test if the checkout page loads correctly. """
        mock_stripe_create.return_value.client_secret = "test_client_secret"
        self.client.login(username="testuser", password="testpass")

        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        self.assertContains(response, "Checkout")

    @patch("stripe.PaymentIntent.create")
    def test_checkout_post_creates_order(self, mock_stripe_create):
        """ Test if submitting checkout form creates an order. """
        mock_stripe_create.return_value.client_secret = "test_client_secret"

        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "John Doe",
                "email": "john@example.com",
                "phone_number": "123456789",
                "country": "GB",
                "postcode": "A1 1AA",
                "town_or_city": "London",
                "street_address1": "123 Brewery Street",
                "street_address2": "",
                "county": "Greater London",
                "client_secret": "test_pid_secret",
            },
        )

        # Order should be created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.full_name, "John Doe")
        self.assertEqual(order.email, "john@example.com")
        self.assertEqual(order.phone_number, "123456789")

        # Order should contain the correct product
        self.assertEqual(order.lineitems.count(), 1)
        line_item = order.lineitems.first()
        self.assertEqual(line_item.product, self.product)
        self.assertEqual(line_item.quantity, 2)

        # Redirects to success page
        self.assertRedirects(
            response, reverse("checkout_success", args=[order.order_number])
        )

    def test_checkout_redirects_when_bag_is_empty(self):
        """ Test checkout redirects to products if the bag is empty. """
        session = self.client.session
        session["bag"] = {}  # Empty bag
        session.save()

        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("products"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "There's nothing in your bag at the moment."
        )

    @patch("checkout.utils.send_mail", return_value=1)
    def test_checkout_success_view(self, mock_send_mail):
        """ Test successful checkout page. """
        order = Order.objects.create(
            full_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            country="GB",
            postcode="A1 1AA",
            town_or_city="London",
            street_address1="123 Brewery Street",
            county="Greater London",
            stripe_pid="test_pid",
        )

        response = self.client.get(
            reverse("checkout_success", args=[order.order_number])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        mock_send_mail.assert_called_once()

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("confirmation email" in str(message) for message in messages))

    @patch("checkout.utils.send_mail", side_effect=Exception("mail down"))
    def test_checkout_success_warns_when_email_fails(self, mock_send_mail):
        order = Order.objects.create(
            full_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            country="GB",
            postcode="A1 1AA",
            town_or_city="London",
            street_address1="123 Brewery Street",
            county="Greater London",
            stripe_pid="test_pid",
        )

        response = self.client.get(reverse("checkout_success", args=[order.order_number]))

        self.assertEqual(response.status_code, 200)
        mock_send_mail.assert_called_once()
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == "warning" for message in messages))
        self.assertTrue(any("confirmation email" not in str(message) for message in messages if message.level_tag == "success"))

    @patch("checkout.utils.send_mail", return_value=1)
    def test_resend_order_confirmation_for_recent_order(self, mock_send_mail):
        order = Order.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            phone_number="123456789",
            country="GB",
            postcode="A1 1AA",
            town_or_city="London",
            street_address1="123 Brewery Street",
            county="Greater London",
            stripe_pid="test_pid",
        )

        session = self.client.session
        session["recent_orders"] = [order.order_number]
        session.save()

        response = self.client.post(
            reverse("resend_order_confirmation", args=[order.order_number]),
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("checkout_success", args=[order.order_number]),
        )
        mock_send_mail.assert_called_once()
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("resent" in str(message) for message in messages))

    def test_resend_order_confirmation_requires_permission(self):
        order = Order.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            phone_number="123456789",
            country="GB",
            postcode="A1 1AA",
            town_or_city="London",
            street_address1="123 Brewery Street",
            county="Greater London",
            stripe_pid="test_pid",
        )

        response = self.client.post(
            reverse("resend_order_confirmation", args=[order.order_number]),
            follow=True,
        )

        self.assertRedirects(response, reverse("home"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("verify permission" in str(message) for message in messages))

    def test_checkout_fails_for_invalid_product(self):
        """ Test if checkout fails when a product
            in the bag does not exist. """
        # Set up session with non-existent product
        session = self.client.session
        session["bag"] = {"99999": 1}  # Non-existent Product ID
        session.save()

        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "John Doe",
                "email": "john@example.com",
                "phone_number": "123456789",
                "country": "GB",
                "postcode": "A1 1AA",
                "town_or_city": "London",
                "street_address1": "123 Brewery Street",
                "street_address2": "",
                "county": "Greater London",
                "client_secret": "test_pid_secret",
            },
        )

        # Ensure redirection to view_bag
        self.assertRedirects(response, reverse("view_bag"))

        # Extract messages
        messages = list(get_messages(response.wsgi_request))

        # Ensure error message is displayed correctly
        expected_message = (
            "One of the products in your bag wasn't found. "
            "Please call us for assistance!"
        )
        self.assertTrue(
            any(expected_message in str(msg) for msg in messages),
            f"Expected message not found in {messages}",
        )


if __name__ == "__main__":
    TestCase.main()
