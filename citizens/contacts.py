# import atom.data
# import gdata.data
# import gdata.contacts.client
# import gdata.contacts.data

import googleapiclient.discovery
import google_auth_oauthlib.flow
import google.oauth2.credentials
gd_client = gdata.contacts.client.ContactsClient(source="<APP NAME>")

def create_contact(gd_client, data):
    new_contact = gdata.contacts.data.ContactEntry()
    new_contact.name = gdata.data.Name(
        given_name=gdata.data.GivenName(text=data['first_name']),
        family_name=gdata.data.FamilyName(text=data['surname']),
        full_name=gdata.data.FullName(
            text=f"{data['first_name']} {data['last_name']}")
    )

    new_contact.content = atom.data.Content(text='Notes')

    # Email details
    new_contact.email.append(
        gdata.data.Email(
            address=data['email'], primary='true',
            rel=gdata.data.WORK_REL, display_name=data['first_name']))

    # Phone Number
    new_contact.phone_number.append(
        gdata.data.PhoneNumber(text=data['phone_number'],
        rel=gdata.data.WORK_REL, primary='true'))

    # Send the contact data to the server
    contact_entry = gd_client.CreateContact(new_contact)
    print('Contact created successfully')
    return contact_entry


def update_contact(gd_client, contact_url, data):
    # Retrieve th contact
    contact_entry = gd_client.GetContact(contact_url)
    contact_entry.name.full_name.text = f"{data['first_name']} {data['last_name']}"
    contact_entry.name.given_name.text = f"{data['first_name']}"
    contact_entry.name.family_name = f"{data['surname']}"

    # Updatet the contact
    try:
        updated_contact = gd_client.Update(contact_entry)
        print("Successfully Updated the Contact")
        return updated_contact
    except gdata.client.RequestError as e:
        if e.status == 412:
            # Handle the mismatch
            pass
    return None

# send a POST request to https://www.google.com/m8/feeds/groups/{userEmail}/full


def create_group(gd_client, data):
    new_group = gdata.contacts.data.GroupEntry(
        title=atom.data.Title(text=data['name']))
    new_group.extended_properties.append(
        gdata.data.ExtendedProperty(name='', value='')
    )

    created_group = gd_client.CreateGroup(new_group)
    # Call to method add contacts to group
    print("Group Successfully created")
    return created_group

# send a PUT request to https://www.google.com/m8/feeds/groups/{userEmail}/full/{groupId}
# def update_contact_group(gd_client, data, groupId):
#     group = gd_client.GetGroup(groupUrl)

#     try:
#         gd_client.Update(group)
#     except expression as identifier:
#         pass

# send a DELETE request to https://www.google.com/m8/feeds/groups/{userEmail}/full/{groupId}


def delete_contact_group(gd_client, contact_group_url):
    # Retrieve the group
    group = gd_client.GetGroup(contact_group_url)
    try:
        gd_client.Delete(group)
    except gdata.client.RequestError as e:
        # Handle Etag mismatch
        if e.status == 412:
            pass

# Agg Group membership


def add_group_membership(gd_client, contact_url, group_atom_id):
    contact = gd_client.GetContact(contact_ur)
    contact.group_membership_info.append(
        gdata.contacts.data.GroupMembershipInfo(href=group_atom_id))

    try:
        updated_contact = gd_client.Update(contact)
        return updated_contact
    except gdata.client.RequestError as e:
        if e.status == 412:
            pass
    return None

# Send a delete request to https://www.google.com/m8/feeds/groups/{userEmail}/full/{contactID}


def delete_contact(gd_client, data, contact_url):
    contact = gd_client.GetContact(contact_url)

    try:
        gd_client.Delete(contact)
    except gdata.client.RequestError as e:
        if e.status == 412:
            # Hand the Etaf problem
            # pass

            # ======================

            # Batch a processing
            # send POT REQEUST TO https://www.google.com/m8/feeds/groups/{userEmail}/full/batch


CLIENTS_SECRETS_FILE = staticfiles_storage.path("client_secret.json")
SCOPES = ['https://www.google.com/m8/feeds/']

API_SERVICE_NAME = 'contacts'
API_VERSION = 'v3'


def test_contacts_api(request):
    # Client and scopes
    if 'credentials' not in request.session:
        return redirect('authorize')

    credentials = goole.oauth2.credentials.Credentials(
        **request.session['credentials']
    )

    feeds = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )

    contacts = feeds

    request.session['credentials'] = credentials_to_dict(credentials)
    return HttpResponse(contacts)


def authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE,
        SCOPES
    )

    flow.redirect_uri = 'http://127.0.0.1:8000/contacts/'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        login_hint='davidnganganjeri079@gmail.com',
        include_granted_scopes='true'
    )

    request.session['state'] = state

    print(authorization_url)
    return redirect(authorization_url)


def oauth2callback(request):
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE, scopes=SCOPES, state=state
    )

    flow.redirect_uri = 'http://127.0.0.1:8000/contacts/'  # Callback url similar to
    authorization_response = 'http://127.0.0.1:8000/oauth2callback/'  # Request url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('contacts')


def revoke(request):
    pass


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def clear_credentials(request):
    pass

 # Contacts
    path('googled764035286992e26.html', about, name='about', ),
    path('contacts/', test_contacts_api, name='contacts'),
    path('authorize/', authorize, name='authorize'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
