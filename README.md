Python-QAAutomation-Framework

Command to execute the UI Sanity Scripts:

pytest -v -m sanityCORP
pytest -v -m sanityINS
pytest -v -m sanityFI
pytest -v -m sanityUSPF
pytest -v -m sanitySF

Command to Execute the API scripts:
pytest -v -m Sanity

Command to Execute the services scripts:
pytest -v -m api (Default staging Env)
pytest -v --ENV dev -m api

#Test Push
#Test Push
#Test Local
