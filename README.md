# django-openehr
<a href="https://badge.fury.io/py/django_openehr"><img src="https://badge.fury.io/py/django_openehr.svg" alt="PyPI version" height="18"></a>

Experimental | Not officially supported by OHCUK

![supported_by_apperta_lores.png](https://github.com/AppertaFoundation/apperta-image-assets/blob/master/supported_by_apperta_lores.png)

Experimental [Django](https://www.djangoproject.com/) models based on [openEHR](http://www.openehr.org/) archetypes and distributed as a Python Package on [PyPi](https://pypi.python.org/pypi), with an accompanying [demo Django application](https://github.com/openhealthcare/django-openehr-demo-app), showing the implementation of a single openEHR Template as a Django Form composed of data fields from the correct underlying openEHR Archetypes, as defined in the Template on the [UK Apperta Clinical Knowledge Manager](http://ckm.apperta.org/ckm/)

The intentions of the experiment are:

* to learn more about the internal structure of openEHR by creating a 'toy' set of models using these archetypes.
* to explore the feasibility of 'misusing' the freely published openEHR archetypes as a 'source of clinical modelling truth' when data-modelling a web application in Django (or any other web framework), as opposed to using openEHR as a technical layer in the intended manner.
* to understand the minimum range of archetypes required to build a proof of concept EHR app.

## Templates included (in the demo app)
| Django Form | openEHR Template |
|------|----------|
| IDCR template | IDCR Transfer of Care summary (minimal).v0 |

## Archetypes included
| Django Model | openEHR Archetype |
| -------------| ----------------- |
| models/address_details.py                 | openEHR-EHR-CLUSTER.address.v1 |
| models/adverse_reaction.py                | openEHR-EHR-EVALUATION.adverse_reaction_uk.v1 |
| models/clinical_synopsis.py               | openEHR-EHR-EVALUATION.clinical_synopsis.v1
| models/demographic_personal.py            | openEHR-EHR-CLUSTER.individual_personal_uk.v1 |
| models/demographic_professional.py        | openEHR-EHR-CLUSTER.individual_professional_uk.v1 |
| models/inpatient_admission.py             | openEHR-EHR-ADMIN_ENTRY.inpatient_admission_uk.v1 |
| models/person_name.py                     | openEHR-EHR-CLUSTER.person_name.v1 |
| models/problem_diagnosis.py               | openEHR-EHR-EVALUATION.problem_diagnosis.v1 |
| models/reason_for_encounter.py            | openEHR-EHR-EVALUATION.reason_for_encounter.v1 |
| models/relevant_contact.py                | openEHR-EHR-ADMIN_ENTRY.relevant_contact_rcp.v0 |
| models/symptom_sign/py                    | openEHR-EHR-CLUSTER.symptom_sign.v1 |
| models/telecom_details.py                 | openEHR-EHR-CLUSTER.telecom_uk.v1 |
| models/therapeutic_direction.py           | openEHR-EHR-CLUSTER.therapeutic_direction.v1 |

_all data from each CKM archetype has been retained as comments in the respective Django model file_

## Reference Model artefacts converted
| Django Model | openEHR Reference Model artefact |
|--------------|----------------------------------|
| DV_IDENTIFIER            | models/identifier.py |

## Method/Approach
* For this experiment/proof of concept, we have attempted to emulate in Django the two-level clinical modelling paradigm of openEHR (archetypes and templates), a paradigm which is also shared by other clinical modelling technologies such as FHIR (resources and profiles)

* **openEHR Archetypes have been recreated as Django models**. In Django (as in many web frameworks), models are Classes, instances of which can be assigned data attributes, and these data attributes for a given instance map to a given row in a database table. Django contains an object-relational mapper (ORM) which handles this abstraction automatically, and numerous convenience methods which simplify access to related objects through foreign key or join-table relationships.

* **openEHR Templates have been rendered as Django Forms**, which form the second layer of our modelling tooling, allowing constraint and specialisation of our Django model (= our archetype)

* Practically, in the absence of an automatable mechanism for creating Django forms from openEHR archetypes, we simply copied and pasted the text from the 'Data' tab of the UK openEHR Clinical Knowledge Manager for each archetype into a text editor. We then reformatted the archetype into a Django model (or model_s_), mapping field types, validations, maxima and minima into their Django idiomatic equivalents. We kept as much contextual information as possible in `#comment` form.

* Models were quite large and therefore for better readbility and also in an effort to optimise the re-use potential of the models, they have been separated out from `models.py` into individual files under the `/models/` directory, importable as a module because of the `__init__.py` containing an `__all__` list.

* openEHR implementations tend to store data in documents rather than in relational tables, hence it's possible that in the conversion of Archetypes to Django models we will encounter modelled entities which are impractical to model in a relational fashion, however so far we've been able to model most things that made sense to model.

### Upstream Issues with Archetypes
* Where issues have arisen regarding upstream archetypes or templates, I've created a GitHub issue in this repo as placeholder/record, and then I've passed the issue back to the UK CKM via it's own internal Change Request method.

# Installation

## Installing the package
* This package has been designed to be a reusable group of clinical models drawn from a canonical source (UK CKM), which can be used in other applications.
* To use it in your own Django project or app, you need to install the package via the command line/terminal:
```
pip install django_openehr
```
or

add `django_openehr` to your requirements.txt file, and then run 
```
pip install -r requirements.txt
```

## Adding these models to an existing Django application
* you may need to adapt these instructions to the specifics of your Django application, since we haven't tested every use-case. If you have problems please feel free to raise an [Issue](https://github.com/openhealthcare/django-openehr/issues) about it, we may be able to help.
* add `django_openehr` to the INSTALLED_APPS list in settings.py
* make the database migrations
```
python manage.py makemigrations
```
* apply the migrations
```
python manage.py migrate
```
* register the models with the Django Admin if you want to be able to manipulate these models in the Admin view. You can see an example of how to do this [here](https://github.com/openhealthcare/django-openehr-demo-app/blob/master/django_openehr_demo/admin.py)
* start the development server
```
python manage.py runserver
```

## Interacting with the models using the Django shell
* install as per above instructions, including migration steps
* invoke the Django shell
```
python manage.py shell
```
* import the models
```
from django_openehr import models
```
* you can then interact with the models and the data in your database using the standard DJango ORM API, eg:
```
>>> models.PersonName.objects.first().given_name
'Marcus'
```

------

## Contributing to this project
* We welcome contributions from the community, and are happy to consider pull requests for bugfixes, optimisations and new archetypes.
* For new Archetype contributions, please follow the one-model-per-file pattern used throughout this package. We accept that this is not traditionally a Django idiom (Rails is all over it though :-) ), but it helps with organising the models, which can become very large and would be unwieldy in a single file.
* Please also consider updating the forms and details views in the [companion Demo Application](https://github.com/openhealthcare/django-openehr-demo-app) with your new models
* We welcome discussion regarding this package in the [Issues](https://github.com/openhealthcare/django-openehr/issues)
