# django-openehr
alpha software | unsupported

experimental django models based on openEHR archetypes

The intention is to explore the minimum range of archetypes required to build a minimum viable EHR app.

## Archetypes converted so far
| archetype | model |
| --------- | ----- |
| openEHR-EHR-CLUSTER.individual_personal_uk.v1 | models/demographics.py |
| openEHR-EHR-CLUSTER.person_name.v1            | flattened into models/demographics.py |
| openEHR-EHR-CLUSTER.symptom_sign.v1           | models/symptom_sign/py |
| openEHR-EHR-CLUSTER.address.v1                | models/address_details.py |
| openEHR-EHR-CLUSTER.telecom_uk.v1             | models/telecom_details.py |
| openEHR-EHR-CLUSTER.therapeutic_direction.v1  | models/therapeutic_direction.py |

## Method/Approach
*For this proof of concept, we have simply copied and pasted the text from the 'Data' tab of the CKM for each archetype into a text editor, and then reformatted, keeping as much information as possible in `# comment` form.
*Django objects have been created for eact data item, keeping as much as possible to idiomatic Django style.
*Models were quite large and therefore for better readbility and also in an effort to optimise the re-use potential of the models, they have been separated out from `models.py` into individual files under the `/models/`` directory.

## Notes
*openEHR implementations tend to store data in documents rather than in relational tables, hence it's possible that in the conversion of Archetypes to Django models we will encounter modelled entities which are impractical to model in a relational fashion, however so far we've been able to model most things that made sense to model.

## Issues
*where Issues have arisen regarding upstream archetypes or an inability to accurately convert the archetype into a Django model, I've created a GitHub issue for it. In time we will pass upstream Issues back to the UK CKM in whatever way is preferred.

## Django Application
The models have been built into a demo/PoC Django Application, although there is very little functionality at present.

To try this application:

*`git clone` this repo into a suitable folder
*`cd` into the cloned directory
*`python manage.py migrate`
*`python manage.py createsuperuser` (enter some super user details)
*`python manage.py runserver`
*navigate to localhost:8000/admin/ to log in and interact with the models using the Django admin interface.


*You can also use the Django shell (`python manage.py shell` to manipulate the new classes.)
