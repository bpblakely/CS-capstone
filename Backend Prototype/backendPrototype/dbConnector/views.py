from django.shortcuts import render
from django.http import HttpResponse
from backendPrototype.settings import DATABASES
from .models import researchint, publications, grants
import MySQLdb
import pandas as pd
from django.template import loader
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
from backendPrototype.process_pdf import pdf_processor
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os

default_path = os.getcwd()
print(default_path)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    template = loader.get_template(default_path+r'/dbConnector/templates/home.html')
    context = { 'user' : request.user, 'faculty': request.user.groups.filter(name="faculty").exists()}

    return HttpResponse(template.render(context))

def resultspage(request):
    if request.method == 'GET':  # If the form is submitted
        dropdown_query = request.GET.get('dropdown', None).lower()
        search_query = request.GET.get('search', None).lower()

        if dropdown_query == 'interest':
            data = researchint.objects.filter(interest__contains=search_query)
        elif dropdown_query == 'name':
            data = researchint.objects.filter(name__contains=search_query)
        else:
            data = researchint.objects.filter(department__icontains=search_query)

        unique_interests = {}
        nameList = []
        emailList = {}
        nameDepart = {}
        grantz = {}
        pubz = {}
        for row in data.values('name'):
            nameList.append(row.get('name'))

        for row in researchint.objects.filter(name__in=nameList):
            row.name = row.name.title()
            row.interest = row.interest.title()
            row.department = row.department.title()

            # Names will appear multiple times, only append each unique research interest
            if row.name in unique_interests.keys():
                unique_interests[row.name].append(row.interest)
            else: # Do stuff once
                unique_interests[row.name] = [row.interest]
                # Match email for publications and grants
                pubz[row.name] = [x['publication'].title() for x in list(publications.objects.filter(email__exact=row.email).values('publication'))]
                grantz[row.name] = [x['grant'].upper() for x in list(grants.objects.filter(email__exact=row.email).values('grant'))]
                nameDepart[row.name] = row.department
                emailList[row.name] = row.email


        context = {'search_query' : search_query, 'research_interests' : unique_interests.items(), 'depart' : nameDepart, 'email': emailList,
                   'selection' : dropdown_query.title(), 'user' : request.user, 'faculty': request.user.groups.filter(name="faculty").exists(),
                   'grantz' : grantz, 'pubz' : pubz}
    template = loader.get_template(default_path+r'/dbConnector/templates/results.html')
    return HttpResponse(template.render(context))

def updatepage(request):
    template = loader.get_template(default_path+r'/dbConnector/templates/uploadData.html')
    context= {'user' : request.user, 'faculty': request.user.groups.filter(name="faculty").exists()}

    # Make sure the user is a faculty member and is in the database
    if context['faculty'] and len(researchint.objects.filter(email=request.user.email)) > 0:
        # If they are in the database, then we fill the text fields with the prior data in the database
        query = researchint.objects.filter(email=request.user.email)
        info = query.first()
        context['name'] = request.user.get_full_name
        context['dept'] = info.department
        # interests
        interests = []
        for row in query:
            interests.append(row.interest.strip())
        context['interests'] = ";\n".join(interests).lower()

        context['email'] = request.user.email

        # publications
        query = publications.objects.filter(email=request.user.email)
        pubs = []
        for row in query:
            pubs.append(row.publication.strip())
        context['pubs'] = ";\n".join(pubs).lower()

        # grants
        query = grants.objects.filter(email=request.user.email)
        grants_list = []
        for row in query:
            grants_list.append(row.grant.strip())
        context['grantz'] = ";\n".join(grants_list).lower()
        
    return HttpResponse(template.render(context))

# Insert into research interests database
def insert_into_database(df, force=True):
    # force = True: Deletes all previous data in the table attributed to the person, force= False: just append new data
    def d(x):
        return researchint(name=x[0].lower(), department=x[1].lower(), email=x[2].lower(), interest=x[3].lower()).save()
    try:
        if force:
            # Delete values based on the name, department, and email from table
            for i, row in df[['name', 'department', 'email']].drop_duplicates().iterrows():
                researchint.objects.filter(name=row[0]).filter(department=row[1]).filter(email=row[2]).delete()
                # print(f'Deletion of {name} successful')
        df.apply(d, axis=1)
        return True
    except:
        print("Duplicate Entry Detected. To write over the existing data call the function with 'force = True'")
        return False

# Insert into publication database
def insert_into_database_pubs(df, force=True):
    # force = True: Deletes all previous data in the table attributed to the person, force= False: just append new data
    def d(x):
        return publications(name=x[0].lower(), department=x[1].lower(), email=x[2].lower(), publication=x[3].lower()).save()
    try:
        if force:
            # Delete values based on the name, department, and email from table
            for i, row in df[['name', 'department', 'email']].drop_duplicates().iterrows():
                publications.objects.filter(name=row[0]).filter(department=row[1]).filter(email=row[2]).delete()
                # print(f'Deletion of {name} successful')
        df.apply(d, axis=1)
        return True
    except:
        print("Duplicate Entry Detected. To write over the existing data call the function with 'force = True'")
        return False

# Insert into grant database
def insert_into_database_grants(df, force=True):
    # force = True: Deletes all previous data in the table attributed to the person, force= False: just append new data
    def d(x):
        return grants(name=x[0].lower(), department=x[1].lower(), email=x[2].lower(), grant=x[3].lower()).save()
    try:
        if force:
            # Delete values based on the name, department, and email from table
            for i, row in df[['name', 'department', 'email']].drop_duplicates().iterrows():
                grants.objects.filter(name=row[0]).filter(department=row[1]).filter(email=row[2]).delete()
                # print(f'Deletion of {name} successful')
        df.apply(d, axis=1)
        return True
    except:
        print("Duplicate Entry Detected. To write over the existing data call the function with 'force = True'")
        return False


@csrf_exempt
def uploadpdf(request):
    # button
    template = loader.get_template(default_path + r'/dbConnector/templates/uploadData.html')

    # If someone tries to upload before attaching a file, throw an error and reload the page
    if not request.FILES.get('filename'):
        context = {}
        context['message'] = 'Upload a CV PDF file first!'
        context['user'] = request.user
        context['faculty'] = request.user.groups.filter(name="faculty").exists()
        return HttpResponse(template.render(context))

    # File is uploaded correctly
    if request.method == "POST" and request.FILES['filename']:
        file = request.FILES['filename']
        fs = FileSystemStorage()
        file_location = default_path + r'/CVs/' + str(request.FILES['filename'])

        # If the file isn't a PDF, throw an error
        if not str(file).endswith('.pdf'):
            context = {}
            context['message'] = 'File must be a PDF!'
            context['user'] = request.user
            context['faculty'] = request.user.groups.filter(name="faculty").exists()
            return HttpResponse(template.render(context))

        # if file already exists, delete it
        if os.path.isfile(file_location):
            os.remove(file_location)

        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # Do PDF processing on the CV file
        if os.path.isfile(file_location):
            df, process_status = pdf_processor(file_location) # process_status = False when the file couldn't be processed
            if process_status:
                context = insert_upload_text(df)
            else:
                context = {'message':'Unable to process CV, make sure it follows the rubric'}
            context['user'] = request.user
            context['faculty'] = request.user.groups.filter(name="faculty").exists()
            return HttpResponse(template.render(context))
    return HttpResponse(template.render())

# Format everything in context nicely
def insert_upload_text(df):
    context = {}
    variables = ['name', 'email', 'dept', 'interests', 'pubs', 'grants']
    context['name'] = df['name'].iloc[0].title()
    context['dept'] = df['department'].iloc[0].title()
    context['interests'] = ";\n".join(df['interest'].tolist())
    context['email'] = df['email'].iloc[0]

    # place holders
    context['pubs'] = ''
    context['grants'] = ''
    return context

def upload_submit_button(request):
    template = loader.get_template(default_path + r'/dbConnector/templates/uploadData.html')
    context = {}
    if request.method == "GET":
        variables = ['interests','pubs','grants']
        name = request.GET.get('name', '').lower()
        email = request.GET.get('email', '')
        dept = request.GET.get('dept', '')
        interests = request.GET.get('interests', '')
        pubs = request.GET.get('pubs', '')
        grantz = request.GET.get('grantz','')

        temp_list = []
        for data in [interests,pubs,grantz]:
            if len(interests) > 0:
                data = data.replace("\n",'').replace("\r",'')
                data = list(filter(bool, data.split(';')))
            else:
                data = []
            temp_list.append(data)

        ints_success = False
        for j,data in enumerate(temp_list):
            li = []
            for i in range(len(data)):
                li.append([name, dept, email, data[i]])

            df = pd.DataFrame([])
            df = df.append(li)
            df.rename(columns={0: 'name', 1: 'department', 2: 'email', 3: 'dummy_var'}, inplace=True)

            if j == 0:
                success = insert_into_database(df)
            elif j == 1:
                success = insert_into_database_pubs(df)
            else:
                success = insert_into_database_grants(df)
            # Technically works despite being terrible
            if success:
                context['message'] = 'Upload Successful!'
                if j == 0:
                    ints_success = True
            else:
                context['message'] = 'Upload Failed!'
        if ints_success:
            if not success:
                context['message'] = 'Research Interests Uploaded Successfully!'
    # Do this when we add the other tables
        #li = []
        # add logic for reading publication and grants, need to do it after we create the pubs and grants database
        # for var in variables:
        #     value = request.GET.get(var,'')
        #     if len(value) == 0:
        #         li.append('')
        #     else:
        #         if var == 'interests':
        #             li.append(value.split(';'))
        #         else: continue

    context['user'] = request.user
    context['faculty'] = request.user.groups.filter(name="faculty").exists()
    return HttpResponse(template.render(context))

def loginButton(request):
    template = loader.get_template(default_path + r'/templates/registration/login.html')
    return HttpResponse(template.render())

# populates the database for the first time with CV data read in batches
def populate_database():
    df = pd.read_csv(default_path + r'/CVs/cv_data.csv')
    insert_into_database(df)
# populate_database()

