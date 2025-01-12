# import openai
# import PyPDF2  # Add this for PDF processing
# from django.shortcuts import render
# from .forms import ResumeForm
# import re
# import os

# openai.api_key = os.getenv('OPENAI_API_KEY')
# print(f"OPENAI_API_KEY from .env: {os.getenv('OPENAI_API_KEY')}")

# def resume_form(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, request.FILES)

#         if form.is_valid():
#             # Check if a PDF file was uploaded
#             if request.FILES.get("resume_pdf"):
#                 uploaded_file = request.FILES["resume_pdf"]

#                 # Extract text from the uploaded PDF
#                 try:
#                     pdf_reader = PyPDF2.PdfReader(uploaded_file)
#                     extracted_text = ""
#                     for page in pdf_reader.pages:
#                         extracted_text += page.extract_text()

#                     # Debugging output
#                     print("Extracted Text from PDF:", extracted_text[:500])  # Display first 500 characters

#                     # Format the input as a conversation
#                     messages = [
#                         {"role": "system", "content": "You are a professional career advisor."},
#                         {"role": "user", "content": f"Provide suggestions to improve the following resume:\n\n{extracted_text}"}
#                     ]

#                     # Call the OpenAI ChatCompletion API
#                     response = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=messages,
#                         max_tokens=1000,
#                         temperature=0.7
#                     )

#                     # Extract the assistant's reply
#                     suggestions = response['choices'][0]['message']['content'].strip()
#                     # Parse the suggestions into HTML bullets
#                     parsed_suggestions = format_suggestions_as_bullets(suggestions)

#                     # Render the response in the thank_you page
#                     return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})

#                 except Exception as e:
#                     error_message = "There was an error processing your PDF file. Please try again."
#                     return render(request, 'resume/resume_form.html', {'form': form, 'error_message': error_message})
#             else:
#                 # If the form data is submitted instead of a PDF
#                 resume_data = {
#                     "full_name": form.cleaned_data['full_name'],
#                     "email": form.cleaned_data['email'],
#                     "phone_number": form.cleaned_data['phone_number'],
#                     "linkedin": form.cleaned_data['linkedin'],
#                     "professional_summary": form.cleaned_data['professional_summary'],
#                     "skills": form.cleaned_data['skills'],
#                     "experience": form.cleaned_data['experience'],
#                     "education": form.cleaned_data['education'],
#                     "certifications": form.cleaned_data['certifications'],
#                     "projects": form.cleaned_data['projects'],
#                     "awards": form.cleaned_data['awards'],
#                     "languages": form.cleaned_data['languages'],
#                     "portfolio_url": form.cleaned_data['portfolio_url'],
#                     "availability": form.cleaned_data['availability']
#                 }

#                 # Format the input as a conversation
#                 messages = [
#                     {"role": "system", "content": "You are a professional career advisor."},
#                     {"role": "user", "content": f"Provide suggestions to improve the following resume:\n\n{resume_data}"}
#                 ]

#                 try:
#                     # Call the OpenAI ChatCompletion API
#                     response = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=messages,
#                         max_tokens=1000,
#                         temperature=0.7
#                     )

#                     # Extract the assistant's reply
#                     suggestions = response['choices'][0]['message']['content'].strip()
#                     # Parse the suggestions into HTML bullets
#                     parsed_suggestions = format_suggestions_as_bullets(suggestions)

#                     # Render the response in the thank_you page
#                     return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})
#                 except Exception as e:
#                     return render(request, 'resume/thank_you.html', {'error': str(e)})

#     else:
#         form = ResumeForm()

#     return render(request, 'resume/resume_form.html', {'form': form})


# def format_suggestions_as_bullets(suggestions):
#     """
#     Convert the ChatGPT suggestions into structured HTML bullets grouped under categories.
#     Handles long inputs and edge cases gracefully.
#     """
#     # Sanity check for input
#     if not suggestions or not isinstance(suggestions, str):
#         return "<p>No suggestions provided.</p>"

#     # Define a regex pattern to match section headers
#     pattern = r"(\d+\.\s\*\*.*?\*\*:)"  # Example: "1. **Title**:"

#     # Split suggestions into sections using regex
#     sections = re.split(pattern, suggestions)

#     if len(sections) <= 1:
#         # If no sections detected, return suggestions as a paragraph
#         return f"<p>{suggestions.strip()}</p>"

#     formatted_html = ""
#     for i in range(1, len(sections), 2):
#         try:
#             # Extract section title and content
#             section_title = sections[i].strip("*: ")
#             section_content = sections[i + 1].strip() if i + 1 < len(sections) else ""

#             # Limit processing to prevent potential freezes
#             if len(section_content) > 5000:  # Prevent excessively long content
#                 section_content = section_content[:5000] + "..."

#             # Split content into bullets (lines starting with "-")
#             bullets = re.split(r"-\s", section_content)
#             bullet_list = "".join([f"<li>{bullet.strip()}</li>" for bullet in bullets if bullet.strip()])

#             # Build HTML structure
#             formatted_html += f"<h3>{section_title}</h3><ul>{bullet_list}</ul>"
#         except Exception as e:
#             # Log and skip problematic sections
#             print(f"Error processing section: {e}")
#             continue

#     # Return formatted HTML or fallback to plain paragraph
#     return formatted_html or f"<p>{suggestions.strip()}</p>"


import openai
import PyPDF2  # Add this for PDF processing
from django.shortcuts import render
from .forms import ResumeForm
import re
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
print(f"OPENAI_API_KEY from .env: {os.getenv('OPENAI_API_KEY')}")

# def resume_form(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, request.FILES)

#         if form.is_valid():
#             job_position = form.cleaned_data.get('job_position', '')
#             job_description = form.cleaned_data.get('job_description', '')

#             # Check if a PDF file was uploaded
#             if request.FILES.get("resume_pdf"):
#                 uploaded_file = request.FILES["resume_pdf"]

#                 # Extract text from the uploaded PDF
#                 try:
#                     pdf_reader = PyPDF2.PdfReader(uploaded_file)
#                     extracted_text = ""
#                     for page in pdf_reader.pages:
#                         extracted_text += page.extract_text()

#                     # Debugging output
#                     print("Extracted Text from PDF:", extracted_text[:500])  # Display first 500 characters

#                     # Format the input as a conversation
#                     messages = [
#                         {"role": "system", "content": "You are a professional career advisor."},
#                         {"role": "user", "content": f"Provide suggestions to improve the following resume for the position of '{job_position}' based on the job description:\n\n{job_description}\n\nResume:\n\n{extracted_text}"}
#                     ]

#                     # Call the OpenAI ChatCompletion API
#                     response = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=messages,
#                         max_tokens=1000,
#                         temperature=0.7
#                     )

#                     # Extract the assistant's reply
#                     suggestions = response['choices'][0]['message']['content'].strip()
#                     # Parse the suggestions into HTML bullets
#                     parsed_suggestions = format_suggestions_as_bullets(suggestions)

#                     # Render the response in the thank_you page
#                     return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})

#                 except Exception as e:
#                     error_message = "There was an error processing your PDF file. Please try again."
#                     return render(request, 'resume/resume_form.html', {'form': form, 'error_message': error_message})
#             else:
#                 # If the form data is submitted instead of a PDF
#                 resume_data = {
#                     "full_name": form.cleaned_data['full_name'],
#                     "email": form.cleaned_data['email'],
#                     "phone_number": form.cleaned_data['phone_number'],
#                     "linkedin": form.cleaned_data['linkedin'],
#                     "professional_summary": form.cleaned_data['professional_summary'],
#                     "skills": form.cleaned_data['skills'],
#                     "experience": form.cleaned_data['experience'],
#                     "education": form.cleaned_data['education'],
#                     "certifications": form.cleaned_data['certifications'],
#                     "projects": form.cleaned_data['projects'],
#                     "awards": form.cleaned_data['awards'],
#                     "languages": form.cleaned_data['languages'],
#                     "portfolio_url": form.cleaned_data['portfolio_url'],
#                     "availability": form.cleaned_data['availability']
#                 }

#                 # Format the input as a conversation
#                 messages = [
#                     {"role": "system", "content": "You are a professional career advisor."},
#                     {"role": "user", "content": f"Provide suggestions to improve the following resume for the position of '{job_position}' based on the job description:\n\n{job_description}\n\nResume:\n\n{resume_data}"}
#                 ]

#                 try:
#                     # Call the OpenAI ChatCompletion API
#                     response = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=messages,
#                         max_tokens=1000,
#                         temperature=0.7
#                     )

#                     # Extract the assistant's reply
#                     suggestions = response['choices'][0]['message']['content'].strip()
#                     # Parse the suggestions into HTML bullets
#                     parsed_suggestions = format_suggestions_as_bullets(suggestions)

#                     # Render the response in the thank_you page
#                     return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})
#                 except Exception as e:
#                     return render(request, 'resume/thank_you.html', {'error': str(e)})

#     else:
#         form = ResumeForm()

#     return render(request, 'resume/resume_form.html', {'form': form})

def resume_form(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            # Extract job position and description
            job_position = form.cleaned_data.get('job_position', 'Not provided')
            job_description = form.cleaned_data.get('job_description', 'Not provided')

            if request.FILES.get("resume_pdf"):
                return handle_pdf_submission(request, request.FILES["resume_pdf"], job_position, job_description, form)
            else:
                return handle_form_submission(request, form.cleaned_data, job_position, job_description)

    else:
        form = ResumeForm()

    return render(request, 'resume/resume_form.html', {'form': form})


def handle_form_submission(request, form_data, job_position, job_description):
    """Process a manually filled form submission."""
    try:
        # Extract form data into a dictionary
        resume_data = {
            "full_name": form_data['full_name'],
            "email": form_data['email'],
            "phone_number": form_data['phone_number'],
            "linkedin": form_data['linkedin'],
            "professional_summary": form_data['professional_summary'],
            "skills": form_data['skills'],
            "experience": form_data['experience'],
            "education": form_data['education'],
            "certifications": form_data['certifications'],
            "projects": form_data['projects'],
            "awards": form_data['awards'],
            "languages": form_data['languages'],
            "portfolio_url": form_data['portfolio_url'],
            "availability": form_data['availability'],
        }

        # Convert the dictionary to a formatted string for ChatGPT
        resume_text = "\n".join(f"{key}: {value}" for key, value in resume_data.items() if value)

        # Generate suggestions using ChatGPT
        suggestions = get_chatgpt_suggestions(resume_text, job_position, job_description)
        parsed_suggestions = format_suggestions_as_bullets(suggestions)

        # Render the response
        return render(request, 'resume/thank_you.html', {
            'suggestions': parsed_suggestions,
            'job_position': job_position,
            'job_description': job_description,
        })

    except Exception as e:
        # Handle errors and return to the form
        error_message = f"Error processing form data: {str(e)}"
        return render(request, 'resume/resume_form.html', {'form': ResumeForm(initial=form_data), 'error_message': error_message})



def handle_pdf_submission(request, uploaded_file, job_position, job_description, form):
    """Process a submitted PDF resume."""
    try:
        # Extract text from the uploaded PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = " ".join(page.extract_text() or "" for page in pdf_reader.pages)

        # Validate extracted text
        if not extracted_text.strip():
            raise ValueError("The uploaded PDF does not contain readable text.")

        # Generate suggestions
        suggestions = get_chatgpt_suggestions(extracted_text, job_position, job_description)
        parsed_suggestions = format_suggestions_as_bullets(suggestions)

        return render(request, 'resume/thank_you.html', {
            'suggestions': parsed_suggestions,
            'job_position': job_position,
            'job_description': job_description,
        })

    except Exception as e:
        error_message = f"Error processing the PDF: {str(e)}"
        return render(request, 'resume/resume_form.html', {'form': form, 'error_message': error_message})



def get_chatgpt_suggestions(resume_text, job_position, job_description):
    """Generate suggestions from ChatGPT API."""
    messages = [
        {"role": "system", "content": "You are a professional career advisor."},
        {
            "role": "user",
            "content": (
                f"Here is a resume for analysis:\n\n"
                f"Job Position: {job_position}\n"
                f"Job Description: {job_description}\n\n"
                f"Resume Text:\n{resume_text}\n\n"
                f"Provide actionable suggestions for improvement tailored to the job position and description."
            )
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip()


def format_suggestions_as_bullets(suggestions):
    """Convert suggestions into structured HTML bullets."""
    if not suggestions or not isinstance(suggestions, str):
        return "<p>No suggestions provided.</p>"

    pattern = r"(\d+\.\s\*\*.*?\*\*:)"
    sections = re.split(pattern, suggestions)

    if len(sections) <= 1:
        return f"<p>{suggestions.strip()}</p>"

    formatted_html = ""
    for i in range(1, len(sections), 2):
        try:
            section_title = sections[i].strip("*: ")
            section_content = sections[i + 1].strip() if i + 1 < len(sections) else ""

            bullets = re.split(r"-\s", section_content)
            bullet_list = "".join(f"<li>{bullet.strip()}</li>" for bullet in bullets if bullet.strip())

            formatted_html += f"<h3>{section_title}</h3><ul>{bullet_list}</ul>"
        except Exception:
            continue

    return formatted_html or f"<p>{suggestions.strip()}</p>"