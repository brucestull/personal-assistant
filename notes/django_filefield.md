# Django `FileField` Usage

[Django FileField - ChatGPT](https://chat.openai.com/share/0bec38c5-017e-4bab-a89a-af26b7f85fa8)

## Request

I have  a Django application.

I want to create a model `Pdf`. It will have a CharField of `name`, a CharField of `description`.

Help me add a field called `item` which will be an uploaded pdf file?

## Response

Certainly! In your Django application, to add an `item` field that represents an uploaded PDF file to your `Pdf` model, you would use the `FileField` provided by Django. Here's how you can define such a model including the `name`, `description`, and the new `item` field for the PDF file:

```python
from django.db import models

class Pdf(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    item = models.FileField(upload_to='pdfs/')
```

In this example:

- `name` is a `CharField` to store the name of the PDF.
- `description` is another `CharField` to store a brief description of the PDF.
- `item` is a `FileField` where `upload_to='pdfs/'` specifies that uploaded PDF files will be stored in a directory called `pdfs` inside your `MEDIA_ROOT` directory. Make sure to replace `'pdfs/'` with your desired upload directory path if needed.

Don't forget to run `makemigrations` and `migrate` to apply these changes to your database:

```shell
python manage.py makemigrations
python manage.py migrate
```

Additionally, ensure your project is properly configured to handle media files. In your settings.py file, define `MEDIA_URL` and `MEDIA_ROOT` settings:

```python
# settings.py

# Base directory for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL to access media through the browser
MEDIA_URL = '/media/'
```

Lastly, to serve these files during development, you’ll need to update your project’s `urls.py` file to include media file routes:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your url patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This setup will allow your `Pdf` model to store PDF files uploaded by users, accessible via the `item` field.

## `Poppler`

The error you're encountering indicates that `poppler` is not installed on your system, or if it is installed, it's not properly added to the system's PATH environment variable. `poppler` is a dependency for the `pdf2image` library to function correctly because it relies on `poppler` utilities to convert PDF pages to images.

Here's how you can resolve this issue on a Windows system:

### Step 1: Install Poppler

1. **Download Poppler for Windows**: You can find Poppler binaries for Windows from various sources. One such source is the unofficial [Poppler Windows releases](https://github.com/oschwartz10612/poppler-windows/releases/) on GitHub.

2. **Extract the downloaded archive**: Once downloaded, extract the zip file to a location on your system, for example, `C:\poppler-xx\`.

### Step 2: Add Poppler to PATH

After installing Poppler, you need to add its `bin` directory to your system's PATH environment variable so that `pdf2image` can utilize it.

1. **Search for Environment Variables**: Press the Windows key and search for "Edit the system environment variables". Then click on the search result to open System Properties.

2. **Environment Variables**: In the System Properties window, click on the "Environment Variables..." button.

3. **Edit PATH**: Under "System variables", scroll down and find the `Path` variable, then click on "Edit...".

4. **Add Poppler to PATH**: Click on "New" and add the path to the `bin` directory of your Poppler installation (e.g., `C:\poppler-xx\bin`). Click "OK" to close all dialogs.

5. **Restart your Command Prompt or IDE**: For the changes to take effect, you may need to restart your command prompt, PowerShell, or IDE (like Visual Studio Code).

### Step 3: Test the Installation

To verify that Poppler is correctly installed and accessible, you can open a new command prompt or PowerShell window and run the following command:

```cmd
pdftoppm -version
```

If Poppler is correctly installed, this command should display the version of Poppler you have installed. If you receive an error or the command is not recognized, double-check the installation steps and ensure the path is correctly added to the PATH variable.

After ensuring Poppler is installed and correctly set up, try running your Python script again. It should now be able to convert PDFs to images without encountering the `PDFInfoNotInstalledError`.
