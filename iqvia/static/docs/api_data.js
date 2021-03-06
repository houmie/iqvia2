define({ "api": [
  {
    "type": "post",
    "url": "/contacts",
    "title": "Adds a contact",
    "description": "<p>Adds a new contact</p>",
    "name": "add_contact",
    "group": "Contacts",
    "parameter": {
      "fields": {
        "Body": [
          {
            "group": "Body",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "surname",
            "description": "<p>The surname of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "6-32",
            "optional": false,
            "field": "username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "Array",
            "optional": false,
            "field": "emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "5-128",
            "optional": false,
            "field": "emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "UUID",
            "optional": false,
            "field": "id",
            "description": "<p>The ID of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "surname",
            "description": "<p>The surname of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "6-32",
            "optional": false,
            "field": "username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Datetime",
            "optional": false,
            "field": "inserted",
            "description": "<p>The insertion time of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "5-128",
            "optional": false,
            "field": "emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "type": "delete",
    "url": "/contacts/<contact_id>",
    "title": "Deletes a contact",
    "description": "<p>Deletes a contact</p>",
    "name": "delete_contact",
    "group": "Contacts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "UUID",
            "optional": false,
            "field": "contact_id",
            "description": "<p>The ID of the contact.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "type": "delete",
    "url": "/contacts/<contact_id>",
    "title": "Deletes contacts",
    "description": "<p>Deletes contacts</p>",
    "name": "delete_contacts",
    "group": "Contacts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "inserted_seconds",
            "description": "<p>Deletes all the contacts inserted before inserted_seconds ago.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "type": "get",
    "url": "/contacts/<username>",
    "title": "Gets a contact",
    "description": "<p>Gets a contact with filters</p>",
    "name": "get_contact",
    "group": "Contacts",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "size": "6-32",
            "optional": true,
            "field": "username",
            "description": "<p>The Username of the contact.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "size": "5-128",
            "optional": true,
            "field": "email",
            "description": "<p>The email address of the contact.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "UUID",
            "optional": false,
            "field": "id",
            "description": "<p>The ID of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "surname",
            "description": "<p>The surname of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "6-32",
            "optional": false,
            "field": "username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Datetime",
            "optional": false,
            "field": "inserted",
            "description": "<p>The insertion time of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "5-128",
            "optional": false,
            "field": "emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "type": "get",
    "url": "/contacts",
    "title": "Gets all the contacts",
    "description": "<p>Gets all the contacts</p>",
    "name": "get_contacts",
    "group": "Contacts",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "contacts",
            "description": "<p>The contacts retrieved.</p>"
          },
          {
            "group": "Success 200",
            "type": "UUID",
            "optional": false,
            "field": "contacts.id",
            "description": "<p>The ID of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "contacts.first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "contacts.surname",
            "description": "<p>The surname of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "6-32",
            "optional": false,
            "field": "contacts.username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Datetime",
            "optional": false,
            "field": "contacts.inserted",
            "description": "<p>The insertion time of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "contacts.emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "5-128",
            "optional": false,
            "field": "contacts.emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "type": "patch",
    "url": "/contacts/<contact_id>",
    "title": "Updates an item",
    "description": "<p>Updates a contact</p>",
    "name": "update_contact",
    "group": "Contacts",
    "parameter": {
      "fields": {
        "Body": [
          {
            "group": "Body",
            "type": "String",
            "size": "1-50",
            "optional": true,
            "field": "first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "1-50",
            "optional": true,
            "field": "surname",
            "description": "<p>The last name of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "1-32",
            "optional": true,
            "field": "username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "Array",
            "optional": true,
            "field": "emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Body",
            "type": "String",
            "size": "5-128",
            "optional": true,
            "field": "emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "UUID",
            "optional": false,
            "field": "id",
            "description": "<p>The ID of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "first_name",
            "description": "<p>The first name of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "1-50",
            "optional": false,
            "field": "surname",
            "description": "<p>The surname of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "6-32",
            "optional": false,
            "field": "username",
            "description": "<p>The username of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Datetime",
            "optional": false,
            "field": "inserted",
            "description": "<p>The insertion time of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "emails",
            "description": "<p>The emails of the contact.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "size": "5-128",
            "optional": false,
            "field": "emails.email",
            "description": "<p>The email address.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "iqvia/contacts/views.py",
    "groupTitle": "Contacts"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "iqvia/static/docs/main.js",
    "group": "_home_clement_daubrenet_iqvia2_iqvia_static_docs_main_js",
    "groupTitle": "_home_clement_daubrenet_iqvia2_iqvia_static_docs_main_js",
    "name": ""
  }
] });
