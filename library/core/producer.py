from confluent_kafka import Producer
import os

producer = Producer({
    'bootstrap.servers': 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'RJYEK5WX3NACCL7I',
    'sasl.password': 'M2y8aiqspkOD8JwGAyfz2/NHiMvNXGi8hbx9CW3ctULG+DfxpoLxW96wxp91/jvh',
    'sasl.mechanism': 'PLAIN',
})