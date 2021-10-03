from django.http import response
from django.test import Client , TestCase, client
from django.urls import reverse

# Create your tests here.
from .models import *
from django.contrib.auth.models import User

#check login.html
class UserLoginTest(TestCase):

    def setUp(self):
        # Create users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username='6110613020',
            email='6110613020@example.com',
            password='6110613020',
            first_name='Chonlasit',
            last_name='Mooncorn',
        )

        Student.objects.create(user=user1)
    
    def test_login_page(self):
        c = Client()
        response = c.get(reverse('register:login'))
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)
        # Make sure login_page available
        self.assertTemplateUsed(response, 'registers/login.html')
    
    def test_student_userinfo(self):
        # login
        c = Client()
        c.post('/login', {'username' : '6110613020' , 'password': "6110613020"})
        response = c.get(reverse('register:info'))
        # Make sure that status code is 200 and correct username
        self.assertEqual(str(response.context['user']), '6110613020')
        self.assertEqual(response.status_code, 200)
        # Make sure that user access to the login page
        self.assertTemplateUsed(response, 'registers/userinfo.html')
        #if fail
        c.post('/login', {'username' : 'ayaya' , 'password': "ayaya"})
        response = c.get(reverse('register:login'))
        self.assertTemplateUsed(response, 'registers/login.html')

    def test_logout(self):
        c = Client()
        c.post('/login', {'username' : '6110613020' , 'password': "6110613020"})
        c.logout()
        response = c.get(reverse('register:login'))
        self.assertEqual(response.status_code, 200)
 

    def test_admin_index(self):
        #login 
        c = Client()
        c.post('/login', {'username' : 'admin' , 'password': "admin"})
        response = c.get(reverse('register:info'))
        # Make sure that status code is 200 and correct username
        self.assertEqual(str(response.context['user']), 'admin')
        self.assertEqual(response.status_code, 200)
        # Make sure that user access to the login page
        self.assertTemplateUsed(response, 'registers/admin_index.html')
    
    def test_non_user(self):
        c = Client()
        c.login(username='1' , password = '1')
        response = self.client.get(reverse('register:info'))
        self.assertEqual(response.status_code, 302)
    
    def test_upload(self):
        c = Client()
        c.login(username='6110613020' , password = '6110613020')
        response = c.get(reverse('register:upload'))
        c.post('/upload', {'form' : '/images/a.jpg' })
        self.assertTemplateUsed(response, 'registers/upload.html')

    def test_non_user_upload(self):
        response = self.client.get(reverse('register:upload'))
        self.assertEqual(response.status_code, 302)


# check index.html and admin_index.html
class UserIndex(TestCase):
    
    # Create users and student
    def setUp(self):

        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username= '6110613020',
            email='6110613020@example.com',
            password='6110613020',
            first_name='Chonlasit',
            last_name='Mooncorn',
        )
        user2 = User.objects.create_user(
            username= '6210612856',
            email='6210612856@example.com',
            password='6210612856',
            first_name='A',
            last_name='B',
        )
    
        Student.objects.create(user=user1)
        Student.objects.create(user=user2)

        #create subject
        Subject.objects.create(
            subject_id="cn201",
            subject_name = "Object Oriented Programming",
            semester = 2,
            year = 1 ,
            max_seat = 2,
            available = True

        )

        Subject.objects.create(
            subject_id="cn202",
            subject_name = "Data Structure I",
            semester = 1,
            year = 2 ,
            max_seat = 2,
            available = True

        )
        Subject.objects.create(
            subject_id="cn203",
            subject_name = "Data Structure II",
            semester = 2,
            year = 2 ,
            max_seat = 2,
            available = True

        )

    def test_userindex_not_login(self):
        response = self.client.get(reverse('register:index'))
        self.assertEqual(response.status_code, 302)

    # check if user dont register anysubject
    def test_userindex(self):
        #login 
        c = Client()
        c.login(username="6110613020" , password = "6110613020")

        response = c.get(reverse('register:index'))

        #user current subject
        self.assertEqual(response.context["subjects"].count(), 0)
        #subject that user don't register
        self.assertEqual(response.context["other_subject"].count(), 3)
        #user subject current seat
        self.assertEqual(response.context["user_seat"], [])
        #other current seat
        self.assertEqual(response.context["other_seat"], [2,2,2])

        subject = Subject.objects.get(subject_id = "cn201")
        student = Student.objects.get(user = User.objects.get(username = 6110613020))
        
        #add subject
        student.subject.add(subject)

        response = c.get(reverse('register:index'))

        self.assertEqual(response.context["subjects"].count(), 1)
        self.assertEqual(response.context["other_subject"].count(), 2)
        self.assertEqual(response.context["user_seat"], [1])
        self.assertEqual(response.context["other_seat"], [2,2])
   
        #remove subject 
        student.subject.remove(subject)

        response = c.get(reverse('register:index'))

        self.assertEqual(response.context["subjects"].count(), 0)
        self.assertEqual(response.context["other_subject"].count(), 3)
        self.assertEqual(response.context["user_seat"], [])
        self.assertEqual(response.context["other_seat"], [2,2,2])

        #empty subject
        Subject.objects.all().delete()

        response = c.get(reverse('register:index'))

        self.assertEqual(response.context["subjects"].count(), 0)
        self.assertEqual(response.context["other_subject"].count(), 0)
        self.assertEqual(response.context["user_seat"], [])
        self.assertEqual(response.context["other_seat"], [])

    def test_index_admin(self):
        c = Client()
        c.login(username="admin" , password = "admin")

        response = c.get(reverse('register:info'))

        self.assertEqual(response.context["subjects"].count(), 3)

        Subject.objects.all().delete()

        response = c.get(reverse('register:info'))

        self.assertEqual(response.context["subjects"].count(), 0)


#check subject info
class UserSubjectInfoEnroll(TestCase):
    # Create users and student
    def setUp(self):

        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username= '6110613020',
            email='6110613020@example.com',
            password='6110613020',
            first_name='Chonlasit',
            last_name='Mooncorn',
        )
        user2 = User.objects.create_user(
            username= '6210612856',
            email='6210612856@example.com',
            password='6210612856',
            first_name='A',
            last_name='B',
        )
    
        Student.objects.create(user=user1)
        Student.objects.create(user=user2)

        #create subject
        Subject.objects.create(
            subject_id="cn201",
            subject_name = "Object Oriented Programming",
            semester = 2,
            year = 1 ,
            max_seat = 1,
            available = True

        )

        Subject.objects.create(
            subject_id="cn202",
            subject_name = "Data Structure I",
            semester = 1,
            year = 2 ,
            max_seat = 2,
            available = True

        )
        Subject.objects.create(
            subject_id="cn203",
            subject_name = "Data Structure II",
            semester = 2,
            year = 2 ,
            max_seat = 2,
            available = True

        )

    def check_login(self):
        sub = Subject.objects.get(subject_id = "cn201")
        response = self.client.get(reverse('register:subjectinfo', args=(sub.subject_id,)))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('register:subjectinfo', args=(sub.subject_id,)))
        self.assertEqual(response.status_code, 302)

    def test_enroll(self):
        c = Client()
        c.login(username="6110613020" , password = "6110613020")
        stu = Student.objects.get(user = User.objects.get(username = "6110613020"))
        sub = Subject.objects.get(subject_id = "cn201")
        stu.subject.add(sub)
        c.post('/enroll')
        response = c.get(reverse('register:index'))
        self.assertEqual(response.status_code, 200)


    def test_subjectinfo_user(self):

        c = Client()
        c.login(username="6110613020" , password = "6110613020")

        stu = Student.objects.get(user = User.objects.get(username = "6110613020"))
        sub = Subject.objects.get(subject_id = "cn201")
        sub.max_seat = 1
    
        response = c.get(reverse('register:subjectinfo', args=(sub.subject_id,)))
        self.assertEqual(response.context["check_seat"], True)

        stu.subject.add(sub)

        response = c.get(reverse('register:subjectinfo', args=(sub.subject_id,)))
        self.assertEqual(response.context["check_seat"], False)

        stu.subject.remove(sub)
        response = c.get(reverse('register:subjectinfo', args=(sub.subject_id,)))
        self.assertEqual(response.context["check_seat"], True)






        

    
        





