from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from messagerie.models import ThreadModel, MessageModel
from .forms import ThreadForm, MessageForm

class MessagerieViewsTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects._create_user(email='user1@exemple.com', password='password1')
        self.user2 = get_user_model().objects._create_user(email='user2@exemple.com', password='password2')
    def test_create_thread_view(self):
        self.client.force_login(self.user1) # simulate user's connexion (authetificated)
        response = self.client.get(reverse('create-thread')) # send GET request to view create-thread using the test's client
        print(response) #It uses the reverse function to obtain the URL of the view from its name. Then, it stores the response in the response variable.
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('create-thread'), {'email': self.user2.email})
        self.assertEqual(response.status_code, 302)  # Redirect after creating the thread

        # Verify that the thread has been created
        thread = ThreadModel.objects.filter(user=self.user1, receiver=self.user2)
        self.assertTrue(thread.exists())

    def test_thread_view(self):
        self.client.force_login(self.user1)

        # Create a thread
        thread = ThreadModel.objects.create(user=self.user1, receiver=self.user2)
        response = self.client.get(reverse('thread', args=[thread.pk]))
        self.assertEqual(response.status_code, 200)

    def test_list_threads_view(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)

    def test_create_message_view(self):
        self.client.force_login(self.user1)

        # Create a thread
        thread = ThreadModel.objects.create(user=self.user1, receiver=self.user2)

        response = self.client.post(reverse('create-message', args=[thread.pk]), {'message': 'Hello'})
        self.assertEqual(response.status_code, 302)  # Redirect after creating the message

        # Verify that the message has been created
        message = MessageModel.objects.filter(thread=thread, sender_user=self.user1, body='Hello')
        self.assertTrue(message.exists())

# Create your tests here.
