# Django Tests using Mock

* Need to work on understanding these concepts better.

## Using an Instantiated Object

```python
    def test_application_list_method(self):
        """
        Tests for the 'application_list' method using real objects.
        """
        self.app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        self.app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        self.app_03 = Application.objects.create(
            name="App 03",
            description="Description 03",
        )
        self.project_01 = Project.objects.create(
            name="Project 01",
            description="Description 01",
        )
        self.project_01.applications.add(self.app_01, self.app_02)
        self.project_02 = Project.objects.create(
            name="Project 02",
            description="Description 02",
        )
        # Either of these two lines to relate project to application will work.
        # self.project_02.applications.add(self.app_03)
        # self.app_03.project.add(self.project_02)
        self.project_02.applications.add(self.app_03)
        admin_instance = ProjectAdmin(model=Project, admin_site=None)
        result_01 = admin_instance.application_list(obj=self.project_01)
        self.assertEqual(len(result_01), 2)
        self.assertIn(self.app_01, result_01)
        self.assertIn(self.app_02, result_01)
        self.assertNotIn(self.app_03, result_01)
        result_02 = admin_instance.application_list(obj=self.project_02)
        self.assertEqual(len(result_02), 1)
        self.assertIn(self.app_03, result_02)
        self.assertNotIn(self.app_01, result_02)
```

## Using Mock

```python
    def test_application_list_method_mock(self):
        """
        Tests for the 'application_list' method using a mock.
        """
        # Set up the mock
        mock_obj = Mock()
        mock_applications = Mock()
        type(mock_obj).applications = PropertyMock(
            return_value=mock_applications,
        )

        # Define the fake applications list
        fake_applications = ["app1", "app2", "app3"]
        mock_applications.all.return_value = fake_applications

        # Initialize your admin class
        admin_instance = ProjectAdmin(model=Project, admin_site=None)

        # Call the method and check the result
        result = admin_instance.application_list(obj=mock_obj)
        self.assertEqual(result, fake_applications)
```

