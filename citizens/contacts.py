# import atom.data
# import gdata.data
# import gdata.contacts.client
# import gdata.contacts.data

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
