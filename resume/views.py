# import openai
# from django.shortcuts import render
# from .forms import ResumeForm
# import re

# # Set your OpenAI API key

# def resume_form(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST)

#         if form.is_valid():
#             # Extract data from the form
#             resume_data = {
#                 "full_name": form.cleaned_data['full_name'],
#                 "email": form.cleaned_data['email'],
#                 "phone_number": form.cleaned_data['phone_number'],
#                 "linkedin": form.cleaned_data['linkedin'],
#                 "professional_summary": form.cleaned_data['professional_summary'],
#                 "skills": form.cleaned_data['skills'],
#                 "experience": form.cleaned_data['experience'],
#                 "education": form.cleaned_data['education'],
#                 "certifications": form.cleaned_data['certifications'],
#                 "projects": form.cleaned_data['projects'],
#                 "awards": form.cleaned_data['awards'],
#                 "languages": form.cleaned_data['languages'],
#                 "portfolio_url": form.cleaned_data['portfolio_url'],
#                 "availability": form.cleaned_data['availability']
#             }

#             # Format the input as a conversation
#             messages = [
#                 {"role": "system", "content": "You are a professional career advisor."},
#                 {"role": "user", "content": f"Provide suggestions to improve the following resume:\n\n{resume_data}"}
#             ]

#             try:
#                 # Call the OpenAI ChatCompletion API
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=messages,
#                     max_tokens=1000,
#                     temperature=0.7
#                 )

#                 # Extract the assistant's reply
#                 suggestions = response['choices'][0]['message']['content'].strip()
#                 # Debugging output
#                 print("Raw Suggestions from ChatGPT:", suggestions)
                

#                 # Parse the suggestions into HTML bullets
#                 parsed_suggestions = format_suggestions_as_bullets(suggestions) # Debugging in the console
#                 # Debugging parsed content
#                 print("Parsed Suggestions:", parsed_suggestions)
                

#                 # Render the response in the thank_you page
#                 return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})
#             except Exception as e:
#                 return render(request, 'resume/thank_you.html', {'error': str(e)})

#     else:
#         form = ResumeForm()

#     return render(request, 'resume/resume_form.html', {'form': form})


# def format_suggestions_as_bullets(suggestions):
#     """
#     Convert the ChatGPT suggestions into structured HTML bullets grouped under categories.
#     Handles long inputs and edge cases gracefully.
#     """
#     import re

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

def resume_form(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            # Check if a PDF file was uploaded
            if request.FILES.get("resume_pdf"):
                uploaded_file = request.FILES["resume_pdf"]

                # Extract text from the uploaded PDF
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    extracted_text = ""
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text()

                    # Debugging output
                    print("Extracted Text from PDF:", extracted_text[:500])  # Display first 500 characters

                    # Format the input as a conversation
                    messages = [
                        {"role": "system", "content": "You are a professional career advisor."},
                        {"role": "user", "content": f"Provide suggestions to improve the following resume:\n\n{extracted_text}"}
                    ]

                    # Call the OpenAI ChatCompletion API
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=1000,
                        temperature=0.7
                    )

                    # Extract the assistant's reply
                    suggestions = response['choices'][0]['message']['content'].strip()
                    # Parse the suggestions into HTML bullets
                    parsed_suggestions = format_suggestions_as_bullets(suggestions)

                    # Render the response in the thank_you page
                    return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})

                except Exception as e:
                    error_message = "There was an error processing your PDF file. Please try again."
                    return render(request, 'resume/resume_form.html', {'form': form, 'error_message': error_message})
            else:
                # If the form data is submitted instead of a PDF
                resume_data = {
                    "full_name": form.cleaned_data['full_name'],
                    "email": form.cleaned_data['email'],
                    "phone_number": form.cleaned_data['phone_number'],
                    "linkedin": form.cleaned_data['linkedin'],
                    "professional_summary": form.cleaned_data['professional_summary'],
                    "skills": form.cleaned_data['skills'],
                    "experience": form.cleaned_data['experience'],
                    "education": form.cleaned_data['education'],
                    "certifications": form.cleaned_data['certifications'],
                    "projects": form.cleaned_data['projects'],
                    "awards": form.cleaned_data['awards'],
                    "languages": form.cleaned_data['languages'],
                    "portfolio_url": form.cleaned_data['portfolio_url'],
                    "availability": form.cleaned_data['availability']
                }

                # Format the input as a conversation
                messages = [
                    {"role": "system", "content": "You are a professional career advisor."},
                    {"role": "user", "content": f"Provide suggestions to improve the following resume:\n\n{resume_data}"}
                ]

                try:
                    # Call the OpenAI ChatCompletion API
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=1000,
                        temperature=0.7
                    )

                    # Extract the assistant's reply
                    suggestions = response['choices'][0]['message']['content'].strip()
                    # Parse the suggestions into HTML bullets
                    parsed_suggestions = format_suggestions_as_bullets(suggestions)

                    # Render the response in the thank_you page
                    return render(request, 'resume/thank_you.html', {'suggestions': parsed_suggestions})
                except Exception as e:
                    return render(request, 'resume/thank_you.html', {'error': str(e)})

    else:
        form = ResumeForm()

    return render(request, 'resume/resume_form.html', {'form': form})


def format_suggestions_as_bullets(suggestions):
    """
    Convert the ChatGPT suggestions into structured HTML bullets grouped under categories.
    Handles long inputs and edge cases gracefully.
    """
    # Sanity check for input
    if not suggestions or not isinstance(suggestions, str):
        return "<p>No suggestions provided.</p>"

    # Define a regex pattern to match section headers
    pattern = r"(\d+\.\s\*\*.*?\*\*:)"  # Example: "1. **Title**:"

    # Split suggestions into sections using regex
    sections = re.split(pattern, suggestions)

    if len(sections) <= 1:
        # If no sections detected, return suggestions as a paragraph
        return f"<p>{suggestions.strip()}</p>"

    formatted_html = ""
    for i in range(1, len(sections), 2):
        try:
            # Extract section title and content
            section_title = sections[i].strip("*: ")
            section_content = sections[i + 1].strip() if i + 1 < len(sections) else ""

            # Limit processing to prevent potential freezes
            if len(section_content) > 5000:  # Prevent excessively long content
                section_content = section_content[:5000] + "..."

            # Split content into bullets (lines starting with "-")
            bullets = re.split(r"-\s", section_content)
            bullet_list = "".join([f"<li>{bullet.strip()}</li>" for bullet in bullets if bullet.strip()])

            # Build HTML structure
            formatted_html += f"<h3>{section_title}</h3><ul>{bullet_list}</ul>"
        except Exception as e:
            # Log and skip problematic sections
            print(f"Error processing section: {e}")
            continue

    # Return formatted HTML or fallback to plain paragraph
    return formatted_html or f"<p>{suggestions.strip()}</p>"
