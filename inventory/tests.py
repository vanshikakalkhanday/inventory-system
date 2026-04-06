from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class CategoryModelTest(TestCase):

    def test_category_creation(self):

        category = Category.objects.create(name="Electronics")

        self.assertEqual(category.name, "Electronics")

        self.assertEqual(str(category), "Electronics")


class ProductModelTest(TestCase):

    def setUp(self):

        self.category = Category.objects.create(name="Electronics")

    def test_product_creation(self):

        product = Product.objects.create(

            name="Laptop",

            description="Gaming laptop",

            price=50000.00,

            quantity=5,

            category=self.category

        )

        self.assertEqual(product.name, "Laptop")

        self.assertEqual(product.price, 50000.00)

        self.assertEqual(product.quantity, 5)

        self.assertEqual(product.category.name, "Electronics")

        self.assertEqual(str(product), "Laptop")

class ProductListViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        Product.objects.create(
            name="Laptop",
            description="Gaming laptop",
            price=50000,
            quantity=5,
            category=self.category
        )

    def test_product_list_page(self):
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/product_list.html')
        self.assertContains(response, "Laptop") 

class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            description="Smartphone",
            price=20000,
            quantity=10,
            category=self.category
        )

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product_detail', args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/product_detail.html')
        self.assertContains(response, "Phone")    

class AddProductViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_add_product(self):
        response = self.client.post(reverse('add_product'), {
            'name': 'TV',
            'description': 'Smart TV',
            'price': 30000,
            'quantity': 3,
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'TV')        