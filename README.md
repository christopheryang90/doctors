to run:
  - pip install flask
    or specify python27 -m pip install flask (I wrote it in python2, but in case your env is 3)
  - python app.y



test adding appointment:
curl -d "date=2019-8-25&time=9:00&kind=sick&notes=hurts&patient=chris&doctor=doc-1" -X POST http://localhost:5000/add_appointment

test deleting appointment:
curl -X DELETE http://localhost:5000/delete_appointment/doc-1/2019-8-25/9:00/chris

test listing appointment:
curl -X GET http://localhost:5000/get_appointments?doctor=doc-1&date=2019-8-25

test listing doctors:
curl -X GET http://localhost:5000/get_doctors