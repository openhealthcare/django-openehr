s# django-openehr
<a href="https://badge.fury.io/py/django_openehr"><img src="https://badge.fury.io/py/django_openehr.svg" alt="PyPI version" height="18"></a>

alpha software | unsupported

Experimental django models based on openEHR archetypes and distributed as a PyPi package, with an accompanying demo Django application, showing the implementation of a single openEHR Template as a Django Form composed of data fields from the correct underliying openEHR Archetypes, as defined in the Template on the [UK Apperta Clinical Knowledge Manager](http://ckm.apperta.org/ckm/)

The intentions of the experiment are:

* to learn more about the internal structure of openEHR by creating a 'toy' using these archetypes.
* to explore the feasibility of 'misusing' openEHR archetypes as a 'source of clinical modelling truth' when data-modelling a web application in Django (or any other web framework)
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
| models/body_site.py                       | not from a specific archetype |
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
* For this experiment/proof of concept, we have attempted to emulate in Django the 2-level clinical modelling paradigm of openEHR.

* openEHR Archetypes have been recreated as Django models. In Django (as in many web frameworks), models are Python classes, instances of which can be assigned data attributes, and these data attributes map to rows in a database table. Django contains an object-relational mapper (ORM) which handles this abstraction automatically.

* openEHR Templates have been rendered as Django forms, which form the second layer of our modelling tooling, allowing constraint and specialisation of our Django model (= our archetype)

* Practically, in the absence of an automatable mechanism for creating Django forms from openEHR archetypes, we simply copied and pasted the text from the 'Data' tab of the UK openEHR Clinical Knowledge Manager for each archetype into a text editor. We then reformatted the archetype into a Django model (or model_s_), mapping field types, validations, maxima and minima into their Django idiomatic equivalents. We kept as much contextual information as possible in `# comment` form.

* Models were quite large and therefore for better readbility and also in an effort to optimise the re-use potential of the models, they have been separated out from `models.py` into individual files under the `/models/`` directory, importable as a module because of the `__init__.py` containing an `__all__` list.

## Notes
* openEHR implementations tend to store data in documents rather than in relational tables, hence it's possible that in the conversion of Archetypes to Django models we will encounter modelled entities which are impractical to model in a relational fashion, however so far we've been able to model most things that made sense to model.

## Issues
* where Issues have arisen regarding upstream archetypes or an inability to accurately convert the archetype into a Django model, I've created a GitHub issue for it. In time we will pass upstream Issues back to the UK CKM in whatever way is preferred.

## Contributing
* We welcome contributions from the community, and are happy to consider pull requests for bugfixes, optimisations and new archetypes.
