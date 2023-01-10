import json, os, django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

consumer = Consumer({
    'bootstrap.servers': 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'RJYEK5WX3NACCL7I',
    'sasl.password': 'M2y8aiqspkOD8JwGAyfz2/NHiMvNXGi8hbx9CW3ctULG+DfxpoLxW96wxp91/jvh',
    'sasl.mechanism': 'PLAIN',
    'group.id': 'boomslagMicroservices',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['default'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print("Received message: {}".format(msg.value()))

    # topic = msg.topic()
    # value = msg.value()

    # if topic == 'transactions':
    #     # execute logic for user_registered event
    #     if msg.key() == b'"order_created"':
    #         print('Add transaction here')
    #         print(json.loads(value))
    #         pass

consumer.close()