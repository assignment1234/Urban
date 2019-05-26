import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', arguments={'x-max-priority': 10})

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    return

channel.basic_consume("hello", callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()