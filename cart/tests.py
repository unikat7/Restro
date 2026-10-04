from django.test import TestCase
from django.urls import reverse
from menu.models import Category, MenuItem


class CartAuthenticationTests(TestCase):
	def test_anonymous_user_cannot_add_item_to_cart(self):
		category = Category.objects.create(name='Test Category', slug='test-category')
		item = MenuItem.objects.create(
			category=category,
			name='Test Item',
			slug='test-item',
			description='Test description',
			price=10,
			is_available=True,
		)

		response = self.client.post(
			reverse('cart:cart_add', args=[item.id]),
			{'quantity': 1},
		)

		self.assertRedirects(
			response,
			f"/accounts/login/?next=/cart/add/{item.id}/",
		)
