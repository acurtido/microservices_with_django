import json, os, django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.apps import apps

Wishlist = apps.get_model('wishlist', 'WishList')

consumer = Consumer({
    'bootstrap.servers': 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'RJYEK5WX3NACCL7I',
    'sasl.password': 'M2y8aiqspkOD8JwGAyfz2/NHiMvNXGi8hbx9CW3ctULG+DfxpoLxW96wxp91/jvh',
    'sasl.mechanism': 'PLAIN',
    'group.id': 'wishlist_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['user_registered'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print("Received message with Value: {}".format(msg.value()))
    print("Message Topic: {}".format(msg.topic()))
    print("Message Key: {}".format(msg.key()))

    topic = msg.topic()
    value = msg.value()

    if topic == 'user_registered':
        if msg.key() == b'create_user':
            user_data = json.loads(value)
            user_id = user_data['id']
            # create a wishlist for the user with the user_id
            wishlist, created = Wishlist.objects.get_or_create(user_id=user_id, defaults={'total_items': 0})
            if created:
                wishlist.save()
    # elif topic == b'"product_added_to_wishlist"':
    #     # execute logic for product_added_to_cart event
    #     if msg.key() == 'add_product_to_wishlist':
    #         print('Add product to user wishlist')
    #         print(json.loads(value))
    #         pass
        pass

consumer.close()